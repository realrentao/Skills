---
name: 意大利语等级考试模拟题
description: 生成意大利语CILS/CELI考级A1-C2全套模拟题交互式网页。包含60套独立模拟试卷（CILS 30 + CELI 30），每级5套，题型按各自真题独立设计。包含听力/阅读/语法/写作/口语5模块，每道听力带独立base64 JS音频文件、自动评分系统、填空显示正确答案、主观题显示参考范文。触发词：意大利语模拟题、CILS模拟、CELI模拟、意语考级、generate exam、生成意大利语试题。
agent_created: true
---

# 意大利语等级考试模拟题

## 概述

生成 CILS（锡耶纳大学）和 CELI（佩鲁贾大学）意大利语等级考试的完整模拟题交互式 HTML 网页。

**架构变化**：
- 旧版：3套试题（CILS1/2/3 + CELI1/2/3），每套6个等级
- **新版：A1-C2每级5套独立试卷 = 60页（CILS 30 + CELI 30）**
- CILS 和 CELI 题库完全独立（670道题不重复）
- 按等级递进：A1日常→A2简单过去→B1虚拟式/新闻→B2专业论述→C1学术→C2哲学

## 触发场景

用户说 "意大利语模拟题"、"CILS 模拟"、"CELI 练习"、"意语考级"、"生成试题"、"A1练习" 等时触发。

## 工作流程

### 第 1 步：确认需求

- 考试类型：CILS（锡耶纳风格） / CELI（佩鲁贾风格） / 全部
- 等级：A1 / A2 / B1 / B2 / C1 / C2
- 套编号：1-5
- 是否新增题目/修改现有/只生成不用改题

### 第 2 步：数据文件说明

数据文件独立分开，互不干扰：

| 文件 | 内容 |
|------|------|
| `scripts/cils_data.py` | CILS 6级 × 5套完整题库（340题） |
| `scripts/celi_data.py` | CELI 6级 × 5套完整题库（330题） |

数据格式：
```python
# 听力/阅读：(question, "opt1|opt2|opt3|opt4", answer_index, "script_text")
CILS["A1"]["ascolto"] = [
    ("Di dove sei?", "Italia|Francia|Spagna|Germania", 0, "Ciao mi chiamo Marco e vengo da Roma."),
    ...
]

# 语法：(question, "keyword1|keyword2")
CILS["A1"]["grammatica"] = [
    ("Io _____ (essere) italiano.", "sono"),
    ...
]

# 写作/口语：(question, "keyword1|keyword2|keyword3")
CILS["A1"]["scrittura"] = [
    ("Scrivi una breve presentazione...", "mi chiamo|anni|vengo|studio|mi piace"),
    ...
]
```

**关键规则**：
- 每个等级 `ascolto` 必须有 **25条**（5套 × 5题/套），不够则从 `EXTRA_` 字典补充
- `lettura` 15条（5套 × 2题 + 余量），`grammatica` 15条（5套 × 3题）
- CILS/CELI 之间题目不能重复
- 同一证书下5套题之间的题目不重复

### 第 3 步：生成全部 60 个 HTML 页面

```bash
cd <repo>
python scripts/fix_duplicate_sets.py
```

该脚本**一键完成**：
1. 从 `cils_data.py` / `celi_data.py` 读取数据
2. 在内存中添加 `EXTRA_CILS`/`EXTRA_CELI` 额外听力题（将不足25题的补到25题）
3. 生成 60 个 HTML 页面（`CILS|CELI/A1-C2/Set_1-5/*.html`）
4. 生成 300 个音频 JS + 300 个文本 TXT 文件（edge-tts）
5. 生成导航页 `index.html`
6. 推送到 GitHub

**如只需重新生成 HTML 不加音频**（比如改题目不改音频）：
```bash
python scripts/add_answers.py
# 只改 HTML 内容，不改音频
```

### 第 4 步：修正重音符号（可选）

如需全面修正意大利语单词的重音符号（è/à/ì/ò/ù）：

```bash
python scripts/fix_accents_final.py
```

### 第 5 步：导航页

导航页在每次生成时自动创建（`gen_independent.py`/`fix_duplicate_sets.py` 内置）。

如果只需要重新生成导航页：
```bash
python scripts/create_nav_v3.py
```

导航结构：
```
index.html
├── CILS/ (蓝色)
│   ├── A1/Set_1..5
│   ├── A2/Set_1..5
│   └── ...C2
└── CELI/ (酒红色)
    ├── A1/Set_1..5
    └── ...
```

## 答题评分系统

### 提交后显示内容

| 题型 | 显示内容 |
|------|---------|
| 听力/阅读 (radio) | ✅ 对/错 + 正确答案 + 听力原文 |
| 语法填空 | ✅ 对/错评分 + **正确答案** (data-answer) |
| 小作文 | ✅ 评分 + **参考范文** (data-reference) |
| 口语 | ✅ 评分 + **回答参考** (data-reference) |
| 总评 | 得分栏 + 等级标签 (Eccellente→Grave) |
| 明细表 | 各模块得分表格 |

### 评分规则

