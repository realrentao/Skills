---
name: 大学意大利语阅读
description: >
  从扫描版PDF或课文内容，生成大学意大利语阅读教程交互式HTML教学页面。
  包含四模块（课文Testo、单词表Vocabolario、注释Note、练习Esercizi），
  段落级/单词级edge-tts音频播放，中文译文，交互式练习，语速控制，原文蒙版盲听。
  使用边缘TTS意大利女声生成全部音频，拆分独立JSON文件并行加载。
  支持GitHub Pages部署。
agent_created: true
---

# 大学意大利语阅读教程 — 交互式课文HTML生成流程

从扫描版PDF或已有课文内容生成完整的交互式HTML教学页面，包含四模块（课文Testo、单词表Vocabolario、注释Note、练习Esercizi），支持段落级/单词级音频播放、中文译文、交互式练习、语速控制、原文蒙版。

---

## 触发词

"大学意大利语阅读"、"课文HTML"、"意大利语课文页面"、"生成课文网页"

## 完整工作流

### 第1步：提取课文内容

根据输入源选择方法：

**A. 扫描版PDF（无文字层）**
1. 用 `PyMuPDF (fitz)` 将PDF关键页转为PNG图片（Matrix 1.5x 分辨率）
2. 使用 `tesseract.js`（Node.js）进行OCR识别，语言配置 `ita+chi_sim`
3. 或使用 WorkBuddy 内置多模态能力直接读取图片内容

**B. 已有文本内容**
直接解析并结构化

**C. 搜索引擎查找**
搜索关键词如 `"大学意大利语阅读教程1" 课文内容`，从公开资源提取

### 第2步：结构化内容

将提取内容分为4个模块：

| 模块 | 数据结构 |
|------|---------|
| **Testo（课文）** | 按段落拆分，对话用 `( )` 包裹，说话人用 `—` 引出，对话+说话人同一行 |
| **Vocabolario（单词表）** | 单词 + 词性 + 中文释义 |
| **Note（注释）** | 语法/表达法讲解 + 中文解释 |
| **Esercizi（练习）** | 阅读理解题(问答型) + 造句(看中文写意语) + 翻译(汉译意) + 全文翻译 |

### 第3步：生成音频

使用 `edge-tts` 工具，意大利女声 `it-IT-IsabellaNeural`：

```bash
pip install edge-tts
edge-tts --voice it-IT-IsabellaNeural --text "testo italiano" --write-media output.mp3
```

**需要生成的音频：**
- **单词音频**：每个单词/短语一个独立 MP3（约 9-13KB 大小）
- **段落音频**：每段课文一个独立 MP3（约 26-176KB 大小）
- **全文音频**：整篇课文朗读（约 1.4MB）

### 第4步：创建HTML页面

HTML 结构层次（必须严格按此顺序）：

```
<html>
<head>
  <style>/* 所有CSS */</style>
  <script>/* 所有JS - 必须先于body加载 */</script>
</head>
<body>
  <!-- HEADER -->
  <div class="header-bar"></div>                     <!-- 意大利三色旗顶端条 -->
  <header class="book-header">...</header>           <!-- 书名信息 -->
  <div class="unit-banner">...</div>                 <!-- 单元标题 -->
  
  <!-- 顶部课程导航 -->
  <nav class="lesson-nav top">
    <a href="index.html" class="back">← 导航页</a>
    <a href="lezione2.html" class="next">下一课 →</a>  <!-- 或 class="disabled" -->
  </nav>
  
  <!-- RIBBON NAV -->
  <nav class="ribbon-nav">...</nav>                  <!-- 章节内导航锚点 -->
  
  <!-- CONTENT -->
  <div class="content">
    <!-- 4个模块卡片 -->
    <section class="section-card" id="testo">...</section>
    <section class="section-card" id="vocabolario">...</section>
    <section class="section-card" id="note">...</section>
    <section class="section-card" id="esercizi">...</section>
  </div>
  
  <!-- 底部课程导航 -->
  <nav class="lesson-nav bottom">...</nav>
  
  <!-- FOOTER -->
  <footer class="page-footer">...</footer>
  
  <script>/* 滚动监听JS - 放body末尾 */</script>
</body>
</html>
```

