#!/usr/bin/env python3
"""
涛哥交易系统 - 选股四维评分脚本

基于交易系统四维模型对A股候选标的进行自动化评分：
  - 量价形态 (40%)
  - 业绩驱动 (25%)
  - 资金面 (20%)
  - 题材催化 (15%)

输入：JSON 格式的标的原始数据（来自 westock-data / neodata）
输出：JSON 格式的评分结果，含各维度得分、总分、风险信号、操作建议

用法：
  python score_stock.py --input data.json [--output result.json]
  python score_stock.py --stdin < data.json
"""

import json
import sys
import argparse
from datetime import datetime


# ─────────────────────────────────────────────
# 评分权重（与交易系统一致）
# ─────────────────────────────────────────────
WEIGHTS = {
    "volume_price": 0.40,  # 量价形态
    "performance":  0.25,  # 业绩驱动
    "capital_flow": 0.20,  # 资金面
    "catalyst":     0.15,  # 题材催化
}


# ─────────────────────────────────────────────
# 维度一：量价形态评分 (0-100)
# ─────────────────────────────────────────────
def score_volume_price(data: dict) -> dict:
    """
    评估威科夫阶段 + 量价信号 + 三周期共振
    """
    score = 50  # 基准分
    signals = []
    risk_flags = []

    # 1. 威科夫阶段判定 (-20 ~ +30)
    wyckoff_stage = data.get("wyckoff_stage", "unknown")
    stage_scores = {
        "A": 20,   # 吸筹建仓 - 分批建仓期
        "B": 25,   # 洗盘震仓 - 加仓点
        "C": 15,   # 首次拉升 - 持有
        "D": -5,   # 主升浪 - 高位谨慎
        "E": -20,  # 出货期 - 远离
        "unknown": 0,
    }
    stage_add = stage_scores.get(wyckoff_stage, 0)
    score += stage_add
    if wyckoff_stage != "unknown":
        signals.append(f"威科夫阶段{wyckoff_stage}(+{stage_add})")

    # 2. 量价信号 (+5 ~ +15 each)
    vp_signals = data.get("volume_price_signals", [])
    signal_scores = {
        "Spring": 15,
        "LPS": 15,
        "Stopping_Volume": 10,
        "Absorption": 8,
        "SC": 5,          # 需等二次测试
        "Test_shrink": 8,  # 缩量测试=合格
        "Test_expand": -5, # 放量测试=还有抛压
        "UT": -15,
        "BC": -15,
        "DE": -10,
    }
    for sig in vp_signals:
        s = signal_scores.get(sig, 0)
        score += s
        if s > 0:
            signals.append(f"{sig}(+{s})")
        elif s < 0:
            risk_flags.append(f"{sig}({s})")

    # 3. 量价结构健康度 (-10 ~ +10)
    # 涨放量跌缩量 = 健康
    vp_structure = data.get("vp_structure", "unknown")
    structure_scores = {
        "up_vol_down_shrink": 10,  # 涨放量跌缩量 = 最健康
        "up_vol_down_vol": 5,       # 涨放量跌也放量 = 一般
        "up_shrink_down_vol": -10,  # 涨缩量跌放量 = 危险
        "up_shrink_down_shrink": 0, # 都缩量 = 观望
        "unknown": 0,
    }
    score += structure_scores.get(vp_structure, 0)
    if vp_structure in ["up_vol_down_shrink"]:
        signals.append("涨放量跌缩量(+10)")
    elif vp_structure == "up_shrink_down_vol":
        risk_flags.append("涨缩量跌放量(-10)")

    # 4. 三周期共振 (-5 ~ +15)
    weekly_ok = data.get("weekly_trend_up", False)
    daily_ok = data.get("daily_buy_signal", False)
    hourly_ok = data.get("hourly_trend_up", False)
    resonance_count = sum([weekly_ok, daily_ok, hourly_ok])
    if resonance_count == 3:
        score += 15
        signals.append("三周期共振(+15)")
    elif resonance_count == 2:
        score += 5
        signals.append("两周期共振(+5)")
    elif resonance_count == 1:
        score -= 5
        risk_flags.append("仅单周期(-5)")
    else:
        score -= 10
        risk_flags.append("无周期共振(-10)")

    # 5. 均线位置 (-5 ~ +5)
    price_above_ma20 = data.get("price_above_ma20", None)
    if price_above_ma20 is True:
        score += 5
        signals.append("站上MA20(+5)")
    elif price_above_ma20 is False:
        score -= 5
        risk_flags.append("跌破MA20(-5)")

    # Clamp
    score = max(0, min(100, score))

    return {
        "dimension": "量价形态",
        "weight": WEIGHTS["volume_price"],
        "raw_score": score,
        "weighted_score": round(score * WEIGHTS["volume_price"], 2),
        "signals": signals,
        "risk_flags": risk_flags,
    }


