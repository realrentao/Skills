---
name: italian-bedtime-video
description: >
  生成每日睡前意大利语学习视频页面。使用 edge-tts 生成中意双语女声音频，
  构建 HyperFrames 1080×1920 竖屏视频页面，5句对话同时显示，当前句高亮。
  当用户要求做"睡前意大利语"、"每日意大利语视频"、"意大利语学习视频"时触发。
  默认输出MP4视频，1080p超清，30fps。
agent_created: true
---

# 睡前意大利语学习视频页面

生成一个竖屏 1080×1920 的睡前意大利语学习视频 HyperFrames 页面，并输出 MP4。

## 视频输出规格（默认）

| 参数 | 值 |
|------|-----|
| 分辨率 | 1080×1920 竖屏 |
| 帧率 | 30fps（超清） |
| 编码 | H.264 + AAC |
| CRF | 18（近无损） |
| 像素格式 | yuv420p, tv range |
| 渲染 | rendercustom.js（CK=300, quality=80） |
| 输出命名 | buonanotte.mp4 |

## 输入

5 句意大利语对话，每句结构：`"意大利语. 中文翻译。"`

## 步骤

### Step 1: 生成分段定义 JSON

在项目目录下创建 `segment_info.json`。每句生成 3 个片段：

| 序号 | 内容 | 语音 | 速度 | 说明 |
|------|------|------|------|------|
| N×3-2 | 意大利语原文 | `it_female` (it-IT-ElsaNeural) | 1.0 | 常速朗读 |
| N×3-1 | 中文翻译 | `cn_female` (zh-CN-XiaoxiaoNeural) | 1.0 | 常速朗读 |
| N×3 | 意大利语原文 | `it_female` (it-IT-ElsaNeural) | 0.68 | 慢速跟读 |

语音映射：
```python
VOICES = {
    'cn_female': 'zh-CN-XiaoxiaoNeural',
    'it_female': 'it-IT-ElsaNeural'
}
SPEED_TO_RATE = {1.0: "+0%", 0.68: "-32%"}
```

### Step 2: 生成音频

使用 edge-tts 配合 xml:lang monkey-patch 生成 15 段音频（5句×3段）。

关键代码 — monkey-patch（必须在 Communicate 之前执行）：
```python
import edge_tts.communicate
_orig = edge_tts.communicate.mkssml
def patched(tc, escaped_text):
    r = _orig(tc, escaped_text)
    if 'it-IT' in tc.voice:
        r = r.replace("xml:lang='en-US'", "xml:lang='it-IT'")
    elif 'zh-CN' in tc.voice:
        r = r.replace("xml:lang='en-US'", "xml:lang='zh-CN'")
    return r
edge_tts.communicate.mkssml = patched
```

音频间隔：300ms。采样率：44100Hz。比特率：192kbps。

### Step 2.5: 合并音轨 & 复制资源

**音画同步关键：** 渲染用 assets/index.mp3 必须**在开头垫 2.0s 静音**以匹配 GSAP 的 INTRO_DUR（否则视频播放时前2秒字幕动画会提前出现首句语音）。末尾也需垫足量静音覆盖视频尾部。

将 15 段音频按正确时序拼接为单轨（含 0.3s 静音间隔 + 前垫2.0s + 后垫4.0s）：
```bash
cd NN期
mkdir -p assets
python3 -c "
import subprocess, os
MEDIA = 'media'
files = [f'seg_{i:04d}.mp3' for i in range(15)]
gap_len = 0.3; intro_silence = 2.0; outro_silence = 4.0
cmd = ['ffmpeg', '-y']
# front silence
cmd.extend(['-f', 'lavfi', '-t', str(intro_silence), '-i', 'anullsrc=r=44100:cl=mono'])
# 15 audio segments
for f in files:
    cmd.extend(['-i', os.path.join(MEDIA, f)])
# 14 intra-gap silences
for i in range(14):
    cmd.extend(['-f', 'lavfi', '-t', str(gap_len), '-i', 'anullsrc=r=44100:cl=mono'])
# trailing silence
cmd.extend(['-f', 'lavfi', '-t', str(outro_silence), '-i', 'anullsrc=r=44100:cl=mono'])
# concat: front[0] + segs[1..15] + gaps[16..29] + outro[30] = 31 inputs
concat = '[0:a]'
for i in range(15):
    concat += f'[{1+i}:a]'
    if i < 14:
        concat += f'[{16+i}:a]'
concat += '[30:a]'
cmd.extend(['-filter_complex', f'{concat}concat=n=31:v=0:a=1',
    '-acodec', 'libmp3lame', '-b:a', '192k', 'assets/index.mp3'])
subprocess.run(cmd, check=True)
"
```

