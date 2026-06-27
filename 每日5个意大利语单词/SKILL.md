---
name: 每日5个意大利语单词
description: 为「每天5个意大利语单词」系列竖屏短视频生成一期完整内容：edge-tts生成意大利语常速+中文+慢速三段音频、GSAP动画HTML、1080×1920竖屏封面、Puppeteer+FFmpeg渲染MP4。触发词：每天5个意大利语单词、5 parole italiane、5 words、意语每日单词、生成单词视频、意大利语单词系列。
agent_created: true
---

# 每日5个意大利语单词 Skill

为「每天5个意大利语单词」系列生成一期竖屏短视频。每期包含 5 个意大利语单词，每个词展示格式：**意大利语常速 → 中文翻译 → 意大利语慢速**。

**项目根目录**：`D:/意大利语材料/每天5个意大利语单词/`

## 工作流概览

```
Step 1: 定义词汇数据（5个词）
Step 2: 生成每词音频（IT常速 + CN中文 + IT慢速，每词一个独立mp3）
Step 3: 生成主视频HTML（1080x1920竖屏，含GSAP动画时间线）
Step 4: 生成封面HTML（1080x1440，3:4比例）
Step 5: 渲染为MP4视频（Edge headless截图 + FFmpeg编码）
Step 6: 渲染封面为PNG
```

---

## Step 1 — 定义词汇数据

词汇结构（每词6个字段）：

| 字段 | 说明 | 示例 |
|---|---|---|
| `it` | 意大利语单词 | sedici |
| `zh` | 中文翻译 | 十六 |
| `en` | 英文翻译 | sixteen |
| `phonetic` | 中文谐音 | 塞迪奇 |
| `icon_type` | 图标类型: `emoji` 或 `svg` | svg |
| `icon_content` | 图标内容 | SVG代码或emoji字符 |

---

## Step 2 — 生成音频

### 使用 `gen_audio_v2.py` 方式（推荐）

每词生成三段音频：
1. IT常速：`edge-tts` 用 `it-IT-ElsaNeural` 女声，rate `+0%`
2. CN中文：`edge-tts` 用 `zh-CN-XiaoxiaoNeural` 女声，rate `+0%`
3. IT慢速：`edge-tts` 用 `it-IT-ElsaNeural` 女声，rate `-30%`

三段拼接、每词一个音频文件。输出到 `assets/` 目录。

**音频文件命名规则**：`{prefix}_{episode}_0{词序号}.mp3`

例如 `numeri_04_01.mp3` 表示 numeri 主题第4期第1个词。

### 关键参数

```
IT_VOICE = 'it-IT-ElsaNeural'      # 意大利语女声
ZH_VOICE = 'zh-CN-XiaoxiaoNeural'  # 中文女声
IT_SLOW_RATE = '-30%'              # 慢速减速比例
BITRATE = '192k'                   # 导出比特率
```

### 参考脚本

参考 `gen_audio_v2.py` 核心逻辑：

```python
async def gen_one(text, voice, rate='+0%'):
    comm = edge_tts.Communicate(text=text+'.', voice=voice, rate=rate)
    # 生成到临时文件，读取为AudioSegment
    # 返回 AudioSegment 对象

# 每词拼接: it1常速 + cn中文 + it2慢速
combined = it1 + cn + it2
combined.export(out_path, format='mp3', bitrate='192k')
```

> **注意**：pydub 依赖 ffmpeg。脚本需要在 Python 3.12+ 环境中运行，安装 `edge-tts` 和 `pydub`。

---

## Step 3 — 生成主视频HTML

### CSS结构

- 画布尺寸：`1080px × 1920px`
- 背景色：`#f5f0eb`（米白色）
- 字体：`-apple-system, 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', sans-serif`

### 意大利元素装饰

```css
/* 两侧国旗色细条 */
.ita-left  { width: 6px; height: 100%; background: #009246; }  /* 绿色 */
.ita-right { width: 6px; height: 100%; background: #ce2b37; }  /* 红色 */

/* 角落装饰 */
.corner-tl { border-top: 6px solid #ce2b37; border-left: 6px solid #ce2b37; }
.corner-tr { border-top: 6px solid #009246; border-right: 6px solid #009246; }

/* 国旗小图标（标题处） */
.flag-mini {
  width: 78px; height: 50px;
  background: linear-gradient(to right, #009246 33.33%, #fff 33.33%, #fff 66.66%, #ce2b37 66.66%);
}
```

### 顶部标题

```html
<div class="top-header" id="top-header">
  <div class="top-title"><span class="flag-mini"></span>意大利语单词<span class="flag-mini"></span></div>
  <div class="top-sub">PAROLE ITALIANE · 5 PAROLE AL GIORNO</div>
</div>
```

### 5张卡片（核心内容）

每张卡片包含：
- `card-num`: PAROLA {序号} / 第{序号}词
- `card-icon`: SVG 渐变色圆角矩形 + 数字/emoji图标
- `card-it`: 意大利语单词（72px，粗体）
- `card-zh`: 中文翻译（44px，红色）
- `card-en`: 英文翻译（28px，灰色斜体）
- `card-phonetic`: 谐音标注（36px，红底圆角标签）

