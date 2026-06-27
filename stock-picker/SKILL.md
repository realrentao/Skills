---
name: stock-picker
description: 基于「涛哥交易系统」四维模型从A股筛选最符合交易系统的标的。触发场景：选股、筛选股票、找买点、A股选股、扫描机会股、威科夫选股、量价选股、四维选股、哪只股值得买、帮我挑股票。该 Skill 融合威科夫量价体系、主力识别、估值判断与止损纪律，输出结构化评分报告与操作建议。
agent_created: true
---

# Stock Picker - 涛哥交易系统选股

## 概述

基于「涛哥交易系统」四维模型，从A股市场中筛选最符合交易系统的标的。核心原则：**主力是方向，估值是安全带，止损是保险绳**。融入威科夫量价体系，实现系统化、可量化、可复现的选股流程。

**四维模型权重：**

| 维度 | 权重 | 核心指标 |
|:---|:---:|:---|
| 量价形态 | 40% | 威科夫阶段A-B、缩地量企稳、涨放量跌缩量 |
| 业绩驱动 | 25% | 净利润增速>50%、行业景气向上 |
| 资金面 | 20% | 融资余额增加、北向/机构买入、换手率5-15% |
| 题材催化 | 15% | 国常会政策/行业涨价/技术突破/美股映射 |

## 选股工作流

### Phase 1：确定选股范围

根据用户输入确定选股范围，支持以下模式：

1. **指定板块/概念**：用户指定板块（如"AI算力""覆铜板"），用 `westock-data sector --search <关键词>` 或 `neodata-financial-search` 查询板块成分股
2. **指定个股评估**：用户给出具体股票代码/名称，直接进入 Phase 2 评估
3. **全市场扫描**：用 `westock-data hot stock` + `neodata-financial-search` 获取热门标的，结合板块资金流向筛选
4. **条件筛选**：用户给出筛选条件（如"净利润增速>30%、PE<30"），用 neodata-financial-search 自然语言查询

**输出**：候选标的列表（股票代码+名称），一般 5-20 只。

### Phase 2：逐只采集四维数据

对每只候选标的，按以下优先级采集数据：

#### 维度一：量价形态数据

| 数据项 | 数据源 | 命令 |
|:---|:---|:---|
| 日K线（20日） | westock-data | `westock-data kline <code> --period day --limit 20` |
| 周K线（20周） | westock-data | `westock-data kline <code> --period week --limit 20` |
| 60分钟K线 | westock-data | `westock-data kline <code> --period 60min --limit 20` |
| 技术指标（MACD） | westock-data | `westock-data technical <code> --group macd` |
| 分时数据 | westock-data | `westock-data minute <code>` |

**人工判定项**（基于K线数据，由 AI 分析）：
- 威科夫阶段判定（A/B/C/D/E）
- 量价信号识别（Spring/LPS/UT/BC等）
- 量价结构健康度（涨放量跌缩量？）
- 三周期共振状态
- 均线位置（MA20/MA60）

#### 维度二：业绩驱动数据

| 数据项 | 数据源 | 命令 |
|:---|:---|:---|
| 财务报表（4期） | westock-data | `westock-data finance <code> --num 4` |
| 公司简况 | westock-data | `westock-data profile <code>` |
| 业绩预告 | westock-data | `westock-data reserve <code>` |

**从财报中提取**：净利润同比增速、营收同比增速、ROE。

**行业景气度**：通过 neodata-financial-search 查询行业景气信息或 WebSearch 补充。

#### 维度三：资金面数据

| 数据项 | 数据源 | 命令 |
|:---|:---|:---|
| A股资金流向 | westock-data | `westock-data asfund <code>` |
| 龙虎榜 | westock-data | `westock-data lhb <code>` |
| 融资融券 | westock-data | `westock-data margintrade <code>` |
| 股东结构 | westock-data | `westock-data shareholder <code>` |
| 实时行情（换手率） | westock-data | `westock-data quote <code>` |

**从数据中提取**：5日主力净流入、融资余额变化、换手率、北向净买卖、基金持仓家数。

#### 维度四：题材催化数据

| 数据项 | 数据源 | 说明 |
|:---|:---|:---|
| 行业/板块动态 | neodata-financial-search | 查询板块异动、行业新闻 |
| 政策催化 | WebSearch | 搜索近期相关政策 |
| 美股映射 | neodata-financial-search | 查询对应美股标的走势 |
| 行业价格趋势 | WebSearch | 搜索行业产品涨价/降价信息 |

**题材催化需人工判定**，AI 根据搜索结果综合评估。

### Phase 3：四维评分

将 Phase 2 采集的数据组织为 JSON 格式，调用评分脚本：

```bash
python <skill_path>/scripts/score_stock.py --input <data.json> --output <result.json>
```

**输入 JSON 格式**（单只标的）：

