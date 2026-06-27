---
name: 每日五个意大利语单词学习（竖屏）
description: 生成意大利语5词竖屏教学页面（1080x1920）及3:4封面图（1080x1440）。当用户说"生成5个意大利语单词"、"做一组颜色单词"、"每日5词"等，或需要创建含音频+动画的竖屏教学页面时使用。自动完成：edge-tts配音生成 → HTML页面构建 → 封面生成 → GSAP音画同步 → 预览。
agent_created: true
---

# 意大利语5词竖屏教学页面生成器

## 概述

此技能用于快速生成意大利语单词教学竖屏视频页面（1080x1920），包含：
- 顶部标题 "意大利语单词" + 意大利国旗配色装饰 + 三色迷你国旗图标
- 中间闪烁标语 "每天五张卡，意语大声说"（彩虹渐变+脉冲光晕动画）
- 底部品牌文字 "涛子办事处 · Ufficio di Taozi"（同样闪烁效果，节奏更慢）
- 5张卡片（意大利语 / 中文 / 英文 / 谐音）
- 5圆点进度条（当前词高亮绿、已完成红）
- 主进度条
- GSAP 音画同步动画
- edge-tts 配音（意大利语正常 + 中文 + 意大利语慢读 + 1.5秒间隔）

## 工作流程

### Step 1：确认单词列表

从用户获取5个单词，每个单词包含：
- `it`：意大利语单词
- `zh`：中文翻译
- `en`：英文翻译
- `phonetic`：中文谐音标注
- `icon`：emoji图标（数字用 1️⃣2️⃣3️⃣4️⃣5️⃣，其他主题自选）

如果用户只说"生成5个单词"而不指定内容，AI自行选择常用意大利语单词（数字、颜色、动物、食物等主题）。

### Step 2：生成配音音频

使用 `scripts/gen_audio.py` 脚本生成配音 MP3。

**音频结构（每个单词）：**
1. 意大利语正常语速（`it-IT-ElsaNeural`, rate=`+0%`）
2. 中文（`zh-CN-XiaoxiaoNeural`, rate=`+0%`）
3. 意大利语慢读（`it-IT-ElsaNeural`, rate=`-30%`）
4. 间隔 1.5 秒

> 三个片段直接拼接（IT→CN→IT之间无静音），1.5秒间隔在GSAP时间线中控制而非混入音频文件。

**执行方式：**
```bash
python scripts/gen_audio.py
```

修改脚本中的 `SETS` 字典可自定义单词列表。直接运行会生成3组默认音频（水果/数字/颜色），输出到 `assets/` 目录。

脚本会打印每个音频片段的时长，用于精确校准GSAP时间线。

**参考：** `references/audio_format.md` 含详细音色参数和代码示例。

### Step 3：创建 HTML 页面

使用 `assets/template.html` 作为模板，替换以下内容：
- 5张卡片的 `it` / `zh` / `en` / `phonetic` / `icon`
- 音频 `src` 路径
- GSAP 时间线（根据音频实际时长精确校准）

**关键布局参数（已验证）：**

| 元素 | CSS 位置 |
|---|---|
| 顶部标题 `.top-header` | `top: 238px` |
| 顶部标题 `.top-title` 字体 | `font-size: 52px; font-weight: 800` |
| 迷你国旗 `.flag-mini` | `width: 78px; height: 50px`（三色渐变，与标题等高） |
| 中间闪烁标语 `.slogan-text` | `top: 420px; font-size: 36px; font-weight: 900` |
| 5圆点进度条 `.dot-progress` | `bottom: 265px` |
| 底部品牌 `.brand-text` | `bottom: 405px; font-size: 38px; font-weight: 900` |
| 主进度条 `.progress-bar` | `bottom: 0` |
| 封面尺寸 | `1080×1440`（3:4）|

**封面设计元素（`cover_{theme}_3x4.html`）：**
- 顶部/底部三色国旗边条（8px高）
- 左右侧绿/红色竖条（12px宽）
- 左上角 L 型红色装饰 + 右下角 L 型绿色装饰
- 右上双圆圈装饰
- 中部装饰线
- 意大利国旗 SVG 图标（180×120px）
- 主标题：每天学习5个意大利语单词（88px, `#ce2b37`高亮)
- 副标题：IMPARA 5 PAROLE ITALIANE OGNI GIORNO（40px, 绿色）
- 5个单词预览卡片（圆角28px, 白底阴影）
- 底部品牌行 + 底部主题标注（如"水果篇"）

