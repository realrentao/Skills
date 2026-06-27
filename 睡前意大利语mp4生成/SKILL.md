---
name: 睡前意大利语mp4生成
description: 从输入5句意大利语对话到生成竖屏1080x1920 MP4视频的完整流水线。包含edge-tts配音、GSAP动画页面、精确音画同步、Puppeteer逐帧渲染。
trigger:
  - 睡前意大利语视频
  - 意大利语mp4
  - 生成意大利语视频
  - 做一期睡前意大利语
agent_created: true
---

# 睡前意大利语 MP4 生成流水线

## 概述

从用户输入的 5 句意大利语对话文本，自动完成：
1. edge-tts 配音（意语原速 → 中文翻译 → 意语慢速，每句三段）
2. GSAP 动画页面（1080×1920 竖屏，夜空主题）
3. 精确音画同步音频合成
4. Puppeteer 逐帧渲染 + FFmpeg 编码 MP4

## 依赖

- Python 3.x + `edge-tts` + `pydub`
- Node.js 22.x + `puppeteer-core`
- FFmpeg（系统 PATH 中可用）
- Edge 浏览器（Windows: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`）

## Step 1: 创建项目结构

```bash
mkdir -p project_dir/media project_dir/temp_segments
```

## Step 2: 生成 segment_info.json

格式为 15 段（5句 × 3段），参考 `references/segment_info_example.json`：

```json
[
  [1, "句1意语常速", "Lieto di conoscerti.", 2.5, "it_female", 1.0],
  [2, "句1中文", "很高兴认识你。（男性说）", 2.5, "cn_female", 1.0],
  [3, "句1意语慢速", "Lieto di conoscerti.", 4.0, "it_female", 0.68],
  ...
]
```

每行 6 个字段：`[序号, 描述, 文本, 估计时长, 语音key, 语速]`

- 语音 key: `it_female` = ElsaNeural, `cn_female` = XiaoxiaoNeural
- 语速: `1.0` = 正常, `0.68` = -32% 慢速
- 估计时长用于预估，实际时长由 pydub 测量

## Step 3: 运行配音流水线

```bash
cd project_dir && python dub_pipeline.py
```

脚本参考: `references/dub_pipeline.py`

输出：
- `media/seg_0000.mp3` ~ `media/seg_0014.mp3`（15 个分段）
- `timing.json`（每段实际时长，单位秒）
- `buonanotte_completa.mp3`（粗合成音频，仅用于预览，**不用于视频**）

**关键：** monkey-patch `xml:lang` 防止意大利语发音变英语口音。

## Step 4: 构建 index.html

基于 `references/index_template.html` 修改：

### 替换内容部分
- 卡片文本：将 5 句意大利语和中文翻译替换到 `.card` 元素中
- 音频路径：确认 `media/seg_XXXX.mp3` 路径正确

### 替换时序部分（关键！）
从 `timing.json` 读取实际时长，硬编码到 `DURATIONS` 数组：

```javascript
const DURATIONS = [
  1.800, 3.312, 2.640,  // 句1: 意快, 中文, 意慢
  1.176, 1.440, 1.704,  // 句2
  ...
];
```

### 时间间隔参数
```javascript
const GAP = 0.3;          // 同一句话内的段间隔
const GAP_SENTENCE = 2.0; // 句子之间的间隔（留出呼吸时间）
const INTRO_DUR = 2.0;    // 开场动画时长
```

### 渲染兼容函数（必须保留！）
页面必须暴露以下函数供渲染脚本调用：

```javascript
window.resetHighlights = function() { ... };     // 清除所有高亮
window.computeHighlight = function(t) { ... };   // 根据时间计算该高亮哪句
window.highlightFn = highlight;                    // 高亮函数引用
window.totalDuration = progressEnd + 2.0;         // 视频总时长
window.__timelines['root'] = tl;                  // GSAP timeline 注册
```

### 品牌名
根据需要修改 `.brand` 区域的内容和 logo 路径。

### 音频播放方式
- 使用 `<audio>` 元素 + `preload="auto"`
- **不要用 AudioContext/fetch/decodeAudioData**，file:// 协议下跨域限制会静音
- 加 `preloadAll()` 等待所有音频 `canplaythrough` 后启动 timeline

## Step 5: 精确音画同步音频合成

```bash
cd project_dir && python resync_audio.py
```

脚本参考: `references/resync_audio.py`

这步会生成 `buonanotte_completa.mp3`，覆盖 Step 3 的粗合成版本。
音频时间轴与 HTML GSAP timeline **完全一致**：
- 开头 2.0s 静音（对应开场动画）
- 句内 0.3s 间隔，句间 2.0s 间隔
- 末尾额外静音确保覆盖视频淡出

## Step 6: 渲染 MP4

```bash
cd project_dir && node render_vertical.js index.html output.mp4 --fps 15 --audio buonanotte_completa.mp3
```

脚本参考: `references/render_vertical.js`

参数：
- `--fps 15`（推荐 15，平衡速度和质量）
- `--audio` 指向 Step 5 生成的精确同步音频

渲染流程：
1. Puppeteer 启动 Edge headless
2. 加载页面 → **立即暂停 timeline**（防 seek 回溯错乱）
3. 逐帧：`pause() → seek(0) → seek(t)` → `resetHighlights()` → `computeHighlight(t)` → 截图
4. FFmpeg 编码 H.264 + AAC

预计耗时：~2 分钟（30-40 秒视频）

## 关键踩坑记录

### 1. 音画不同步
- **原因**：粗合成音频间隔（300ms）与 HTML 间隔（句间 2.0s）不匹配
- **修复**：必须运行 `resync_audio.py` 按 HTML 时间轴精确合成

### 2. HTML 无声音
- **原因**：AudioContext + fetch 在 file:// 协议下有跨域限制
- **修复**：改回 `<audio>` 元素 + `preload="auto"`

### 3. 渲染开头卡顿
- **原因**：页面加载后 `tl.play()` 自动播放了 3-4 秒，seek(0) 回溯导致动画错乱
- **修复**：加载后立即 `tl.pause()`，等待从 4s 缩短到 0.8s

### 4. 渲染高亮错乱
- **原因**：GSAP `seek()` 不会可靠触发 `tl.call()` 回调
- **修复**：渲染时用 `computeHighlight(t)` 直接计算，不依赖回调

### 5. FFmpeg -itsoffset
- **不要加 `-itsoffset`**！音频已内含开场静音，加 offset 反而不同步
- **不要加 `-shortest`**！会截断画面

## 文件清单

```
project_dir/
├── segment_info.json       # 输入：15段配音定义
├── dub_pipeline.py         # Step 3: edge-tts 配音
├── timing.json             # Step 3 输出：实际时长
├── index.html              # Step 4: GSAP 动画页面
├── resync_audio.py         # Step 5: 精确音频合成
├── render_vertical.js      # Step 6: Puppeteer 渲染
├── buonanotte_completa.mp3 # Step 5 输出：同步音频
├── output.mp4              # Step 6 输出：最终视频
├── media/                  # 15 个分段音频
└── temp_segments/          # 临时文件
```

## 参考脚本

所有脚本的最新版本在 `references/` 目录下：
- `references/dub_pipeline.py`
- `references/resync_audio.py`
- `references/render_vertical.js`
- `references/index_template.html`
- `references/segment_info_example.json`
