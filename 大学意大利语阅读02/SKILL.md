---
name: 大学意大利语阅读02
description: >
  第二课 La stipsi di Godot — 基于第一课HTML模板替换内容，生成完整交互式HTML教学页面。
  包含四模块（课文Testo、单词表Vocabolario、注释Note、练习Esercizi），
  段落级/单词级edge-tts音频播放，中文译文，交互式练习，语速控制，原文蒙版。
  大量对话段落，使用 dq/attr CSS 标签处理说话人标注。
  使用 edge-tts it-IT-IsabellaNeural 意大利女声生成全部音频。
agent_created: true
---

# 大学意大利语阅读教程 02 — 第二课 La stipsi di Godot

## 触发词
"大学意大利语阅读02"、"第二课"、"La stipsi di Godot"、"lezione2"

## 课文数据
- **课文标题**: La stipsi di Godot（戈多便秘症）
- **段落数**: 43段（大量对话式，用 dq/attr 处理说话人标注）
- **单词数**: 8个词汇
- **注释数**: 12条
- **练习**:
  - Ex1: 10道阅读理解问答
  - Ex2: 20个词语/表达法造句
  - Ex3: Fare un breve riassunto del testo（课文摘要写作，textarea + 参考摘要折叠）
  - Ex4: Leggere il testo e tradurre in cinese（Il devoto di San Giuseppe 阅读翻译）
  - Ex4 附带单词表：devoto, basta, orazione, cero, elemosina, ostinarsi, battibecco, impiantare

## 完整构建流程

### 1. 内容准备
- 课文文本（43段对话式，包含 dq 说话内容和 attr 说话人属性）
- 8个词汇 + 12条注释
- 10道阅读理解 + 20个造句短语 + 摘要写作 + 阅读翻译题

### 2. 构建HTML页面
**核心原则：完全复制 lezione1.html 的HTML结构/UI样式/布局，只替换文本内容**

**方法一：文本替换（推荐）**
- 用 `lezione1.html` 作为模板
- 按顺序替换 4 个 section 的内容：
  1. Testo（全文 + read-full-bar）
  2. Vocabolario（单词 grid）
  3. Note（12条注释 + play按钮）
  4. Esercizi（4组练习）

**方法二：Python脚本重建**
- 用 `html.find()` 定位 section 边界
- ⚠️ 注意：Esercizi section 没有 `</section>` 闭合标签（extend到文件尾）
- ⚠️ 注意：搜索 class 要完整匹配 `class="section-card testo"` 而非 `class="section-card"`
- 用 `html.rfind('</section>', ts, next_section_start)` 确定 section 边界

**对话标签：**
```html
<p class="dialogue-line">
  <span class="dq">对话内容</span>
  <span class="attr">说话人描述</span>
</p>
```

### 3. Note区（注释）结构
```html
<div class="note-item">
  <div class="expr-wrap">
    <div class="expr">表达式</div>
    <button class="play-btn" data-word="表达式" onclick="playWord(this)">...</button>
  </div>
  <div class="desc">中文解释</div>
  <div class="example">例句<span class="cn-ex">例句中文翻译</span></div>
</div>
```
⚠️ 每条注释必须有 play-btn，play-btn 的 data-word 属性必须与 w_map.json 匹配

### 4. Esercizi（练习）结构
**Ex1 问答：**
```html
<div class="ex-item">
  <div class="ex-q-row">
    <span class="ex-num">1)</span>
    <span class="ex-text">问题</span>
    <button class="btn-answer" onclick="toggleAnswer(this, '答案')">答案</button>
  </div>
  <div class="answer-box"></div> <!-- 必须留空 -->
</div>
```
⚠️ answer-box 必须为空（`<div class="answer-box"></div>`），答案仅存于 onclick 属性

**Ex2 造句：**
```html
<div class="ex-term-wrap">
  <span class="term" onclick="toggleTermAnswer(this, '例句')">词汇</span>
  <div class="term-answer">例句</div>
</div>
```

**Ex3 摘要写作：**
```html
<textarea id="summary" rows="6" style="..."></textarea>
<button class="ex4-toggle" onclick="toggleSummary(this)">显示参考摘要</button>
<div class="ex4-translation"><!-- 参考摘要内容 --></div>
```
需要添加 `toggleSummary()` JS函数

**Ex4 阅读翻译：**
- 意大利语原文（Il devoto di San Giuseppe）+ 单词表 + textarea + 参考译文折叠
- 需要添加 `toggleEx4Translation()` JS函数

### 5. 生成音频
**目录**: `audio2/`（与 audio/ 区分）
**段落音频**: 43段 + 全文
**单词音频**: 8词汇 + 12注释 + 8 Ex4词汇 = 28个
**索引**: `audio2/w_map.json`, `audio2/p_map.json`
**音频JSON格式**: `{"b64": "<base64>", "text": "<原文>"}`
**文件名**: base64编码（无填充`=`）

⚠️ **关键陷阱**: 段落音频必须严格匹配HTML中的段落拆分。如果音频段落数 ≠ HTML段落数，从第一个不匹配的位置起全部错位。

### 6. HTML调整
**顶部导航栏（lesson-nav top）：**
- 导航页（链接到 index.html）
- 上一课（链接到 lezione1.html，绿色 `class="prev"`）
- 下一课（灰色 disabled）

**底部导航栏（lesson-nav bottom）：**
- 导航页 / 上一课（绿色） / 下一课

**导航页（index.html）：**
- 第二课卡片改为可点击（移除 `coming` 类）
- 标题改为 "La stipsi di Godot"
- 底部可选：上一课/下一课导航（用户有时需要有时不需要）

### 7. CSS新增
- `.lesson-nav a.prev` — 绿色背景按钮（与 `.next` 相同样式）

## 关键陷阱
- **段落音频偏移**: 音频段落数必须等于HTML段落数，否则从第一个差值起全部错位
- **w_map.json格式**: 必须是扁平结构 `{"word": "path"}`，不是 `{"words": {"word": "path"}}`
- **残留第一课内容**: 替换后必须全文搜索 Ciccio/ombrello/pioveva/aprile/passaggio/brontolare 等第一课关键词
- **破损HTML标签**: 替换后检查 `<span class="ex-text"Cosa` 这种缺少 `>` 的情况
- **删除旧音频文件**: 重新生成旧文件名需要清理 `audio2/w/` 和 `audio2/p/` 目录
- **注意**: `.section-card .section-body { padding: 32px; }` 被后续 `@media` 中的 `padding: 20px` 覆盖

## 参考文件
- `lezione2.html` — 完整HTML页面
- `audio2/w_map.json` — 单词音频索引
- `audio2/p_map.json` — 段落音频索引
- `rebuild_lezione2.py` — section重建脚本
- `regenerate_audio.py` — 段落音频生成脚本
- `fix_word_audio.py` — 单词音频生成脚本