**GSAP 时间线规则：**
- 每张卡片 `fromTo` 入场（0.3s, `back.out(1.5)`）
- 每张卡片 `to` 出场（0.25s, `power2.in`）
- 圆点通过 `tl.set()` 切换 className（`dot` → `dot current` → `dot active`）
- 主进度条用 `tl.fromTo(pf, {width:'0%'}, {width:'100%'})` 驱动

**GSAP 时间线计算公式（音频重生成后用）：**

音频重生成后时长变化，需重新计算时间线。已知每卡音频时长 `D[i]`（i=0~4）：

```
GAP_BETWEEN = 1.5   # 组间停顿秒数
CROSSFADE = 0.256    # 圆点过渡时间

pos[0] = 0.0
for i in range(5):
    audio_at = pos[i] + 0.5       # 音频播放起点
    card_end = pos[i] + 0.5 + D[i] + GAP_BETWEEN  # 卡片消失点
    if i < 4:
        pos[i+1] = card_end + CROSSFADE   # 下个卡片出现点
total = card_end[-1] + 0.5        # 进度条总时长

# 每个卡片对应的GSAP调用：
# tl.fromTo("#card-N", ... , pos[i])           - 卡片出现
# tl.call(..., audio-N..., audio_at)           - 音频播放
# tl.to("#card-N", ..., card_end)               - 卡片消失
# tl.set("#dot-N", "active", card_end)          - 圆点变已完成
# tl.set("#dot-N+1", "current", pos[i+1])       - 下个圆点高亮
# tl.fromTo(pf, ..., total)                     - 进度条
```

**常见故障排查：**
- 音频时长改变后卡片消失时间未更新 → 卡片听不完就被切掉
- 临时文件权限拒绝 → 用 `tempfile.gettempdir()` 避开受限目录

### 彩虹闪烁效果说明

顶部标语和底部品牌文字均使用 CSS 彩虹渐变 + 脉冲光晕动画：

```css
.slogan-text, .brand-text {
  background: linear-gradient(90deg, #ce2b37, #ff6600, #ffcc00, #009246, #0066cc, #9b59b6, #ce2b37);
  background-size: 400% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 10px rgba(206,43,55,0.3));
}

.slogan-text { animation: rainbowFlow 8s ease-in-out infinite; }   /* 标语：8s周期 */
.brand-text { animation: rainbowFlow 12s ease-in-out infinite; }    /* 品牌：12s周期（更慢） */

@keyframes rainbowFlow {
  0%   { background-position: 0% 50%; filter: drop-shadow(0 0 4px rgba(206,43,55,0.3)); }
  25%  { filter: drop-shadow(0 0 16px rgba(255,102,0,0.6)); }
  50%  { background-position: 100% 50%; filter: drop-shadow(0 0 4px rgba(0,146,70,0.3)); }
  75%  { filter: drop-shadow(0 0 18px rgba(0,102,204,0.6)); }
  100% { background-position: 0% 50%; filter: drop-shadow(0 0 4px rgba(206,43,55,0.3)); }
}
```

标语和品牌文字使用同一个关键帧，但不同周期（标语8s，品牌12s），形成错落的呼吸感。

### Step 4：预览与微调

用 `preview_url` 工具预览 HTML 文件，根据用户反馈微调：
- 位置调整：说"XXX上移/下移XXpx"
- 字体大小：说"XXX字体放大/缩小X号"
- 颜色：说"XXX改成XXX颜色"
- 闪烁频率：说"闪烁频率调慢/调快"
- 闪烁颜色：调整 `.slogan-text` / `.brand-text` 的 `linear-gradient()` 色值
- 脉冲光晕：调整 `drop-shadow()` 的 `rgba()` 值和模糊半径
- 顶部主标题：默认 "意大利语单词"，可改为其他文字
- 中间标语：默认 "每天五张卡，意语大声说"，可替换
- 底部品牌：默认 "涛子办事处 · Ufficio di Taozi"，可替换

### Step 4.5（可选）：生成 3:4 封面图

基于已有封面模板（如 `cover_fruit_3x4.html`）为当前主题制作封面：

