---
name: nuovo-espresso
description: 从 Nuovo Espresso 1 / DIECI A1 意大利语教材 PDF 或 Markdown 创建交互式 HTML 网页课程。包含完整流水线：提取教材内容 → 设计交互页面（词汇发音、语法表格、对话音频、选择题测验）→ 纯 CSS 国旗 → 音频系统（edge-tts 意大利女声 + base64 独立文件 + fetch 动态加载 + 打断机制）→ 部署到 GitHub Pages。当用户说"做意大利语课程"、"做成交互式HTML"、"参考xxx做成HTML"时触发。
agent_created: true
---

# Nuovo Espresso / DIECI A1 交互式意大利语课程构建 Skill

## 概述

本 Skill 定义了从意大利语教材 PDF/Markdown 到可部署的交互式 HTML 网页课程的完整工作流。覆盖教材内容提取、交互设计、音频生成、CSS 国旗、部署等全流程。

## 触发词

- "把XX教材做成交互式HTML"
- "做意大利语课程网页"
- "参考XX设计做成交互式"
- "意大利语学习页面"
- "nuovo espresso" / "dieci A1" 课程制作

## 核心工作流

### 阶段一：内容提取与项目初始化

1. **读取教材内容**
   - 从 IMA 知识库提取 PDF（使用 `mcp__ima-mcp__fetch_media_content`）
   - 或从本地 Markdown 文件读取（`Read` 工具）
   - 或直接从 PDF 文件使用 PyMuPDF (`fitz`) 提取文本

2. **分析课程结构**
   - 确定单元数量（通常 10 单元）
   - 每单元的章节划分：词汇、语法、对话、练习
   - 文化板块（Caffè culturale）

3. **创建项目目录结构**
   ```
   project-name/
   ├── index.html              ← 课程主页
   ├── unita-1.html ~ 10.html  ← 各单元页面
   ├── css/
   │   └── ne-styles.css       ← 样式文件
   ├── js/
   │   └── ne-audio-player.js  ← 音频播放器（可选）
   └── audio/
       ├── ne-audio-data.js    ← 音频 manifest + 加载器
       └── d/                  ← 独立 base64 音频文件（按需加载）
   ```

### 阶段二：HTML 页面设计

#### 2.1 课程主页 (index.html)
- Hero 区域：课程标题 + 说明
- 统计数字：单元数、词汇数等
- 10 个单元卡片网格，每张卡片包含：编号、名称、emoji、简介
- 课程结构说明

#### 2.2 单元页面 (unita-1.html ~ 10.html)
**每页必须包含：**

**头部结构：**
- `<!DOCTYPE html>` + `<html lang="zh-CN">`
- `<head>` 内引入 CSS、音频 manifest、音频播放器 JS
- `<body>` 内顶栏导航 + 滚动进度条

**内容区按页码 (PAG.) 分节：**
- 词汇卡片：使用 `.vocab-card` + 点击发音 (`onclick="speak('word')"`)
- 语法表格：使用 `.grammar-table` 或 `.grammar-pair`（响应式）
- 对话框：使用 `.source-box` + `.item` + `.badge` + `.ds-text` + `onclick="speak()"`
- Caffè culturale：金色左边框分隔，时间划分卡，点击发音
- 测验题：`.quiz-question` + `.quiz-option` + `cq()` 重试机制

**页面尾部：**
- 上下单元导航按钮
- `<script>` 含滚动进度条 + cq 函数

### 阶段三：音频系统

#### 3.1 音频生成
使用 `edge-tts` 意大利女声 (`it-IT-IsabellaNeural`) 生成所有词汇/短语的 MP3：

```python
proc = await asyncio.create_subprocess_exec(
    "edge-tts", "--voice", "it-IT-IsabellaNeural",
    "--text", word, "--write-media", mp3_path
)
```

#### 3.2 base64 文件转换
每个 MP3 转为独立 JS 文件，包含 base64 数据：

```js
// audio/d/a.js
const AD_a = "data:audio/mp3;base64,...";
```

#### 3.3 音频 Manifest (ne-audio-data.js)
包含两部分：
- `AUDIO_KEYS`：单词 → 文件名映射（96+ 条）
- `speak()` 函数：fetch 动态加载 + 缓存 + 打断机制

```js
function speak(text) {
  stopAllAudio();
  var key = AUDIO_KEYS[text] || AUDIO_KEYS[text.toLowerCase()];
  // 已缓存 → 直接播放
  // fetch 加载 audio/d/xxx.js → 提取 base64 → 播放
  // fetch 失败 → fallback Web Speech API
}
function stopAllAudio() {
  // 暂停 currentAudio
  // speechSynthesis.cancel()
}
```

### 阶段四：CSS 设计与组件