同时复制 logo-piano.jpg：
```bash
# 从上一期复制
cp ../36期/media/logo-piano.jpg media/
```

### Step 3: 构建 HyperFrames 页面

创建 `index.html`，竖屏 1080×1920，要求：

**设计规范：**
- 深蓝夜空渐变背景（#0a0e27 → #141845 → #1a1050 → #0d0a2a）
- 意大利元素：三色条纹（绿/白/红）、"ITALIA" 水印字、金色月光
- 散落星光点缀
- 字体：'Georgia' 用于意大利语，'PingFang SC'/'Microsoft YaHei' 用于中文

**页面布局：**
- 顶部标题："Buonanotte" (金色 italic, 72px) + "睡前意大利语" (浅色, 26px)
- 中部 5 张句子卡片，等间距排列
- 每张卡片包含：意大利语 (44px, 暖色) + 中文翻译 (22px, 浅色)
- 底部进度条、页码标记

**CSS 防抖规则：**
- 卡片 `.card` **必须**移除 `backdrop-filter`（GPU 模糊导致渲染抖动）：
  ```css
  /* ❌ 不要加 backdrop-filter: blur(10px) */
  .card { ... backdrop-filter: blur(10px); }  // 删掉
  ```
- 卡片和分页点**必须**移除 CSS `transition`（15fps 渲染时过渡动画导致半高亮抖动）：
  ```css
  /* ❌ 不要加 transition */
  .card { ... transition: ... }  // 删掉
  .dot { ... transition: ... }   // 删掉
  ```
- 卡片添加 `will-change: transform, opacity` 提示 GPU 独立合成：
  ```css
  .card { will-change: transform, opacity; }
  ```

**动画时序（关键！音频生成后才可确定）：**
- ⚠️ 先跑音频流水线，从 timing.json 获取实际时长，再写入 HTML
- **统一使用 GAP=0.3s（句内句间均为 0.3s，与 dub_pipeline.py 一致）**，不使用 GAP_SENTENCE=2.0
- 开头 INTRO_DUR=2.0s 静音：标题淡入(0.8s) + 卡片交错入场(stagger 0.06s, 从 0.8s 开始)
- ⚡ **高亮不依赖 GSAP callback**，用独立的 `window.renderTick(timelineTime)` 函数直接计算
- 进度条：全程匀速 `tl.to('#progressBar', {width: '100%', duration: ...}, INTRO_DUR)`
- 结尾：全部完成后 0.5s 淡出(1.5s)
- 根元素添加 `data-duration` 属性（向上取整秒数）

**视觉效果（CSS 动画，独立于 GSAP 运行）：**
- 🌙 **月亮呼吸发光**：用 `.moon-wrapper` 包裹月亮 + 独立的 `.moon-glow` 发光层，避免 GSAP inline style 冲突：
  ```html
  <div class="moon-wrapper">
    <div class="moon-glow"></div>
    <div id="moon" class="moon">...</div>
  </div>
  ```
  ```css
  .moon-wrapper { position:absolute; top:230px; right:160px; width:120px; height:120px; }
  .moon-glow {
    position:absolute; top:50%; left:50%;
    width:500px; height:500px; margin:-250px 0 0 -250px;
    border-radius:50%;
    background:radial-gradient(circle,rgba(212,168,67,0.25) 0%,rgba(212,168,67,0.12) 20%,rgba(212,168,67,0.05) 40%,transparent 60%);
    pointer-events:none;
    animation:moonGlowPulse 25s ease-in-out infinite;
  }
  @keyframes moonGlowPulse {
    0%, 100% { opacity:0.2; transform:scale(0.6); }
    50%      { opacity:0.6; transform:scale(1.8); }
  }
  .moon { position:absolute; top:0; left:0; width:120px; height:120px; border-radius:50%; ...; opacity:0; }
  ```