**步骤：**
1. 复制 `cover_fruit_3x4.html` 为 `cover_{theme}_3x4.html`
2. 替换 `<title>` 中的主题名称
3. 替换 5 个 `.word-chip` 卡片中的意大利语单词和中文翻译
4. 替换底部 `.bottom-note` 中的主题标注文字
5. 用 Puppeteer/Edge 截图输出为 PNG

**截图方法：**
```javascript
const puppeteer = require('puppeteer-core');
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
// 设置视口: 1080x1440, deviceScaleFactor: 2
// 截图格式: PNG, fullPage: true
```

输出文件命名：`cover_{theme}_3x4.png`，2160×2880（2x retina）。

**已有封面套系：** fruit（水果篇）、color（颜色篇）、scuola（教室篇）、numeri_02（数字6-10篇）

### Step 5（可选）：导出 MP4

使用 `html-to-mp4-render` 技能中的 `render_v8.js` 将 HTML 渲染为竖屏 MP4。

**前置条件：**
- Edge 浏览器（已安装）
- FFmpeg（已安装）
- Node.js + `puppeteer-core`（已安装）

**步骤 5.1：生成组合音频**

HTML 页面有 5 个独立 `<audio>` 元素，渲染时需合并为一个音频文件，严格对齐 GSAP 时间线：

```
LEAD_IN = 0.5s     # 首段音频前静音（对应入场动画）
GAP = 2.256s       # 组间间隔（= 1.5s停顿 + 0.256s过渡 + 0.5s下段音频延迟）
PAD_END            # 末尾补齐到 totalDuration

组合音频 = silence(0.5s) + audio1 + silence(2.256s) + audio2 + silence(2.256s) + ...
       + audio5 + silence(totalDuration - 组合总时长)
```

参考 Python 代码：
```python
from pydub import AudioSegment
combined = AudioSegment.silent(duration=500)  # 0.5s lead-in
for i in range(5):
    seg = AudioSegment.from_file(f'assets/{prefix}_01_0{i+1}.mp3')
    combined += seg
    if i < 4:
        combined += AudioSegment.silent(duration=2256)  # 2.256s gap
target_ms = int(totalDuration * 1000)
if len(combined) < target_ms:
    combined += AudioSegment.silent(duration=target_ms - len(combined))
combined.export(f'assets/{prefix}_01.mp3', format='mp3', bitrate='192k')
```

**步骤 5.2：执行渲染**

```bash
cp <path-to>/render_v8.js <html目录>/
NODE_PATH="<puppeteer路径>/node_modules" node render_v8.js \
    <file>.html <output>.mp4 --fps 30 --width 1080 --height 1920
```

关键参数：
- `--width 1080 --height 1920` — 竖屏分辨率
- `--fps 30` — 帧率（默认30fps，高清流畅）
- 渲染脚本自动搜索 `assets/<basename>.mp3` 作为音频源

**步骤 5.3：验证**

打开生成的 MP4，检查：
- 音频是否与卡片切换同步
- 每段音频（IT常速→CN→IT慢速）是否完整播放
- 组间 1.5s 停顿是否正确

## 文件结构

```
italian-5words-vertical/
├── SKILL.md              # 本文件
├── scripts/
│   └── gen_audio.py    # 配音生成脚本（edge-tts）
├── assets/
│   ├── template.html    # HTML模板（含GSAP动画框架）
│   └── logo-piano.jpg  # 品牌logo图片
└── references/
    └── audio_format.md  # 音频格式说明（配音结构、edge-tts参数）
```

## 注意事项

1. **GSAP 库**：HTML 需引用同目录下的 `gsap.min.js`（已存在于 `D:/意大利语材料/意大利语手势竖版单个/`）
2. **音频自动播放**：页面加载后需调用 `tl.play()` 和 `audio.play()`，浏览器可能阻止，需用户点击页面
3. **`gsap.set()` 语法**：用 `gsap.set(elem, {className:'dot active'})` 而非 `tl.to(elem, {className:...})`
4. **进度条驱动**：优先用 GSAP 时间线驱动，避免独立 `requestAnimationFrame` 导致语法错误（curly quote 问题）
5. **彩虹闪烁兼容**：`-webkit-background-clip: text` 在部分浏览器中需加 `-webkit-` 前缀；`background-clip: text` 为标准属性
6. **并发渲染说明**：`render_v8.js` 使用固定目录 `_render_frames/` 存放临时帧，**不可并行运行**多个渲染任务，否则最后一个完成的渲染会因帧目录被清理而失败