# ─────────────────────────────────────────────
# 维度二：业绩驱动评分 (0-100)
# ─────────────────────────────────────────────
def score_performance(data: dict) -> dict:
    """
    评估净利润增速、行业景气度、营收增长
    """
    score = 50
    signals = []
    risk_flags = []

    # 1. 净利润增速 (-20 ~ +25)
    profit_growth = data.get("profit_growth_yoy", None)
    if profit_growth is not None:
        if profit_growth > 100:
            score += 25
            signals.append(f"净利润增速{profit_growth:.0f}%(+25)")
        elif profit_growth > 50:
            score += 20
            signals.append(f"净利润增速{profit_growth:.0f}%(+20)")
        elif profit_growth > 20:
            score += 10
            signals.append(f"净利润增速{profit_growth:.0f}%(+10)")
        elif profit_growth > 0:
            score += 0
            signals.append(f"净利润增速{profit_growth:.0f}%(+0)")
        elif profit_growth > -20:
            score -= 10
            risk_flags.append(f"净利润下滑{profit_growth:.0f}%(-10)")
        else:
            score -= 20
            risk_flags.append(f"净利润大幅下滑{profit_growth:.0f}%(-20)")

    # 2. 营收增速 (-10 ~ +15)
    revenue_growth = data.get("revenue_growth_yoy", None)
    if revenue_growth is not None:
        if revenue_growth > 30:
            score += 15
            signals.append(f"营收增速{revenue_growth:.0f}%(+15)")
        elif revenue_growth > 10:
            score += 8
            signals.append(f"营收增速{revenue_growth:.0f}%(+8)")
        elif revenue_growth > 0:
            score += 0
        elif revenue_growth > -10:
            score -= 5
            risk_flags.append(f"营收下滑{revenue_growth:.0f}%(-5)")
        else:
            score -= 10
            risk_flags.append(f"营收大幅下滑{revenue_growth:.0f}%(-10)")

    # 3. 行业景气 (-10 ~ +15)
    industry_trend = data.get("industry_trend", "unknown")
    trend_scores = {
        "up": 15,        # 景气向上
        "stable": 5,     # 平稳
        "down": -10,     # 景气下行
        "unknown": 0,
    }
    s = trend_scores.get(industry_trend, 0)
    score += s
    if s > 0:
        signals.append(f"行业景气{industry_trend}(+{s})")
    elif s < 0:
        risk_flags.append(f"行业景气{industry_trend}({s})")

    # 4. ROE (-5 ~ +10)
    roe = data.get("roe", None)
    if roe is not None:
        if roe > 15:
            score += 10
            signals.append(f"ROE {roe:.1f}%(+10)")
        elif roe > 10:
            score += 5
            signals.append(f"ROE {roe:.1f}%(+5)")
        elif roe > 5:
            score += 0
        else:
            score -= 5
            risk_flags.append(f"ROE偏低{roe:.1f}%(-5)")

    score = max(0, min(100, score))

    return {
        "dimension": "业绩驱动",
        "weight": WEIGHTS["performance"],
        "raw_score": score,
        "weighted_score": round(score * WEIGHTS["performance"], 2),
        "signals": signals,
        "risk_flags": risk_flags,
    }