- 🏷️ **品牌跑马灯**：`.brand` 添加缓慢明暗脉动（周期 40s）：
  ```css
  @keyframes brandMarquee {
    0%   { color:rgba(255,255,255,0.08); filter:brightness(0.5); }
    25%  { color:rgba(212,168,67,0.5); filter:brightness(1.2); text-shadow:0 0 30px rgba(212,168,67,0.3); }
    50%  { color:rgba(255,255,255,0.10); filter:brightness(0.6); }
    75%  { color:rgba(212,168,67,0.4); filter:brightness(1.0); text-shadow:0 0 20px rgba(212,168,67,0.2); }
    100% { color:rgba(255,255,255,0.08); filter:brightness(0.5); }
  }
  .brand { animation:brandMarquee 40s ease-in-out infinite; }
  ```
- 🟫 **暖光灯带边框**：叠加 `.glow-border` 层在 `#root` 最底部，z-index:200：
  ```css
  @keyframes borderPulse {
    0%, 100% { box-shadow:inset 0 0 40px 10px rgba(212,168,67,0.1), inset 0 0 80px 20px rgba(212,168,67,0.05); border-color:rgba(212,168,67,0.05); }
    50%      { box-shadow:inset 0 0 60px 20px rgba(212,168,67,0.25), inset 0 0 120px 30px rgba(212,168,67,0.12), 0 0 40px 10px rgba(212,168,67,0.08); border-color:rgba(212,168,67,0.2); }
  }
  .glow-border { position:absolute; top:0; left:0; width:1080px; height:1920px; pointer-events:none; z-index:200; border:3px solid rgba(212,168,67,0.05); border-radius:4px; animation:borderPulse 30s ease-in-out infinite; }
  ```
  ⚠️ 所有 CSS 动画周期设为 **25s/40s/30s**（缓慢闪烁，原频率的 1/5），避免在视频中产生视觉干扰。

**音频元素：**
- 15 个 `<audio>` 标签，id="audio-{idx}" (idx 0-14)
- 音频文件放在 `media/` 子目录（格式 seg_{idx:04d}.mp3）

**GSAP 规则：**
- timeline `{ paused: true }`，全局暴露 `window.tl = tl`
- **不注册** `window.__timelines`（避免 render 脚本双重 seek）
- GSAP timeline 只做视觉动画（opacity、transform 过渡）和音频播放控制
- 高亮完全由 `renderTick` 独立控制
- **注册 onUpdate 事件**，确保预览模式（`tl.play()`）也每帧触发 renderTick：
  ```javascript
  tl.eventCallback("onUpdate", function() {
    window.renderTick(tl.time());
  });
  ```
  ⚠️ `eventCallback` 注册必须在 `window.renderTick` 赋值之前或之后都行，onUpdate 在播放/seek 时才触发，那时 renderTick 已经就位。

**renderTick 函数（必须在 window 对象上暴露）：**
```javascript
window.renderTick = function(timelineTime) {
  var audioTime = timelineTime - INTRO_DUR;
  var sentIdx = -1;
  if (audioTime >= 0) {
    for (var i = segments.length - 1; i >= 0; i--) {
      if (audioTime >= segments[i].start) { sentIdx = segments[i].sentIdx; break; }
    }
  }
  // 状态缓存：sentIdx 没变则跳过 DOM 操作（避免冗余重绘）
  if (sentIdx === window.__lastSent) return;
  window.__lastSent = sentIdx;

  var cards = document.querySelectorAll('.card');
  var dots = document.querySelectorAll('.dot');
  cards.forEach(function(c) { c.classList.remove('active', 'done'); });
  dots.forEach(function(d) { d.classList.remove('active', 'done'); });

  if (sentIdx >= 0 && sentIdx < SENTENCES) {
    cards.forEach(function(c,i) { if (i < sentIdx) c.classList.add('done'); });
    dots.forEach(function(d,i) { if (i < sentIdx) d.classList.add('done'); });
    cards[sentIdx].classList.add('active');
    dots[sentIdx].classList.add('active');
  } else if (sentIdx >= SENTENCES) {
    cards.forEach(function(c) { c.classList.remove('active'); c.classList.add('done'); });
    dots.forEach(function(d) { d.classList.remove('active'); d.classList.add('done'); });
  }
  document.getElementById('progressText').textContent =
    sentIdx >= SENTENCES ? '5 / 5' : (sentIdx < 0 ? '0 / 5' : (sentIdx + 1) + ' / 5');
};
```