卡片容器：`.card-wrap`（绝对定位、居中、默认 `opacity:0`）

卡片本身：`.card`（880px宽、白色、圆角48px、红绿渐变顶边）

#### SVG图标方案（推荐用于数字类词汇）

```html
<div class="card-icon">
  <svg viewBox="0 0 200 200">
    <defs>
      <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#667eea"/>
        <stop offset="100%" stop-color="#764ba2"/>
      </linearGradient>
      <filter id="n1">
        <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#764ba2" flood-opacity="0.4"/>
      </filter>
    </defs>
    <rect x="20" y="20" width="160" height="160" rx="30" fill="url(#g1)" filter="url(#n1)"/>
    <text x="100" y="125" font-size="70" font-weight="900" fill="#fff" text-anchor="middle">16</text>
  </svg>
</div>
```

#### Emoji图标方案（推荐用于水果/物品等具象词汇）

```html
<div class="card-icon">🍍</div>
```

### 品牌标识

**中间品牌标语**（顶部区域，动画开始后就可见）：

```html
<div class="middle-brand" id="middle-brand">
  <span class="slogan-text">每天五张卡，意语大声说</span>
</div>
```

**底部品牌**（底部区域）：

```html
<div class="bottom-brand" id="bottom-brand">
  <img class="brand-logo" src="assets/logo-piano.jpg" alt="涛子办事处">
  <span class="brand-text">涛子办事处 · Ufficio di Taozi</span>
</div>
```

`brand-text` 和 `slogan-text` 都使用彩虹渐变动画（`rainbowFlow`）。

### 5圆点进度条

5个圆点，每个 `28×28px`，间距24px：

- `.dot` — 默认：浅红背景，红边框
- `.dot.active` — 已学：红色实心 + 发光阴影
- `.dot.current` — 当前：绿色实心 + 放大1.25x + 发光阴影

```html
<div class="dot-progress" id="dot-progress">
  <div class="dot" id="dot-1"></div>
  <div class="dot" id="dot-2"></div>
  <div class="dot" id="dot-3"></div>
  <div class="dot" id="dot-4"></div>
  <div class="dot" id="dot-5"></div>
</div>
```

### 底部进度条

```html
<div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
```

### Audio标签（5个隐藏）

```html
<audio id="audio-1" src="assets/{prefix}_{episode}_01.mp3" preload="auto"></audio>
<audio id="audio-2" src="assets/{prefix}_{episode}_02.mp3" preload="auto"></audio>
...
```

### GSAP 时间线

使用 `gsap.timeline({ paused: true })`，关键时间参数：

**固定值**：
- 词间间隔（GAP）：`1.5s`
- 圆点过渡权重（XFADE）：`0.256s`
- Intro动画总持续时间：0.6s

**每词时间线计算逻辑**：

```
pos[0] = 0.0

对第 i 个词 (0-based):
  pos[i] = 第i词出现时间
  ats[i] = pos[i] + 0.5s    // 音频播放时间（卡片出现后0.5s播放）
  card_end[i] = ats[i] + durs[i] + GAP  // 卡片结束时间（音频播完后再等1.5s间隙）
  pos[i+1] = card_end[i] + XFADE  // 下一词出现时间（含过渡重叠）

totalDuration = card_end[4] + 0.5  // 最后一张卡结束后多留0.5s收尾
```

**GSAP关键动画**：

```javascript
// Intro (时间0开始)
tl.fromTo("#top-header", ..., 0);
tl.fromTo("#dot-progress", ..., 0.3);
tl.fromTo("#bottom-brand", ..., 0.5);
tl.fromTo("#middle-brand", ..., 0.4);

// 每词（以第1词为例）
tl.fromTo("#card-1", { opacity:0, scale:0.85 }, { opacity:1, scale:1, duration:0.3, ease:"back.out(1.5)" }, pos);
tl.set("#dot-1", { className:"dot current" }, pos);
tl.call(function(){ /* audio-1 play */ }, null, ats);
tl.to("#card-1", { opacity:0, scale:0.95, duration:0.25, ease:"power2.in" }, card_end);
tl.set("#dot-1", { className:"dot active" }, card_end);
tl.set("#dot-2", { className:"dot current" }, pos_next);

// 进度条
tl.fromTo(pf, { width:"0%" }, { width:"100%", duration:totalDuration, ease:"none" }, 0);
tl.to(["#dot-progress","#bottom-brand",".progress-bar"], { opacity:0, duration:0.5 }, totalDuration - 0.6);

tl.play();
window.tl = tl;
window.totalDuration = totalDuration;
```

#### 音频播放（用 call 实现）

```javascript
tl.call(function(){
  document.getElementById("audio-{i+1}").currentTime = 0;
  document.getElementById("audio-{i+1}").play().catch(function(e){});
}, null, ats);
```

**要点**：
- 每词播放自己的独立 audio 标签
- audio 标签 hidden，不需要 visible controls
- 使用 `currentTime = 0` 确保重播时从头开始
- GSAP 时间线控制一切，不需要 audio 的 `ontimeupdate`