# ─────────────────────────────────────────────
# 维度三：资金面评分 (0-100)
# ─────────────────────────────────────────────
def score_capital_flow(data: dict) -> dict:
    """
    评估主力资金、融资余额、换手率、机构/北向买入
    """
    score = 50
    signals = []
    risk_flags = []

    # 1. 主力资金5日趋势 (-20 ~ +20)
    main_fund_5d = data.get("main_fund_net_5d", None)
    if main_fund_5d is not None:
        if main_fund_5d > 0:
            score += 20
            signals.append(f"5日主力净流入{main_fund_5d:.0f}万(+20)")
        elif main_fund_5d > -5000:
            score -= 5
            risk_flags.append(f"5日主力小幅流出{main_fund_5d:.0f}万(-5)")
        else:
            score -= 20
            risk_flags.append(f"5日主力大幅流出{main_fund_5d:.0f}万(-20)")

    # 2. 融资余额变化 (-10 ~ +10)
    margin_change = data.get("margin_balance_change_pct", None)
    if margin_change is not None:
        if margin_change > 5:
            score += 10
            signals.append(f"融资余额增长{margin_change:.1f}%(+10)")
        elif margin_change > 0:
            score += 5
            signals.append(f"融资余额微增{margin_change:.1f}%(+5)")
        elif margin_change > -5:
            score -= 5
        else:
            score -= 10
            risk_flags.append(f"融资余额大降{margin_change:.1f}%(-10)")

    # 3. 换手率 (-10 ~ +10)
    turnover_rate = data.get("turnover_rate", None)
    if turnover_rate is not None:
        if 5 <= turnover_rate <= 15:
            score += 10
            signals.append(f"换手率{turnover_rate:.1f}%(理想区间+10)")
        elif 3 <= turnover_rate < 5:
            score += 5
            signals.append(f"换手率{turnover_rate:.1f}%(偏低+5)")
        elif turnover_rate > 15:
            score -= 5
            risk_flags.append(f"换手率过高{turnover_rate:.1f}%(-5)")
        elif turnover_rate > 20:
            score -= 10
            risk_flags.append(f"换手率极高{turnover_rate:.1f}%(-10)")

    # 4. 北向/机构买入 (-10 ~ +15)
    northbound_net = data.get("northbound_net_buy", None)
    if northbound_net is not None:
        if northbound_net > 0:
            score += 15
            signals.append(f"北向净买入{northbound_net:.0f}万(+15)")
        else:
            score -= 10
            risk_flags.append(f"北向净卖出{northbound_net:.0f}万(-10)")

    # 5. 基金持仓家数 (-15 ~ +10)
    fund_holders = data.get("fund_holder_count", None)
    if fund_holders is not None:
        if fund_holders > 10:
            score += 10
            signals.append(f"基金持仓{fund_holders}家(+10)")
        elif fund_holders > 0:
            score += 5
            signals.append(f"基金持仓{fund_holders}家(+5)")
        else:
            score -= 15
            risk_flags.append("基金0持仓(-15)⚠️双杀信号")

    score = max(0, min(100, score))

    return {
        "dimension": "资金面",
        "weight": WEIGHTS["capital_flow"],
        "raw_score": score,
        "weighted_score": round(score * WEIGHTS["capital_flow"], 2),
        "signals": signals,
        "risk_flags": risk_flags,
    }


# ─────────────────────────────────────────────
# 维度四：题材催化评分 (0-100)
# ─────────────────────────────────────────────
def score_catalyst(data: dict) -> dict:
    """
    评估政策催化、行业涨价、技术突破、美股映射等
    """
    score = 50
    signals = []
    risk_flags = []

    # 1. 政策催化 (-5 ~ +20)
    policy_catalyst = data.get("policy_catalyst", "none")
    policy_scores = {
        "strong": 20,     # 国常会/重大政策
        "moderate": 10,   # 部委/行业政策
        "weak": 5,        # 地方/一般政策
        "none": 0,
        "negative": -5,   # 利空政策
    }
    s = policy_scores.get(policy_catalyst, 0)
    score += s
    if s > 0:
        signals.append(f"政策催化{policy_catalyst}(+{s})")
    elif s < 0:
        risk_flags.append(f"政策利空({s})")

    # 2. 行业涨价 (-5 ~ +15)
    price_trend = data.get("industry_price_trend", "stable")
    price_scores = {
        "surging": 15,    # 产品大幅涨价
        "rising": 10,     # 产品涨价
        "stable": 0,
        "falling": -5,    # 产品降价
        "crashing": -10,  # 产品大幅降价
    }
    s = price_scores.get(price_trend, 0)
    score += s
    if s > 0:
        signals.append(f"行业价格{price_trend}(+{s})")
    elif s < 0:
        risk_flags.append(f"行业价格{price_trend}({s})")

    # 3. 技术突破 (-5 ~ +15)
    tech_breakthrough = data.get("tech_breakthrough", "none")
    tech_scores = {
        "major": 15,     # 重大技术突破
        "minor": 8,      # 一般技术进展
        "none": 0,
        "disrupted": -5,  # 技术路线被替代
    }
    s = tech_scores.get(tech_breakthrough, 0)
    score += s
    if s > 0:
        signals.append(f"技术突破{tech_breakthrough}(+{s})")

    # 4. 美股映射 (-5 ~ +10)
    us_mapping = data.get("us_mapping", "none")
    us_scores = {
        "strong": 10,    # 核心对标美股大涨
        "moderate": 5,   # 间接映射
        "none": 0,
        "negative": -5,  # 对标美股大跌
    }
    s = us_scores.get(us_mapping, 0)
    score += s
    if s > 0:
        signals.append(f"美股映射{us_mapping}(+{s})")
    elif s < 0:
        risk_flags.append(f"美股映射{us_mapping}({s})")

    # 5. 题材持续性 (-5 ~ +10)
    catalyst_durability = data.get("catalyst_durability", "unknown")
    durability_scores = {
        "long_term": 10,    # 持续6个月以上
        "medium_term": 5,   # 持续1-6个月
        "short_term": 0,    # 短期炒作
        "unknown": 0,
        "fading": -5,       # 题材消退
    }
    s = durability_scores.get(catalyst_durability, 0)
    score += s
    if s > 0:
        signals.append(f"题材持续性{catalyst_durability}(+{s})")
    elif s < 0:
        risk_flags.append(f"题材消退({s})")

    score = max(0, min(100, score))

    return {
        "dimension": "题材催化",
        "weight": WEIGHTS["catalyst"],
        "raw_score": score,
        "weighted_score": round(score * WEIGHTS["catalyst"], 2),
        "signals": signals,
        "risk_flags": risk_flags,
    }