**自动播放控制（支持渲染模式）：**
```javascript
if (window.__renderOnly) {
  window.renderTick(0);   // 渲染模式：不自动播放，由 render 脚本 seek 控制
} else {
  preloadAll().then(function() { tl.play(); });
}
```

**时序计算方式（推荐硬编码）：**
1. 运行 dub_pipeline.py 生成音频
2. 从生成的 timing.json 读取实际时长（秒）
3. 将这些时长硬编码为 JS 数组 DURATIONS = [...]
4. 遍历构建 segments 数组：起点累加(cursor += duration + GAP)
5. 每段：`tl.call(playAudio(idx), [], INTRO_DUR + seg.start)`
6. 每段结束：`tl.call(stopAudio(idx), [], INTRO_DUR + seg.start + seg.duration)`
7. ❌ **不在 GSAP timeline 中添加 highlight callback**，高亮由 renderTick 处理
8. 避免依赖 loadedmetadata（不同浏览器行为不一致）

**渲染脚本修改点（如果使用 html-to-mp4-render script）：**

⚠️ **必须使用不使用 `seek(0)` 重置的独立渲染脚本**，否则每帧卡片入场动画重跑导致高亮过渡回弹。

1. 将 `render_v8.js` 复制为 `rendercustom.js`，修改以下关键点：
   - ❌ 移除 `tl.seek(0)` 和 `timelines` 的双重 seek
   - ❌ 移除 `window.__timelines` 的遍历（本项目不注册 `__timelines`）
   - ✅ 只做 `tl.seek(seekTime)` 直接跳转
   - ✅ 后面调用 `window.renderTick(seekTime)`
   - ✅ 在 `page.goto()` 之前用 `evaluateOnNewDocument` 设 `__renderOnly=true`
   - ✅ 高帧率渲染（30fps）时：`CHUNK_SIZE=300`（默认500，30fps时改小防内存溢出）
   - ✅ 截图 quality=80（平衡质量与速度）

   ```javascript
   // 在 page.setViewport 之后、page.goto 之前：
   await page.evaluateOnNewDocument(() => { window.__renderOnly = true; });

   // 每帧的 evaluate 块（rendercustom.js 中的核心修改）：
   await page.evaluate((seekTime) => {
     const tl = window.tl;
     if (tl) { tl.seek(seekTime); }
     if (typeof window.renderTick === 'function') {
       window.renderTick(seekTime);
     }
   }, t);
   ```

2. 渲染命令示例（15fps 常规 / 30fps 超清）：
   ```bash
   # 使用 managed Node.js
   "C:\Users\迪丽希斯\.workbuddy\binaries\node\versions\22.22.2\node.exe" rendercustom.js index.html buonanotte.mp4 --fps 15 --width 1080 --height 1920
   "C:\Users\迪丽希斯\.workbuddy\binaries\node\versions\22.22.2\node.exe" rendercustom.js index.html buonanotte.mp4 --fps 30 --width 1080 --height 1920  # 30fps 超清
   ```

### Step 4: 验证

**项目优先**：如果项目已用 `npx hyperframes init` 初始化，可运行：
```
cd project && npx hyperframes lint
```
修复 warnings：去除 Google Fonts 外部链接、用 `id="root"` 替代 `[data-composition-id="root"]`、避免 GSAP tween 重叠。

**纯 HTML 页面**：直接打开 index.html 预览，检查：
- 所有音频能否正常加载播放（浏览器控制台检查 404）
- 高亮切换时序是否正确
- 进度条是否匀速前进
- 总时长是否与预期一致

**音画同步检查（输出MP4后）：**
- 前2秒（标题动画）是否为静音 → 若有语音出现说明 assets/index.mp3 缺少 2.0s 前垫静音
- 每句高亮切换时语音是否同步 → 核对 timing.json 的 start 时间与 JS 中 D[] 计算的 sg[i].start 是否一致
- 视频结尾是否有完整的 fadeout 且无音频截断 → assets/index.mp3 后垫静音需足够长

## 项目文件结构

```
project-name/
├── index.html              # HyperFrames 视频页面
├── segment_info.json       # 音频分段定义
├── dub_pipeline.py         # 配音流水线脚本
├── timing.json             # 音频实际时长
├── media/                  # 音频文件
│   ├── seg_0000.mp3
│   ├── ...
│   └── logo-piano.jpg
├── assets/                 # 合并音轨（渲染用）
│   └── index.mp3
└── temp_segments/          # 临时音频（可删除）
    └── ...
```
