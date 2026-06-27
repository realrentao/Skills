---
name: "睡前意大利语1000句页面生成"
description: "生成"睡前意大利语基本口语1000句"懒加载页面（page_XXX.html + audio_XXX.js），含 edge-tts 音频生成、base64 编码、教学卡片内容创建、GitHub 上传。触发：生成page_XXX、新一批10句、睡前意大利语新页面。"
agent_created: true
---

# 睡前意大利语1000句页面生成 — 完整工作流

从 10 句文案到 GitHub 部署的端到端流程。

## 输入格式

用户以任意格式提供 10 句双语数据：

```
序号. 意大利语句子 中文翻译
```

示例：
```
1. Buonanotte! 晚安！
2. Sono furioso! 我怒不可遏！
...
10. Nevica. 下雪了。
```

## 整体流程

```
用户提供10句文案
    │
    ├─→ Step 1: 音频生成（意大利语3速 + 中文正常）
    │
    ├─→ Step 2: audio_XXX.js 生成（base64懒加载JS）
    │
    ├─→ Step 3: page_XXX.html 生成（教学卡片页面）
    │
    └─→ Step 4: GitHub 上传（Python + requests + Contents API）
```

---

## Step 1: 双语音频生成

### 1a. 意大利语音频（10句 × 3速 = 30个MP3）

使用 skill `意大利语音频批量生成`。

- **发音人**：`it-IT-IsabellaNeural`
- **三速倍率**：慢速(-30%) / 正常(0%) / 快速(+40%)
- **命名规则**：`{页面内索引_slow}.mp3` / `{页面内索引_normal}.mp3` / `{页面内索引_fast}.mp3`（如 1_slow.mp3）
- **特殊字符**：文件名只含索引编号，不嵌入意大利语句子

**关键经验**：edge-tts **不能大量并发调用**，必须**顺序执行**。并发会导致部分失败和文件锁定冲突。

### 1b. 中文音频（10句 × 1速 = 10个MP3）

使用 skill `中文女声批量生成`。

- **发音人**：`zh-CN-XiaoxiaoNeural`
- **仅正常语速**
- **命名规则**：`{页面内索引_cn}.mp3`（如 1_cn.mp3）

### 1c. 输出目录（重要）

```
D:\意大利语材料\睡前意大利语1000句\page_0XX\
├─ 1_slow.mp3    ← 意大利语慢速
├─ 1_normal.mp3  ← 意大利语正常
├─ 1_fast.mp3    ← 意大利语快速
├─ 1_cn.mp3      ← 中文正常
├─ ... (2-10同理)
```

所有MP3文件放在同一个目录（不分意大利语/中文子目录）。

**注意**：会话重启可能清空音频目录。建议同时生成 zip 备份包。

---

## Step 2: 生成 audio_XXX.js（base64 懒加载）

将 40 个 MP3（30意大利语 + 10中文）编码为 `AUDIO_DATA_XXX` JS 对象。

```python
import base64, os

AUDIO_DIR = 'D:/意大利语材料/睡前意大利语1000句/page_XXX'
OUT_PATH = 'D:/意大利语材料/睡前意大利语1000句/Base64懒加载/audio_XXX.js'

lines = ['var AUDIO_DATA_XXX = {']
for i in range(1, 11):
    for speed in ['slow', 'normal', 'fast', 'cn']:
        fname = f'{i}_{speed}.mp3'
        fpath = os.path.join(AUDIO_DIR, fname)
        with open(fpath, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
        lines.append(f'  "{i}_{speed}": "data:audio/mp3;base64,{b64}",')
lines.append('};')

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
```

生成的文件约 500-700KB，包含 40 条 base64 data URI（`"1_slow"`, `"1_normal"`, `"1_fast"`, `"1_cn"` ... `"10_cn"`）。

---

## Step 3: 生成 page_XXX.html（教学页面）

### 3a. 样式与结构

**CSS**：与 page_011 完全一致（`:root` 变量、`.sentence-card`、`.grammar-box`、`.note-box` 等）。直接从 page_011 复制 CSS 块。

**导航位置**：页面顶部和底部各一组导航按钮。

### 3b. 页面元数据

- `meta[page-id]` 改为对应页码（如 `006`）
- `title`：`边睡边记 51-60句 | ...`
- 头部文案：`第 X 页（共100页）`
- 进度条：`width: X%` 对应 `60/1000`
- PAG 编号：`PAG.06`

### 3c. 句子卡片结构（每句一个 .sentence-card）

```html
<!-- 第XX句：分类标签 -->
<div class="sentence-card" id="s51">
  <div class="sentence-header">
    <span class="sentence-number">#XX</span>
    <span class="italian-text"><em>意大利语句子</em></span>
    <div class="chinese-text">中文翻译</div>
  </div>
  <div class="audio-section">
    <span class="audio-label">🔊 发音</span>
    <div class="audio-btn-group">
      <button class="audio-btn slow" onclick="playAudio(N, 'slow')">🐢 慢速</button>
      <button class="audio-btn normal" onclick="playAudio(N, 'normal')">🎵 正常</button>
      <button class="audio-btn fast" onclick="playAudio(N, 'fast')">🚀 快速</button>
    </div>
  </div>
  
  <!-- 单词解析 -->
  <div class="detail-section">
    <div class="section-title"><span class="section-icon words">📖</span> 单词解析</div>
    <ul class="word-list">
      <li class="word-item">
        <div><span class="word-it">单词<span class="word-pos">词性</span></span></div>
        <div class="word-meaning">中文释义（词源补充）</div>
        <div class="word-extra">变位/相关词</div>
      </li>
    </ul>
  </div>
  
  <!-- 语法解析 -->
  <div class="detail-section">
    <div class="section-title"><span class="section-icon grammar">⚙️</span> 语法解析</div>
    <div class="grammar-box">
      <div class="grammar-point">
        <span class="gp-label">语法点标题</span>
        <span class="gp-text">语法解释，<strong>重点</strong>用strong，<em>例句中的词</em>用em。</span>
      </div>
      <div class="example-sent">
        📌 例句展示，可含 &lt;br&gt; 换行和多个例句
      </div>
    </div>
  </div>
  
  <!-- 实用提示 -->
  <div class="detail-section">
    <div class="section-title"><span class="section-icon note">💡</span> 实用提示</div>
    <div class="note-box">生活场景对话、文化提示、相关表达汇总</div>
  </div>
</div>
```