# ─────────────────────────────────────────────
# 估值红线检查（一票否决）
# ─────────────────────────────────────────────
def check_valuation_redlines(data: dict) -> list:
    """
    检查估值红线，触发任一条件 = 坚决不进
    """
    red_flags = []

    pe = data.get("pe", None)
    industry_avg_pe = data.get("industry_avg_pe", None)
    if pe is not None and industry_avg_pe is not None:
        if pe > industry_avg_pe * 2:
            red_flags.append(f"🔴 PE {pe:.1f} > 行业均值{industry_avg_pe:.1f}的2倍")

    ytd_gain = data.get("ytd_gain_pct", None)
    profit_growth = data.get("profit_growth_yoy", None)
    if ytd_gain is not None and ytd_gain > 150:
        if profit_growth is None or profit_growth < ytd_gain / 3:
            red_flags.append(f"🔴 年内涨幅{ytd_gain:.0f}% > 150%，业绩增速跟不上")

    fund_holders = data.get("fund_holder_count", None)
    if fund_holders == 0 and pe is not None and pe > 50:
        red_flags.append("🔴 基金0持仓 + 高PE = 双杀信号")

    margin_ratio = data.get("margin_to_float_pct", None)
    if margin_ratio is not None and margin_ratio > 5:
        red_flags.append(f"🔴 融资余额占流通市值{margin_ratio:.1f}% > 5%")

    return red_flags


# ─────────────────────────────────────────────
# 综合评分 & 操作建议
# ─────────────────────────────────────────────
def generate_recommendation(total_score: float, dimension_results: list, red_flags: list) -> dict:
    """
    根据综合得分和红线状态给出操作建议
    """
    # 红线一票否决
    if red_flags:
        return {
            "action": "🔴 别碰！",
            "reason": f"触发估值红线：{'; '.join(red_flags)}",
            "position": "0%",
        }

    # 综合评分区间
    if total_score >= 75:
        return {
            "action": "🟢 可以进场",
            "reason": "四维信号强劲，多维共振",
            "position": "3成底仓，盈利后加到5-7成",
        }
    elif total_score >= 60:
        return {
            "action": "🟡 轻仓试探",
            "reason": "部分维度尚可，但信号不够强",
            "position": "1-2成观察仓",
        }
    elif total_score >= 45:
        return {
            "action": "🟠 观望为主",
            "reason": "信号偏弱，需等待更明确信号",
            "position": "0-1成",
        }
    else:
        return {
            "action": "🔴 别碰！",
            "reason": "多维信号偏弱或存在风险",
            "position": "0%",
        }