#### 设计规范

- **配色**：意大利三色旗 `--ita-green: #009246`, `--ita-white: #F1F2F1`, `--ita-red: #CE2B37`, 金色点缀 `--gold: #C4A35A`
- **字体**：页面标题 `'Playfair Display', serif`，内容正文 `'Times New Roman', serif`（含课文、单词表、注释、练习），中文 `'Noto Serif SC', serif`，UI文字 `'Inter', sans-serif`
- **响应式**：768px 断点调整布局

#### 课文段落结构

每个段落必须用以下结构包裹：

```html
<div class="p-wrap">
  <span class="orig-text"><p>意大利语原文 text text...</p></span>
  <div class="trans-bar">
    <button class="para-btn" onclick="playPara(this, '0')">▶</button>
    <button class="speed-p-btn" onclick="setParaSpeed(this, 0.7)">0.7×</button>
    <button class="speed-p-btn active" onclick="setParaSpeed(this, 1.0)">1.0×</button>
    <button class="speed-p-btn" onclick="setParaSpeed(this, 1.3)">1.3×</button>
    <button class="btn-trans" onclick="toggleTrans(this, '0')">译文</button>
    <button class="btn-trans btn-orig" onclick="toggleOrig(this)">原文</button>
  </div>
  <div class="trans-box">中文翻译</div>
</div>
```

#### 对话段落特殊处理

对话（书中用 `()` 包裹）的实现：

```html
<p class="dialogue-line">
  <span class="dq">对话内容</span>
  <span class="attr">说话人说明</span>
</p>
```

#### 间距标准（重要，曾反复调试）

```
.p-wrap { margin-bottom: 0.75em; }         /* 段落间距 */
.trans-bar { margin-top: 4px; margin-bottom: 0; }  /* 按钮离正文近 */
.trans-box { margin: 0; }                   /* 译文紧贴按钮 */
.section-card.testo .section-body p { margin-bottom: 0; }  /* p标签无margin */
.section-card.testo .section-body .dialogue-line { margin-bottom: 0; }
```

### 第5步：音频系统

#### 音频文件拆分

**不要**把音频 base64 内嵌在 HTML 中。必须拆分为独立文件：

```
audio/
├── w_map.json        # 单词映射 { "单词": "audio/w/xxx.json" }
├── p_map.json        # 段落映射 { "paragraphs": { "0": "audio/p/xxx.json", ... } }
├── w/                # 单词音频文件
│   ├── YWxsb...json  # base64url编码文件名（不含=）
└── p/                # 段落音频文件
    ├── MA.json
    ├── ZnVsbA.json   # 全文朗读
    └── MjI.json      # 新增段落
```

**生成文件名规则**（用 Python 的 `base64.urlsafe_b64encode`）：
```python
def safe_filename(key):
    key_bytes = key.encode('utf-8')
    return base64.urlsafe_b64encode(key_bytes).decode('ascii').rstrip('=')
```

**JSON 文件内容格式**：
```json
// 单词文件
{"b64": "base64编码的MP3音频数据..."}

// 段落文件
{"b64": "base64编码的MP3音频数据...", "text": "该段意大利语原文文本..."}
```

**⚠️ 编码陷阱**：JSON 读写必须使用 `encoding='utf-8'`，否则带重音符号的意大利语单词（perché, là, è, ò）会在 Windows 默认 GBK 编码下损坏。

#### HTML 端加载机制

JavaScript 部分必须使用**异步 + 序列号保护**机制：

