---
name: 大学意大利语阅读B版
description: >
  生成大学意大利语阅读教程第二课（La stipsi di Godot）的交互式HTML教学页面。
  戏剧对话型课文结构，31个对话行，66个段落，audio2/ 目录。
  第二课导航：有"返回首页" + "上一课(链接lezione1)" + "下一课(禁用)"。
  额外功能：Ex3摘要折叠（toggleSummary）+ Ex4翻译折叠（toggleEx4Translation）。
  继承"大学意大利语阅读"技能的所有核心功能。
  触发词与"大学意大利语阅读"相同，用此版本生成第二课。
agent_created: true
---

# 大学意大利语阅读B版 — 第二课（La stipsi di Godot）

基于"大学意大利语阅读"技能，针对**第二课**（戏剧对话型课文）的专项模板。

---

## 何时使用

用户要求生成大学意大利语阅读教程的第二课（课文名含"Godot"或明确指定"B版"）时，调用此技能。

---

## ★ 统一设计规范（两课共用，生成时严格遵循）

> ⚠️ 以下规范为 A版 / B版 共同遵守的设计标准，**所有字号/颜色/间距/字体必须在生成时应用此规范**，不得随意改动。

### 配色系统

| CSS变量 | 色值 | 用途 |
|---------|------|------|
| `--ita-green` | `#009246` | 意大利绿，主色调 |
| `--ita-white` | `#F1F2F1` | 意大利白 |
| `--ita-red` | `#CE2B37` | 意大利红 |
| `--gold` | `#C4A35A` | 金色点缀 |
| `--cream` | `#FAF8F3` | 页面背景 |
| `--text-dark` | `#2C2C2C` | 正文主色 |
| `--text-mid` | `#5C5C5C` | 次要文字/注释 |
| `--border-light` | `#E8E4DC` | 边框/分隔线 |
| `--shadow-card` | `0 4px 24px rgba(0,0,0,0.06)` | 卡片阴影 |
| `--radius` | `12px` | 圆角统一值 |

### 字体系统

| 字体 | 用途 | 声明顺序 |
|------|------|---------|
| **Playfair Display** | 页面标题、课文标题 | 第一位 serif |
| **Times New Roman** | 课文正文、单词表、练习 | 意大利语正文 |
| **Noto Serif SC** | 中文正文、译文 | 中文字体 |
| **Inter** | UI标签、按钮、导航 | sans-serif 首位 |

**Google Fonts 引用**：
```
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,500&family=Noto+Serif+SC:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
```

### 字号层级

| 元素 | 字号 |
|------|------|
| 书系标签 `.series` | 13px |
| 书名 `.book-title` | 22px |
| 课文意大利语正文 | 18px |
| 单词表单词 `.vocab-word` | 18px |
| 单词表词性 | 12px |
| 单词表中文释义 | 14px |
| 注释正文 `.note-body` | 15px |
| 练习说明文字 | 15px |
| 译文框 `.trans-box` | 15px |
| 译文框内金边翻译 | 15px |
| 按钮文字 `.para-btn` | 13px |
| 语速标签 | 12px |
| 章节标题 h3 | 18px |
| h3 数字圆圈 `.num` | 16px |
| 底部 Footer | 12px |

### 间距标准

| 类名 | 样式值 | 用途 |
|------|--------|------|
| `.p-wrap` | `margin-bottom: 0.75em` | 段落间距 |
| `.trans-bar` | `margin-top: 4px; margin-bottom: 0` | 按钮离正文近 |
| `.trans-box` | `margin: 0` | 译文紧贴按钮 |
| `.section-card.testo .section-body p` | `margin-bottom: 0` | p标签无额外margin |
| `.section-card.testo .section-body .dialogue-line` | `margin-bottom: 0` | 对话行无margin |
| `.vocab-item` | `padding: 10px 0; border-bottom: 1px solid var(--border-light)` | 单词间隔线 |
| `.note-item` | `margin-bottom: 16px` | 注释块间距 |
| `.exercise-section` | `margin-bottom: 28px` | 练习模块间距 |