### 3d. 内容编写原则

**单词解析**：
- 拆解句子中每个实词，给出词性（v. / n. m. / n. f. / agg. / prep. / avv. 等）
- 不规则动词标注变位表
- 额外列标注词源、相关词汇、易混淆词

**语法解析**：
- 2个语法点，每个带 `gp-label` 标题 + `gp-text` 解释
- `example-sent` 块含 5-10 个例句，覆盖不同用法
- 关联已学句子（如"复习第33句 Ho sete"）
- 必须用 `<strong>` 标注当前句子本身

**实用提示**：
- 日常生活场景对话（A: / B: 格式）
- 文化背景知识
- 同类表达汇总
- 常见错误提示

### 3e. 播放脚本（懒加载版）

```html
<script>
let currentAudio = null;
let audioData = null;
let audioLoaded = false;

function playAudio(idx, speed) {
  if (currentAudio) { currentAudio.pause(); currentAudio = null; }
  if (!audioLoaded) {
    var s = document.createElement('script');
    s.src = 'audio_XXX.js';   // ← 改为当前页码
    s.onload = function() {
      audioLoaded = true;
      audioData = AUDIO_DATA_XXX;  // ← 改为当前页码
      var key = idx + '_' + speed;
      if (audioData[key]) {
        currentAudio = new Audio(audioData[key]);
        currentAudio.play().catch(function(e){ console.warn('播放失败:', e); });
      }
    };
    document.head.appendChild(s);
  } else {
    var key = idx + '_' + speed;
    if (audioData[key]) {
      currentAudio = new Audio(audioData[key]);
      currentAudio.play().catch(function(e){ console.warn('播放失败:', e); });
    }
  }
}
</script>
```

**关键**：`AUDIO_DATA_XXX` 和 `audio_XXX.js` 必须与当前页码一致。

---

## Step 4: GitHub 上传

### 4a. 读取 GitHub Token

Token 存储在 `~/.workbuddy/mcp.json` 中：

```python
import json
with open('C:/Users/迪丽希斯/.workbuddy/mcp.json') as f:
    config = json.load(f)
TOKEN = config['mcpServers']['github']['env']['GITHUB_PERSONAL_ACCESS_TOKEN']
```

### 4b. 使用 Python + requests 直接调用 Contents API

**为什么不用 MCP 工具**：`mcp__github__push_files` / `create_or_update_file` 对于 500KB+ 的 audio JS 文件，参数 payload 过大（520K chars），会导致参数传递失败。改用 Python + `requests` 直调 API 更为可靠。

```python
import requests, base64

OWNER = 'realrentao'
REPO = 'italiano-1000-frasi'
BRANCH = 'main'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def upload_file(path, content, message):
    """上传单个文件到 GitHub"""
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}?ref={BRANCH}'
    
    # 获取现有 SHA（如果文件存在）
    r = requests.get(url, headers=HEADERS)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    payload = {
        'message': message,
        'content': base64.b64encode(content.encode()).decode(),
        'branch': BRANCH
    }
    if sha:
        payload['sha'] = sha
    
    r = requests.put(url, json=payload, headers=HEADERS)
    return r.status_code, r.json().get('commit', {}).get('sha', '')[:8]

# 上传两个文件
upload_file('page_006.html', html_content, 'Add page_006: 句子51-60')
upload_file('audio_006.js', js_content, 'Add audio_006.js: base64 audio for 51-60')
```

### 4c. 验证部署

```
GET https://realrentao.github.io/italiano-1000-frasi/page_XXX.html → 期望 200
```

---

## 文件路径约定

| 内容 | 本地路径 | GitHub 路径 |
|------|---------|------------|
| 音频源文件 | `D:\意大利语材料\睡前意大利语1000句\page_0XX\` | 不上传 |
| audio JS | `D:\意大利语材料\睡前意大利语1000句\Base64懒加载\audio_XXX.js` | repo 根目录 `audio_XXX.js` |
| page HTML | `D:\意大利语材料\睡前意大利语1000句\Base64懒加载\page_XXX.html` | repo 根目录 `page_XXX.html` |

## 页码范围

- page_001: 1-10句
- page_002: 11-20句
- page_003: 21-30句
- page_004: 31-40句
- page_005: 41-50句
- **page_006: 51-60句**
- page_007 起依此类推...

## 经验总结

1. **edge-tts 必须顺序调用**，并发会导致文件锁定和部分失败
2. **会话重启可能清空音频目录**——解压 zip 备份即可恢复
3. **MCP GitHub 工具对 500KB+ payload 不可靠**——用 Python + requests + Contents API
4. **GitHub Token 从 mcp.json 读取**，不硬编码在 skill 中
5. **文件名中的特殊字符**：`?` → `_`，句尾标点留在文件名中
6. **HTML 直接写到本地文件再用 Read 工具读取**——避免 Write 工具里的转义问题，尤其是代码块中的 emoji 和特殊字符