```javascript
let playSeq = 0;

// 加载音频索引
(async function() {
  const [wMap, pMap] = await Promise.all([
    fetch('audio/w_map.json'),
    fetch('audio/p_map.json')
  ]);
  AUDIO_MAP.word = await wMap.json();
  AUDIO_MAP.para = (await pMap.json()).paragraphs;
  setTimeout(startPreload, 100);
})();

// 并发预加载（6路并发）
function startPreload() {
  const allUrls = [];
  for (const key in AUDIO_MAP.word) allUrls.push(AUDIO_MAP.word[key]);
  for (const key in AUDIO_MAP.para) allUrls.push(AUDIO_MAP.para[key]);
  preloadBatch(allUrls, 6);
}
```

**三个音频类型互相打断**（使用统一 `stopAllAudio()` + 序列号保护）：

```javascript
const seq = ++playSeq;    // 每次点击递增
stopAllAudio();           // 停止所有类型
const data = await getAudioData(key);  // 异步获取
if (seq !== playSeq) return;  // 如又被点，丢弃
```

**`stopAllAudio()` 必须同时处理三种音频**：
```javascript
function stopAllAudio() {
  if (currentAudio) { currentAudio.pause(); ... }      // 单词
  if (currentParaAudio) { currentParaAudio.pause(); ... }  // 段落
  if (fullAudio) { fullAudio.pause(); ... }             // 全文
}
```

#### 获取音频数据的正确方式

⚠️ **`AUDIO_MAP.para` 是对象（Object），不是数组（Array）！**

```javascript
// ✅ 正确
fileUrl = AUDIO_MAP.para[key];           // 直接键查找
for (const key in AUDIO_MAP.para) { ... } // for...in 遍历

// ❌ 错误（会导致 TypeError，静默失败）
AUDIO_MAP.para.find(i => i.key === key);   // 对象没有 .find()
for (const item of AUDIO_MAP.para) { ... } // 对象不可迭代
```

### 第6步：部署到 GitHub

使用 GitHub API 直接推送文件到仓库。每次需要：
1. 创建 `lezioneX.html`
2. 创建 `audio/` 目录下的所有文件
3. 更新 `index.html` 导航页
4. 创建 `.nojekyll` 文件

**重要**：单个 HTML 文件很大（含音频映射），必须通过 GitHub Git Data API 的 blob/tree/commit 方式推送，不能用 `create_or_update_file`（有 1MB 限制）。

部署用 PAT token（储存在 `~/.workbuddy/MEMORY.md`）。

### 第7步：关键注意事项（踩坑记录）

1. **UTF-8 编码**：所有 JSON 文件的读写必须指定 `encoding='utf-8'`，否则带重音符号的意大利语单词会损坏
2. **段落索引同步**：每次修改段落结构（合并/拆分对话）后，必须同步更新 `p_map.json` 并重新生成或映射对应音频
3. **对话标点**：意大利语对话用 `( )` 包裹，说话人用 `—` 引出；中文翻译用 `" "` 双引号
4. **中文翻译润色**：`Ciccio` → 奇奇（音译），全文做文学化处理
5. **`trans-box` 标签**：`<div class="trans-box">` 是 23 个字符（`+23` 偏移量），不是 22
6. **`<script>` 位置**：所有播放函数（`playWord`, `playPara`, `playFullText`）必须在 `<head>` 中的第一个 `<script>` 块内定义（在 DOM 渲染之前），这样 `onclick` 才能正确引用
7. **GitHub Pages 路径**：使用相对路径 `audio/w_map.json`，不要硬编码绝对路径

### 第8步：文件结构

最终仓库结构：

```
university-italian-reading/
├── index.html                    # 导航页
├── .nojekyll                     # 禁用 Jekyll
├── lezione1.html                 # 课文页面（带所有JS/CSS）
├── audio/
│   ├── w_map.json                # 单词→文件映射
│   ├── p_map.json                # 段落→文件映射
│   ├── w/                        # 单词音频
│   │   ├── YWxsb250YW5hcnNp.json
│   │   └── ...
│   └── p/                        # 段落音频
│       ├── MA.json
│       ├── ZnVsbA.json
│       └── ...
└── README.md
```