#### 4.1 配色系统
- `--ne-red`: #C0392B
- `--ne-orange`: #E67E22
- `--ne-gold`: #F39C12
- `--ne-blue`: #1A5276
- `--ne-cream`: #FEF9E7
- `--ne-bg`: #FDFCFB

#### 4.2 关键组件
- `.vocab-card`：词汇卡片（可点击发音）
- `.interactive-block`：交互块容器
- `.source-box`：原文展示块（金色左边框）
- `.exercise-card`：练习题卡片（蓝色标签）
- `.grammar-table`：语法表格
- `.grammar-pair`：响应式并排语法（桌面 1fr 1fr → 手机 1fr）
- `.highlight-word`：高亮可点击词汇
- `.ds-text`：可点击对话文字（虚线下划线）
- `.quiz-question` / `.quiz-option`：测验题
- `.comm-box`：实用表达框
- `.wrong` / `.correct`：测验选项状态

#### 4.3 纯 CSS 国旗
所有国旗用 CSS 渐变实现（不使用 emoji），确保各平台一致性：

```css
.flag-it { background: linear-gradient(90deg, #009246 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #CE2B37 66.66%); }
.flag-de { background: linear-gradient(90deg, #000 33.33%, #DD0000 33.33%, #DD0000 66.66%, #FFCE00 66.66%); }
.flag-fr { background: linear-gradient(90deg, #002395 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #ED2939 66.66%); }
.flag-es { background: linear-gradient(180deg, #AA151B 25%, #F1BF00 25%, #F1BF00 75%, #AA151B 75%); }
.flag-gb { background: #012169; overflow:hidden; /* 多层 linear-gradient 叠加出米字交叉线 */ }
.flag-pt { background: linear-gradient(90deg, #006600 40%, #FF0000 40%); /* + ::after 金色圆形 */ }
.flag-at { background: linear-gradient(90deg, #ED2939 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #ED2939 66.66%); }
.flag-ch { background: #FF0000; background-image: /* 白十字 */; }
.flag-ie { background: linear-gradient(90deg, #169B62 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #FF883E 66.66%); }
.flag-ru { background: linear-gradient(180deg, #FFF 33.33%, #0039A6 33.33%, #0039A6 66.66%, #D52B1E 66.66%); }
.flag-cn { background: #DE2910; /* ::before 大星 ★ , ::after 小星 text-shadow */ }
.flag-us { background: repeating-linear-gradient(#B22234 0px, #B22234 .166em, #FFF .166em, #FFF .332em); /* ::after 蓝色 canton */ }
.flag-emoji { display:inline-block; width:1.2em; height:1em; vertical-align:-0.15em; 意大利三色渐变 }
```

每个国旗尺寸为 `width: 1.2em; height: 1em;`，带 `box-shadow: 0 1px 2px rgba(0,0,0,0.12)`。

### 阶段五：测验系统

#### cq() 函数
```js
function cq(el, c) {
  // 清除所有选项的错误状态 + 解除锁定
  // 清除之前的反馈文字
  // 如果正确 → 锁定所有选项 + ✅
  // 如果错误 → 红色高亮 + ❌ 再想想（可继续尝试）
}
```

### 阶段六：部署

#### 6.1 GitHub 仓库
```bash
git init && git add . && git commit -m "Initial commit"
gh repo create nuovo-espresso --public --push
```

#### 6.2 GitHub Pages 部署
- 创建 `.github/workflows/deploy.yml`
- 添加 `.nojekyll` 文件（确保 `audio/d/` 目录不被忽略）
- 在仓库 Settings → Pages → Source: GitHub Actions

#### 6.3 API 推送（git 不通时）
使用 GitHub API 配合 token 直接推送：
```python
urllib.request.Request('https://api.github.com/.../contents/file.html', method='PUT')
```

## 常见问题处理

### 音频不发音
1. 检查 `AUDIO_KEYS` 映射表是否包含该词
2. 检查 `audio/d/xxx.js` 文件是否存在
3. 检查文件引用的路径（`audio/d/` + key + `.js`）
4. 检查 manifest 中的文件名和实际文件名是否匹配（注意 sanitize 规则差异）

### 页面空白
1. 检查 `<script>` 标签是否闭合（最常见 bug！）
2. 检查 `</style>`, `</head>`, `<body>` 是否缺失

### Git 推送失败
- 网络不通时改用 `mcp__github__push_files` 或 GitHub API + token 推送
- MCP 工具有文件大小限制（~18KB），大文件需用 GitHub API 直接推送

### 国旗显示异常
- 改用纯 CSS（linear-gradient / Unicode 字符 / clip-path）
- 不使用 emoji 以确保跨平台一致性
- 小尺寸时简化设计（如美国旗省略 50 颗星）