### 布局规范

| 类名 | 样式值 | 用途 |
|------|--------|------|
| `.book-header` | `max-width: 1100px; margin: 0 auto; padding: 40px 40px 0; text-align: center` | 内容区居中 |
| `.unit-banner` | `max-width: 1100px; margin: 30px auto 0; padding: 0 40px` | banner居中 |
| `.content` | `max-width: 1100px; margin: 0 auto; padding: 0 24px 40px` | 主内容区 |
| `.section-card` | `max-width: 900px; margin: 0 auto 20px; border-radius: var(--radius)` | 卡片居中 |

### 动画与过渡

| 元素 | 样式值 | 用途 |
|------|--------|------|
| `.trans-box` 展开/收起 | `max-height` + `overflow: hidden` + `transition: max-height 0.35s ease` | 译文滑入 |
| `.btn-trans` hover | `background: #F0F5F0` | 按钮反馈 |
| `.lesson-nav a` hover | 颜色/背景变化 `transition: all 0.2s` | 导航反馈 |
| `.ribbon-nav a` | `transition: all 0.2s ease` | 锚点导航 |

### Box Model

```
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
```

### 媒体查询断点

```
@media (max-width: 768px) { ... }
```

---

## 与基础技能的核心差异

此版本（第二课）与第一课（A版）的差异点：

| 差异项 | A版（第一课） | B版（第二课） |
|--------|-------------|-------------|
| 课文名 | L'ombrello di Ciccio（奇奇的雨伞） | La stipsi di Godot（戈多的便秘） |
| 课文风格 | 叙述型，对话较少 | 戏剧对话型，对话密集 |
| 对话行数 | 17个 `dialogue-line` | 31个 `dialogue-line` |
| 段落总数 | 49个 `p-wrap` | 66个 `p-wrap` |
| 音频目录 | `audio/` | `audio2/` |
| 音频文件数 | 约26个段落音频 | 约46个段落音频 |
| 顶部导航 | `← 导航页` + `下一课(禁用)` | `← 导航页` + `← 上一课` + `下一课(禁用)` |
| 底部导航 | 同上 | 同上 |
| prev CSS | **无** `.lesson-nav a.prev` | **有** 绿色 `.lesson-nav a.prev` 样式 |
| Ex3摘要折叠 | **无** | **有** `toggleSummary()` |
| Ex4翻译折叠 | **无** | **有** `toggleEx4Translation()` |

---

## 导航HTML（顶部 + 底部各一份）

```html
<nav class="lesson-nav top">
  <a href="index.html" class="back">
    <svg viewBox="0 0 24 24"><polygon points="15,3 7,12 15,21" transform="scale(-1,1) translate(-22,0)"/></svg>
    导航页
  </a>
  <a href="lezione1.html" class="prev">
    <svg viewBox="0 0 24 24"><polygon points="15,3 7,12 15,21" transform="scale(-1,1) translate(-22,0)"/></svg>
    上一课
  </a>
  <a href="#" class="next disabled">
    下一课
    <svg viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21"/></svg>
  </a>
</nav>
```

底部重复一次，将 `class="lesson-nav top"` 改为 `class="lesson-nav bottom"`。

---

## CSS 导航样式（关键片段 — B版新增 .prev 样式）

```css
.lesson-nav a.back {
  background: transparent; color: var(--text-mid);
  border: 1.5px solid #D0D0D0;
}
.lesson-nav a.back:hover {
  border-color: var(--ita-green); color: var(--ita-green); background: #F0F5F0;
}
.lesson-nav a.prev {                        /* ★ B版新增 */
  background: var(--ita-green); color: #fff;
  border: 1.5px solid var(--ita-green);
}
.lesson-nav a.prev:hover { background: #007A38; }
.lesson-nav a.next {
  background: var(--ita-green); color: #fff;
  border: 1.5px solid var(--ita-green);
  margin-left: auto;                        /* ★ B版新增：右对齐 */
}
```