| 模块 | 满分 | 评分方式 |
|------|:----:|----------|
| 听力 | 20 | radio 精确匹配 |
| 阅读 | 20 | radio 精确匹配 |
| 语法 | 20 | 关键词模糊匹配 (normalize + includes) |
| 写作 | 20 | 关键词命中率(0-20) + 字数加成(0-5)，封顶20 |
| 口语 | 20 | 关键词命中率(0-20) + 字数加成(0-5)，封顶20 |

等级：≥85% Eccellente / ≥70% Buono / ≥55% Discreto / ≥40% Insufficiente / <40% Grave

## 音频系统

### 播放流程
```
点击 ▶ Ascolta
  → playAudio(btn)
  → 设置 window._audioLoaded callback
  → <script> 加载 "audio/cils_1_1_a1.js"
  → JS 文件 IIFE: (function(){var b64="...";if(window._audioLoaded)window._audioLoaded(b64);})()
  → callback 解码 AudioContext → 播放
```

### JS 变量冲突（已修复 ⚠️）
**旧 Bug**：`sub()` 函数中用 `var kws=` 声明本地数组，与全局函数 `function kws()` 重名，导致评分失败
**修复**：本地变量改为 `kwlist`，调用时 `kws(ut,kwlist)`

### 答案显示属性
- 语法题：`data-answer="corretta_parola"` + JS 显示 "Risposta corretta: xxx"
- 写作/口语：`data-reference="testo_di_riferimento"` + JS 显示 "Risposta di riferimento: xxx"
- 参考范文在 `add_answers.py` 的 `REFERENCES` 字典中，按等级和证书分开

## ⚠️ 关键操作顺序（必读）

每次修改数据后，按此顺序执行：

```bash
# 第1步：修改数据 → 生成60页HTML + 300音频 + 推送
python scripts/fix_duplicate_sets.py
# 从 cils_data.py / celi_data.py 读取数据，生成页面、音频、推送

# 第2步：添加答案显示功能（fix_duplicate_sets.py 的JS不含此功能）
python scripts/add_answers.py
# 加 data-answer/data-reference + kwlist JS修复 + 推送

# 第3步：修正意大利语重音符号
python scripts/fix_accents_all.py
# 修复 c'è/perché/società/città 等重音 + 重新生成HTML + 推送

# 第4步（可选）：全面语法检查
python scripts/check_grammar.py
```

## 数据文件

| 文件 | 说明 |
|------|------|
| `cils_data.py` | CILS 题库（A1→C2，ascolto 25题 + lettura 15题 + grammatica 15题 + scrittura 5题 + orale 5题） |
| `celi_data.py` | CELI 题库（同上结构，独立命题） |

## 生成脚本

| 脚本 | 功能 |
|------|------|
| `fix_duplicate_sets.py` | **主生成器**：生成60页HTML→300音频JS→300文本TXT→推送GitHub |
| `add_answers.py` | **次生成器**：加 data-answer/data-reference + kwlist JS修复 |
| `fix_accents_all.py` | **重音修正器**：修复数据源和HTML中所有缺失重音 |
| `fix_accents_final.py` | 重音修正（旧版，被 fix_accents_all.py 取代） |
| `check_grammar.py` | **语法检查器**：扫描所有问题的语法/内容问题 |
| `gen_independent.py` | 原始生成器（备用） |
| `create_nav_v3.py` | 导航页生成器 |

## 数据结构

### ascolto / lettura（选择题）
```python
[("问题?", "选项1|选项2|选项3|选项4", 答案索引, "听力脚本"), ...]
# ascolto: 25题/级 = 5套×5题 全不重复
# lettura: 15题/级 = 5套×3题
```

### grammatica（填空题）
```python
[("Completa: Io _____ (essere) italiano.", ["sono"]), ...]
# 15题/级 = 5套×3题，每套不同
```

### scrittura（小作文）
```python
[("题目描述 40-50 parole.", ["关键词1",...]), ...]
# 5题/级 = 5套×1题
```

## GitHub 推送

- 脚本自动推送：GitHub API 逐文件 PUT，自动重试 409 Conflict
- 备用：`git add -A && git commit -m "msg" && git pull --rebase origin master && git push origin master`
- 强制覆盖：`git push origin master --force`

## 避坑指南 ⚠️

### 1. 操作顺序必须遵守
fix_duplicate_sets.py → add_answers.py → fix_accents_all.py。跳过任一环节会导致功能缺失。

### 2. ascolto 必须有25题/级
15题只能覆盖3套，不够5套独立。EXTRA_ 字典提供额外10题。

### 3. JS kws 变量冲突
sub() 中不能用 `var kws=`（与全局 function kws() 重名）。必须用 `kwlist`。

### 4. 答案索引必须对应脚本
特别是 extra 题的 ans 值，要确认 keyword 在 script 中出现。

### 5. 单引号转义
data-script 属性中的 `'` → `&#39;`，否则浏览器截断。

### 6. 重音须在数据源中修复
只修 HTML 不够——下次 regenerate 会覆盖。必须同步修改 cils_data.py / celi_data.py。

## 演示地址
https://realrentao.github.io/italiano-esami/