# ─────────────────────────────────────────────
# 主评分函数
# ─────────────────────────────────────────────
def score_stock(data: dict) -> dict:
    """
    对单只标的进行四维评分

    输入 data 字段说明：
      # 量价形态
      wyckoff_stage: str           - 威科夫阶段 A/B/C/D/E
      volume_price_signals: list   - 量价信号列表 [Spring, LPS, UT, BC...]
      vp_structure: str            - 量价结构 up_vol_down_shrink/up_shrink_down_vol等
      weekly_trend_up: bool        - 周线趋势向上
      daily_buy_signal: bool       - 日线有买入信号
      hourly_trend_up: bool        - 60分钟趋势向上
      price_above_ma20: bool       - 价格站上MA20

      # 业绩驱动
      profit_growth_yoy: float     - 净利润同比增速(%)
      revenue_growth_yoy: float    - 营收同比增速(%)
      industry_trend: str           - 行业景气 up/stable/down
      roe: float                    - ROE(%)

      # 资金面
      main_fund_net_5d: float       - 5日主力净流入(万)
      margin_balance_change_pct: float - 融资余额变化(%)
      turnover_rate: float           - 换手率(%)
      northbound_net_buy: float      - 北向净买入(万)
      fund_holder_count: int         - 基金持仓家数

      # 题材催化
      policy_catalyst: str           - 政策催化 strong/moderate/weak/none/negative
      industry_price_trend: str      - 行业涨价 surging/rising/stable/falling/crashing
      tech_breakthrough: str         - 技术突破 major/minor/none/disrupted
      us_mapping: str                - 美股映射 strong/moderate/none/negative
      catalyst_durability: str       - 题材持续性 long_term/medium_term/short_term/fading

      # 估值红线
      pe: float                      - 市盈率
      industry_avg_pe: float         - 行业平均PE
      ytd_gain_pct: float            - 年内涨幅(%)
      margin_to_float_pct: float     - 融资余额占流通市值(%)
    """
    # 四维评分
    vp_result = score_volume_price(data)
    pf_result = score_performance(data)
    cf_result = score_capital_flow(data)
    ct_result = score_catalyst(data)

    # 综合加权得分
    total = (
        vp_result["weighted_score"]
        + pf_result["weighted_score"]
        + cf_result["weighted_score"]
        + ct_result["weighted_score"]
    )

    # 估值红线
    red_flags = check_valuation_redlines(data)

    # 操作建议
    rec = generate_recommendation(total, [vp_result, pf_result, cf_result, ct_result], red_flags)

    # 汇总风险信号
    all_risks = []
    for dim in [vp_result, pf_result, cf_result, ct_result]:
        all_risks.extend(dim["risk_flags"])
    all_risks.extend(red_flags)

    return {
        "symbol": data.get("symbol", "UNKNOWN"),
        "name": data.get("name", "UNKNOWN"),
        "timestamp": datetime.now().isoformat(),
        "total_score": round(total, 2),
        "dimensions": [vp_result, pf_result, cf_result, ct_result],
        "valuation_red_flags": red_flags,
        "all_risk_flags": all_risks,
        "recommendation": rec,
    }


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="涛哥交易系统 - 选股四维评分")
    parser.add_argument("--input", "-i", help="输入JSON文件路径")
    parser.add_argument("--output", "-o", help="输出JSON文件路径")
    parser.add_argument("--stdin", action="store_true", help="从stdin读取JSON")
    args = parser.parse_args()

    # 读取输入
    if args.stdin:
        raw = sys.stdin.read()
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        print("错误：请指定 --input <file> 或 --stdin", file=sys.stderr)
        sys.exit(1)

    try:
        input_data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误：{e}", file=sys.stderr)
        sys.exit(1)

    # 支持单标的或多标的
    if isinstance(input_data, dict):
        stocks = [input_data]
    elif isinstance(input_data, list):
        stocks = input_data
    else:
        print("错误：输入须为JSON对象或数组", file=sys.stderr)
        sys.exit(1)

    # 评分
    results = []
    for stock in stocks:
        result = score_stock(stock)
        results.append(result)

    # 按综合得分排序（降序）
    results.sort(key=lambda x: x["total_score"], reverse=True)

    output = {
        "scoring_time": datetime.now().isoformat(),
        "scoring_model": "涛哥交易系统-四维评分 v1.0",
        "total_candidates": len(results),
        "results": results,
    }

    out_json = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_json)
        print(f"评分完成，结果已写入 {args.output}")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