**关键**：`.lesson-nav a.next` 需要 `margin-left: auto` 使三个按钮左-中-右分布（back靠左，prev居中，next靠右）。

---

## 音频系统配置

```javascript
const [wMapResp, pMapResp] = await Promise.all([
  fetch('audio2/w_map.json'),
  fetch('audio2/p_map.json')
]);
```

所有 `fetch()` 调用使用 `audio2/` 前缀，不是 `audio/`。

---

## JavaScript 函数清单

B版**完整函数列表**（比A版多两个）：

| 函数名 | 用途 |
|--------|------|
| `stopAllAudio()` | 停止所有音频（单词+段落+全文） |
| `playWord(word, btn)` | 播放单词音频 |
| `playPara(btn, idx)` | 播放段落音频 |
| `playFullText()` | 播放全文音频 |
| `setParaSpeed(btn, speed)` | 切换段落语速 |
| `setWordSpeed(btn, speed)` | 切换单词语速 |
| `setFullSpeed(btn, speed)` | 切换全文语速 |
| `toggleTrans(btn, idx)` | 显示/隐藏单句译文 |
| `toggleOrig(btn)` | 显示/隐藏原文 |
| `toggleAnswer(btn, answer)` | 显示/隐藏练习答案 |
| `setGlobalSpeed(speed)` | 全局语速 |
| `toggleBlindMode()` | 原文蒙版盲听 |
| `setBlindModeSpeed(speed)` | 蒙版模式语速 |
| `toggleListening()` | 开启/关闭听力模式 |
| `toggleSummary(btn)` | **★ B版新增** Ex3摘要折叠/展开 |
| `toggleEx4Translation(btn)` | **★ B版新增** Ex4翻译折叠/展开 |

---

## toggleSummary / toggleEx4Translation 实现

### JS 函数（B版在所有播放函数之前定义）

```javascript
function toggleSummary(btn) {
    const box = btn.nextElementSibling;
    box.classList.toggle('open');
    const showing = box.classList.contains('open');
    btn.innerHTML = showing
      ? '<span class="arrow open">&#9660;</span> 隐藏参考摘要'
      : '<span class="arrow">&#9654;</span> 显示参考摘要';
}

function toggleEx4Translation(btn) {
    const box = btn.nextElementSibling;
    box.classList.toggle('open');
    const showing = box.classList.contains('open');
    btn.innerHTML = showing
      ? '<span class="arrow open">&#9660;</span; 隐藏参考译文'
      : '<span class="arrow">&#9654;</span> 显示参考译文';
}
```

### Ex3（摘要）HTML结构

```html
<!-- Ex 3: Riassunto（摘要）-->
<div class="exercise-section">
  <h3><span class="num">3</span> Fare un breve riassunto del testo — 写一篇课文摘要</h3>
  <p style="font-size:13px;color:var(--text-mid);margin-bottom:8px;">
    用意大利语写一段 80-120 词的短文，概括课文主要内容。
  </p>
  <textarea id="summary" rows="6" style="..."></textarea>
  <!-- 折叠按钮 + 折叠内容 -->
  <button class="ex4-toggle" onclick="toggleSummary(this)">
    <span class="arrow">&#9654;</span> 显示参考摘要
  </button>
  <div class="ex4-translation">
    <p>参考摘要的意大利语文本...</p>
  </div>
</div>
```

### Ex4（翻译）HTML结构