---

## Step 4 — 生成封面HTML

封面尺寸：`1080px × 1440px`（3:4比例）

关键元素：
- 顶部/底部意大利国旗三色边条
- 左右红绿侧边装饰条
- 角落L型装饰
- 圆形装饰（右上角）
- 意大利国旗SVG图标
- 主标题：`每天学习<span>5个</span><br>意大利语单词`
- 副标题：`IMPARA 5 PAROLE ITALIANE OGNI GIORNO`
- 5词预览网格（每词显示it + zh）
- 底部品牌：涛子办事处 · Ufficio di Taozi + logo
- 底部小字：`IMPARA L'ITALIANO CON TAOZI`

---

## Step 5 — 渲染MP4

使用 `render_v8.js`，参数：

```bash
node render_v8.js <htmlFile> <outputMp4> [--fps 15] [--width 1080] [--height 1920]
```

**关键参数**：
- FPS: 15（默认）
- 尺寸：1080x1920（竖屏）
- chunk大小：500帧
- Edge路径：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- Puppeteer 核心库路径：检查系统已安装路径
- 输出编码：H.264 + AAC 音频（从 `assets/{name}.mp3` 自动匹配）
- 视频质量：`-crf 18`，`-preset medium`

**渲染流程**：
1. 启动Edge（headless模式），单浏览器会话
2. 探测HTML总duration
3. 计算帧数和时间点列表
4. 分chunk截图（每chunk 500帧，reload页面清理内存）
5. 每帧seek GSAP时间线 + CDP screenshot
6. FFmpeg拼接为MP4
7. 清理临时帧目录

### 前置依赖

- Node.js + puppeteer-core（已全局安装）
- ffmpeg（已安装到系统PATH）
- Microsoft Edge（已安装）
- 项目已包含 `gsap.min.js`（已下载到项目目录）

---

## Step 6 — 渲染封面为PNG

封面HTML需要截图生成PNG（用于视频封面/缩略图）。

可以复用 `render_v8.js` 但只截第一帧，或者使用 `agent-browser` skill 打开封面HTML截图。

---

## 命名规范

| 元素 | 命名模式 | 示例 |
|---|---|---|
| 项目主题前缀 | 英文主题词 | `numeri`, `scuola`, `verbi`, `color`, `fruit`, `famiglia`, `luoghi`, `arte` |
| 期号 | `_0{期号}` | `_04` |
| 音频文件 | `{prefix}_{episode}_0{词序号}.mp3` | `numeri_04_01.mp3` |
| 主HTML | `{prefix}_{episode}_light.html` | `numeri_04_light.html` |
| 视频文件 | `{prefix}_{episode}.mp4` | `numeri_04.mp4` |
| 封面HTML | `cover_{prefix}_{episode}_3x4.html` | `cover_numeri_04_3x4.html` |
| 封面PNG | `cover_{prefix}_{episode}_3x4.png` | `cover_numeri_04_3x4.png` |

---

## 参考脚本

项目目录下的关键脚本及用途：

| 脚本 | 用途 |
|---|---|
| `gen_audio_v2.py` | 生成IT常速+CN中文+IT慢速每词独立音频（推荐） |
| `gen_audio.py` | 生成IT+CN+IT(第二遍常速)每词独立音频（旧版，无慢速） |
| `gen_separate_audio.py` | 将IT和CN分别生成再合并（旧版方式） |
| `color_01_audio.py` | 颜色主题音频生成示例（含目标时长对齐） |
| `update_html.py` | 根据DURATIONS数组更新GSAP时间线 |
| `fix_write.py` | 直接写入完整HTML的示例 |
| `render_v8.js` | Edge headless + FFmpeg 视频渲染引擎 |
| `check_dur.py` | 检查seg片段时长 |
| `check_fruit_times.py` | 计算每词三段音频精确时长（含静音间隔） |
| `verify.py` | 验证HTML中GSAP时间线的card/audio/end时间 |
| `cover_3x4.html` | 3:4封面模板 |

---

## 快速开始 — 新建一期示例

假设要创建 `scuola_03`（学校主题第3期）：

1. **定义5词数据**

2. **生成音频**
```bash
python gen_audio_v2.py  # 修改SETS中的第3期数据后运行
```

3. **创建 HTML** — 基于 `fruit_01_light.html` 或 `numeri_04_light.html` 模板修改：
   - 替换词汇数据（it/zh/en/phonetic）
   - 替换图标
   - 音频src改为新前缀
   - 重新计算GSAP时间线

4. **更新GSAP时间线** — 运行 `check_fruit_times.py` 获取精确时长，或用 `update_html.py` 方式

5. **创建封面** — 基于 `cover_3x4.html` 修改

6. **渲染视频**
```bash
node render_v8.js scuola_03_light.html scuola_03.mp4 --fps 15 --width 1080 --height 1920
```

7. **渲染封面**
```bash
node render_v8.js cover_scuola_03_3x4.html cover_scuola_03_3x4.png --fps 1 --width 1080 --height 1440
```
