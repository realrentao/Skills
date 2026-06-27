---
name: 大学意大利语阅读01
description: >
  第一课 L'ombrello di Ciccio — 从扫描版PDF提取内容，生成完整交互式HTML教学页面。
  包含四模块（课文Testo、单词表Vocabolario、注释Note、练习Esercizi），
  段落级/单词级edge-tts音频播放，中文译文，交互式练习，语速控制。
  使用 edge-tts it-IT-IsabellaNeural 意大利女声生成全部音频，
  拆分独立JSON文件并行加载。支持GitHub Pages部署。
agent_created: true
---

# 大学意大利语阅读教程 01 — 第一课 L'ombrello di Ciccio

## 触发词
"大学意大利语阅读01"、"第一课"、"L'ombrello di Ciccio"、"lezione1"

## 课文数据
- **课文标题**: L'ombrello di Ciccio（奇奇的雨伞）
- **段落数**: 25段
- **单词数**: 18个词汇
- **注释数**: 16条
- **练习**:
  - Ex1: 10道阅读理解问答
  - Ex2: 20个词语造句
  - Ex3: 9句汉译意（文本框+关键词匹配检查）
  - Ex4: 全文中文翻译（折叠展开）

## 完整构建流程

### 1. 提取课文内容
**扫描版PDF（无文字层）:**
- 用 PyMuPDF (fitz) 将PDF关键页转为PNG（Matrix 1.5x）
- 用 tesseract.js OCR，语言 ita+chi_sim
- 从目录确认 Unità 1 Testo 1
- 逐页提取课文正文、词汇表、注释、练习

### 2. 构建HTML页面
**结构：**
- 4个 section-card：testo / vocab / note / esercizi
- 商务风UI + 意大利国旗绿白红元素
- Playfair Display（意语）+ Noto Serif SC（中文）双字体
- 响应式布局，粘性导航锚点
- 对话标点: 书名号«» → 括号()
- 说话人+对话内容同行

**交互式练习：**
- Ex1: 每题"答案"按钮 → 正下方展示参考答案
- Ex2: 点击词语查看例句
- Ex3: 输入框 + "检查"按钮 → 基于关键词匹配判定
- Ex4: "显示参考译文"折叠展开

### 3. 生成音频
**TTS引擎**: `edge-tts --voice it-IT-IsabellaNeural`
**段落音频**: 25段独立音频 + 全文音频
**单词音频**: 18个词汇 + 16条注释 = 34个独立音频

**音频文件命名**: base64编码（无填充`=`），参考 `audio/w/` 和 `audio/p/`

**音频JSON格式:**
```json
{"b64": "<base64_encoded_mp3>", "text": "<原文文本>"}
```

**索引文件:**
- `audio/w_map.json` — 单词路径映射（扁平结构，key=词，value=路径）
- `audio/p_map.json` — 段落路径映射（含 "full" 全文）

### 4. HTML音频系统
- 先加载 w_map.json / p_map.json
- 6路并发后台预加载所有音频
- 点击即时播放，若未加载完成则按需 fetch
- `playWord(btn)` — 单词播放（读取 data-word）
- `playPara(btn, idx)` — 段落播放
- `playFullText()` — 全文播放
- 播放按钮变红脉冲动画，自动停止上一个音频
- 异步函数 + 序列号防竞态（stale async fetch guard）

### 5. 部署至GitHub Pages
```python
# 使用 GitHub Git Data API 推文件
# 1. GET git/refs/heads/main → 获取HEAD SHA
# 2. POST git/blobs → 创建每个文件的blob
# 3. POST git/trees → 创建目录树
# 4. POST git/commits → 创建提交
# 5. PATCH git/refs/heads/main → 更新分支

# 注意：大文件（base64音频JSON）用Git Data API
# 小文件可 PUT /repos/{owner}/{repo}/contents/{path}
```

## 关键陷阱
- **OCR编码**: tesseract.js 输出需 UTF-8 编码
- **音频JSON格式**: `data.b64` 不是 `data.audio`
- **trans-box 23字符偏移**: 中文译文框偏移量是23个字符
- **序列号防竞态**: 异步fetch使用递增序列号 guard 防止过时数据
- **base64补丁**: 文件名不含 `=` 填充
- **全局变量冲突**: 不同播放函数使用独立的 state 变量

## 参考文件
- `lezione1.html` — 完整HTML页面
- `audio/w_map.json` — 单词音频索引
- `audio/p_map.json` — 段落音频索引
- `audio/w/*.json` — 单词音频文件
- `audio/p/*.json` — 段落音频文件