```html
<!-- Ex 4: Traduzione（翻译）-->
<div class="exercise-section">
  <h3><span class="num">4</span> Leggere il testo e tradurre in cinese — 阅读课文并译成中文</h3>
  <p style="font-size:13px;color:var(--text-mid);margin-bottom:10px;">
    阅读下面的意大利语短文，将其翻译成中文。
  </p>
  <!-- 意大利语原文展示区 -->
  <div style="font-family:'Times New Roman','Georgia',serif;font-size:18px;...">
    <p>意大利语原文...</p>
  </div>
  <!-- 折叠按钮 + 折叠内容 -->
  <button class="ex4-toggle" onclick="toggleEx4Translation(this)">
    <span class="arrow">&#9654;</span> 显示参考译文
  </button>
  <div class="ex4-translation">
    <p>中文翻译...</p>
  </div>
</div>
```

### CSS 支持样式

```css
.ex4-toggle {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 16px; font-size: 13px; font-weight: 500;
  border: 1.5px solid var(--ita-green); border-radius: 20px;
  background: transparent; color: var(--ita-green); cursor: pointer;
  margin-bottom: 12px;
}
.ex4-toggle .arrow { font-size: 10px; }
.ex4-toggle:hover { background: #F0F5F0; }
.ex4-translation {
  display: none;
  padding: 14px 18px;
  background: #F8F6F3; border-radius: 8px;
  border-left: 3px solid var(--gold);
  font-size: 15px; line-height: 1.8; color: #333;
  margin-bottom: 16px;
}
.ex4-translation.open { display: block; }
.ex4-translation .arrow { display: inline-block; transition: transform .2s; }
.ex4-translation .arrow.open { transform: rotate(180deg); }
```

---

## 第二课课文内容（La stipsi di Godot）

### Testo（课文）

课文为意大利语戏剧对话风格，大量对话，Alessio 和父母的互动 + 邻居 Signora Bice 的介入。

- **段落数量**：66个 `p-wrap`
- **对话行数**：31个 `dialogue-line`（比A版多很多）
- 对话用 `( )` 包裹说话人，`—` 引出说话内容
- 中文翻译用 `" "` 双引号

### Vocabolario（单词表）

约20-30个核心词汇，结构同A版。

### Note（注释）

语法和表达法讲解，同A版结构。

### Esercizi（练习）

**Ex 1** — 阅读理解问答（4-5题，答案折叠按钮）  
**Ex 2** — 造句（根据中文写意大利语句子）  
**Ex 3** — 写摘要（用意大利语写80-120词摘要）**★ 有折叠**  
**Ex 4** — 汉译意（阅读意大利语原文译成中文）**★ 有折叠**

---

## 完整HTML结构

```
<header> book-header (书名)
<div> unit-banner (单元标题)
<nav> ribbon-nav (章节锚点)
<div class="content">
  <section id="testo"> ... </section>
  <section id="vocabolario"> ... </section>
  <section id="note"> ... </section>
  <section id="esercizi"> (含 Ex3摘要折叠 + Ex4翻译折叠) </section>
</div>
<nav> lesson-nav top (含prev链接)
<footer> page-footer
<script> (滚动监听)
```

---

## 部署方式

与"大学意大利语阅读"基础技能相同，通过 GitHub Git Data API 推送。
第二课的 `prev` 链接为 `href="lezione1.html"`，`next` 按钮使用 `href="#"` + `class="disabled"`。

---

## 踩坑补充（B版专属）

1. **prev 链接目标**：始终链接到 `lezione1.html`，不要硬编码错误的文件名
2. **audio 目录为 audio2/**：不是 `audio/`，确保 fetch 路径正确
3. **对话行 31 个**：比A版（17个）多很多，段落索引映射要正确对应
4. **段落总数 66 个**：p_map.json 中段落索引 0-65
5. **Ex3/Ex4 折叠 JS**：两个函数必须定义在所有播放函数之前，确保 onclick 引用生效
6. **.ex4-translation.open**：默认隐藏，`.open` 类控制 display:block
7. **prev 按钮 margin**：`.next` 需要 `margin-left: auto` 实现三栏右对齐