```json
{
  "symbol": "sh600519",
  "name": "贵州茅台",
  "wyckoff_stage": "B",
  "volume_price_signals": ["Spring", "LPS"],
  "vp_structure": "up_vol_down_shrink",
  "weekly_trend_up": true,
  "daily_buy_signal": true,
  "hourly_trend_up": false,
  "price_above_ma20": true,
  "profit_growth_yoy": 15.3,
  "revenue_growth_yoy": 12.5,
  "industry_trend": "up",
  "roe": 18.5,
  "main_fund_net_5d": 5000,
  "margin_balance_change_pct": 3.2,
  "turnover_rate": 8.5,
  "northbound_net_buy": 2000,
  "fund_holder_count": 45,
  "policy_catalyst": "moderate",
  "industry_price_trend": "rising",
  "tech_breakthrough": "none",
  "us_mapping": "moderate",
  "catalyst_durability": "medium_term",
  "pe": 25.3,
  "industry_avg_pe": 30.0,
  "ytd_gain_pct": 35,
  "margin_to_float_pct": 1.2
}
```

**评分脚本字段说明**详见 `references/trading-system.md`。

### Phase 4：估值红线检查

估值红线为**一票否决**项，触发任一条即标记为"别碰"：

1. PE > 行业均值 2倍以上
2. 股价年内涨幅 > 150%，但业绩增速跟不上
3. 基金0持仓 + 高PE = 双杀信号
4. 融资余额占流通市值 > 5%

评分脚本已内置红线检查，也可在采集数据时提前筛查以节省时间。

### Phase 5：生成选股报告

按综合得分从高到低排序，输出结构化选股报告。报告格式如下：

---

#### 🏆 选股报告 - <日期>

**选股范围**：<板块/条件>
**候选数量**：X 只
**评分模型**：涛哥交易系统-四维评分

| 排名 | 代码 | 名称 | 综合得分 | 量价(40%) | 业绩(25%) | 资金(20%) | 题材(15%) | 操作建议 |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | sh600519 | 贵州茅台 | 72.5 | 82 | 65 | 70 | 55 | 🟢 可以进场 |
| 2 | ... | ... | ... | ... | ... | ... | ... | ... |

**⚠️ 红线标的（一票否决）**：

| 代码 | 名称 | 红线原因 |
|:---|:---|:---|
| sz002636 | 金安国纪 | 基金0持仓+高PE=双杀；年内涨幅>150%业绩不匹配 |

**Top 3 详细分析**：

（对排名前3的标的，输出各维度详细信号、风险提示、建议建仓价位与仓位配置）

---

### Phase 6：止损预设（对推荐标的）

对综合评分 ≥ 60 的推荐标的，必须给出：

| 止损类型 | 计算方式 | 价位 |
|:---|:---|:---|
| 硬止损 | 买入价 × 92% | XX.XX 元 |
| 技术止损 | MA20 下方 1-2% | XX.XX 元 |
| 时间止损 | 3-5天不涨反跌 | 3个交易日后评估 |

## 数据查询策略

### 优先级

1. **neodata-financial-search**：默认优先使用，适合自然语言查询、板块异动、宏观指标
2. **westock-data**：neodata 不覆盖时使用，适合技术指标、筹码、股东、龙虎榜等结构化数据
3. **WebSearch**：两个数据源都无法满足时使用，适合政策催化、行业新闻

### 批量查询优化

- westock-data `finance` 命令支持逗号分隔多股代码批量查询
- 同板块标的建议按板块分批采集，减少重复查询
- 行业平均PE只需查一次，同板块标的共用

### 代码格式

- 沪市：`sh600519`
- 深市：`sz000001`
- 科创板：`sh688xxx`
- 北交所：`bj8xxxx`

## 交易系统参考

完整的交易系统规则、威科夫量价信号谱图、买前必过清单详见 `references/trading-system.md`。

在执行选股流程时，加载 `references/trading-system.md` 以确保评分与交易系统一致。特别是：
- 威科夫九大量价信号的定义与判定标准
- 洗盘 vs 出货的区分标准
- 三周期共振分析法
- 买前必过清单（11项检查）

## 五大戒律（选股过程必须遵守）

1. **不追高** —— 任何买入都等缩量回调
2. **不死扛** —— 放量破支撑 = 走人
3. **不抄底** —— 等缩量企稳 + 放量反弹再进
4. **不贪婪** —— 达到目标位分批减仓
5. **不恐慌** —— 缩量回调是机会不是风险

## 输出规范

- 所有金额单位标注人民币（¥），港股/美股标注对应货币
- 涨用红色，跌用绿色（A股惯例）
- 数据出处必须标注（westock-data / neodata / WebSearch + 日期）
- 综合评分 ≥ 75 → 🟢；60-74 → 🟡；45-59 → 🟠；< 45 → 🔴
- 红线标的无论得分多少，统一标记 🔴 别碰

## Resources

### scripts/score_stock.py
四维评分脚本，接受 JSON 输入，输出结构化评分结果。支持单标的和多标的批量评分，自动按综合得分降序排列。

### references/trading-system.md
涛哥交易系统完整文档，包含四维模型、威科夫量价体系、买前必过清单、实战案例。选股过程中需加载此文件确保评分与交易系统一致。
