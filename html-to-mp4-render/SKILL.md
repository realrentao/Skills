---
name: html-to-mp4-render
description: |
  Render GSAP-animated HTML courseware (1920x1080) to MP4 using Edge headless + Puppeteer CDP screenshots + FFmpeg encoding.
  Handles GSAP from() seek correctness via invalidate(), yuvj420p pixel format, and single-browser stability.
  Trigger: "渲染HTML为MP4", "render HTML to MP4", "把HTML课件转成视频", "generate video from HTML".
agent_created: true
---

# HTML → MP4 Courseware Render

## Purpose

Converts GSAP-animated HTML courseware pages (1920x1080) into H.264 MP4 videos with synchronized audio, following a robust single-browser chunked capture pipeline.

## When to Use

- Rendering any GSAP-powered HTML teaching courseware to MP4
- User asks to "render", "转MP4", "生成视频" from an HTML file
- Re-rendering existing courseware at higher FPS or with fixed pixel format

## Critical Rules (learned from hard failures)

### 1. NEVER use `run_in_background: true` for long renders

Background tasks are killed by the system after ~10 minutes. Instead:

```bash
# CORRECT: foreground launch → auto-background after timeout
node scripts/render_v8.js input.html output.mp4 --fps 15 2>&1
# timeout: 180000 (3 min) → will auto-background and continue

# WRONG: dies at 10 min
# run_in_background: true
```

### 2. Single browser session, page.reload() between chunks

Opening/closing Edge repeatedly causes CDP disconnects. Launch once, reload per chunk.

### 3. GSAP from() tweens need `seek(0).seek(time)` pattern

Plain `tl.seek(time)` produces wrong frame states for `from()` tweens. Using `invalidate()` clears all cached values and makes elements invisible. The correct approach: first seek to 0 to reset all `from()` initial states, then seek to the target time.

```javascript
// CORRECT: reset from() states, then seek
tl.seek(0);
tl.seek(time);

// WRONG: causes duplicated/wrong content
tl.seek(time);

// WRONG: causes all content to disappear
tl.invalidate(); tl.seek(time);
```

### 4. yuvj420p pixel format fix

JPEG screenshots carry full-range (yuvj420p) metadata. The `-vf scale=in_range=full:out_range=limited` filter converts to standard TV-range yuv420p:

```
ffmpeg -vf "scale=in_range=full:out_range=limited" -pix_fmt yuv420p -color_range tv
```

## Usage

```bash
node scripts/render_v8.js <htmlFile> <outputMp4> [--fps 15]
```

### Example

```bash
cd "D:/意大利语材料/意大利语美发课程全套资料/视频汇总"
node render_v8.js lezione05.html lezione05.mp4 --fps 30
```

### 环境依赖（已修复）

- **puppeteer-core**: 安装到 `C:\Users\迪丽希斯\.workbuddy\binaries\node\workspace\node_modules\puppeteer-core`（`npm install puppeteer-core`）
- **Edge 路径**: WorkBuddy 用的是 32-bit Node，必须用 `process.env['ProgramFiles(x86)']` 而不是 `process.env.ProgramFiles`（后者返回64位路径但 Edge 在32位路径）
  - 正确: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
  - 错误: `C:\Program Files\Microsoft\Edge\Application\msedge.exe`
  - `render_v8.js` 已修复为 `path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', ...)`

## Script: render_v8.js

Located at `scripts/render_v8.js`. Key characteristics:

- **CHUNK_SIZE**: 500 frames per browser page load
- **Screenshot**: CDP `Page.captureScreenshot`, JPEG quality 80
- **FFmpeg**: libx264, crf=18, preset=medium, yuv420p tv-range, movflags +faststart
- **Audio**: Auto-detected from `assets/<basename>.mp3` (derived from HTML filename)
- **Duration**: Read from `window.totalDuration` or `<audio data-duration>`

## Reference

### GSAP Animation Requirements

HTML files must expose:
- `window.tl` — main GSAP timeline (paused)
- `window.__timelines` — optional map of named timelines
- `window.totalDuration` — total animation duration in seconds
- `<audio id="audio" data-duration="794" src="assets/lezioneXX.mp3">`

### ⚠️ Critical: No `seek(0)` if no `from()` tweens

The original `render_v8.js` does `tl.seek(0); tl.seek(t)` on every frame to reset `from()` tween initial states. **If your HTML only uses `set()` and `to()` (no `from()` tweens), you MUST remove `seek(0)`:**

```javascript
// ❌ Bad — seek(0) resets all animations to start state, causing
//    stagger animations to re-run every frame → visual bounce/jitter
if (tl) { tl.seek(0); tl.seek(seekTime); }

// ✅ Good — direct seek, no re-run of completed animations
if (tl) { tl.seek(seekTime); }
```

The `seek(0)` reset causes completed stagger/to animations to re-play from position 0 on every frame. For card-stagger intros, this makes highlighted cards visually "pop" or "bounce" during transitions. Removing `seek(0)` when no `from()` tweens exist eliminates this artifact entirely.

**Also required:** set `window.__renderOnly = true` via `evaluateOnNewDocument` before `page.goto()` to prevent auto-play:

```javascript
await page.evaluateOnNewDocument(() => { window.__renderOnly = true; });
```

### 30fps High-FPS Rendering Tips

When rendering at 30fps (or higher), the frame count doubles and memory pressure increases. Adjustments:

- **Reduce chunk size**: `const CHUNK_SIZE = 300;` (default is 500). Smaller chunks prevent Edge/Puppeteer from running out of memory on long renders.
- **Keep quality=80**: Higher quality means larger Base64 data per frame, which slows disk writes. 80 is the sweet spot for slide/video content.
- **Monitor progress**: At 30fps, a 46s video = ~1400 frames. At ~2f/s capture rate, expect ~12 min total render time.
- **Timeout**: Set Bash timeout to 900000ms (15 minutes) or more for high-fps renders.

### FFmpeg Parameters (optimized for slide content)
| GOP | fps × 2 | Regular keyframe interval |
| pix_fmt | yuv420p | Standard broadcast range |
| color_range | tv | Limited range (16-235) |
| movflags | +faststart | Web streaming ready |
| audio | aac 192k | Good voice quality |
