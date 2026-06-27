#!/usr/bin/env node
/**
 * render_vertical.js — 竖屏 1080x1920 GSAP 动画页面渲染为 MP4
 * 基于 render_v8.js，适配竖屏视频尺寸
 *
 * Usage: node render_vertical.js <htmlFile> <outputMp4> [--fps 15] [--audio <mp3>]
 */
const puppeteer = require('C:/ProgramData/WorkBuddy/chromium-env/1xej3f3/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: node render_vertical.js <htmlFile> <outputMp4> [--fps 15] [--audio audio.mp3]');
  process.exit(1);
}
const htmlFile = path.resolve(args[0]);
const outputMp4 = path.resolve(args[1]);
const fpsIdx = args.indexOf('--fps');
const fps = fpsIdx >= 0 ? parseInt(args[fpsIdx + 1]) : 15;
const audioIdx = args.indexOf('--audio');
const overrideAudio = audioIdx >= 0 ? path.resolve(args[audioIdx + 1]) : null;

const CHUNK_SIZE = 500;
const W = 1080, H = 1920;

if (!fs.existsSync(htmlFile)) { console.error('HTML not found'); process.exit(1); }

const htmlDir = path.dirname(htmlFile);
const framesDir = path.join(htmlDir, '_render_frames');
if (fs.existsSync(framesDir)) fs.rmSync(framesDir, { recursive: true });
fs.mkdirSync(framesDir, { recursive: true });

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const htmlUrl = `file:///${htmlFile.replace(/\\/g, '/')}`;

async function render() {
  const t0 = Date.now();

  console.log('[0/4] Launching Edge (single session)...');
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: EDGE_PATH,
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--disable-gpu', '--disable-dev-shm-usage',
      `--window-size=${W},${H}`,
      '--disable-extensions', '--disable-background-networking',
      '--disable-sync', '--no-first-run',
      '--disable-features=TranslateUI', '--mute-audio',
    ],
  });

  // Probe duration
  console.log('[1/4] Probing...');
  let page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  await page.goto(htmlUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  // 立即暂停所有 timeline，防止自动播放导致 seek 回溯时动画错乱
  await page.evaluate(() => {
    if (window.__timelines) {
      for (const k of Object.keys(window.__timelines)) {
        window.__timelines[k].pause();
      }
    }
  });
  await new Promise(r => setTimeout(r, 1000)); // 仅等 GSAP 初始化，不等播放

  const info = await page.evaluate(() => ({
    duration: window.totalDuration || parseFloat(document.getElementById('audio')?.dataset?.duration || 0),
  }));

  const totalDuration = info.duration;
  if (!totalDuration || totalDuration <= 0) { console.error('No duration found. Set window.totalDuration in HTML.'); await browser.close(); process.exit(1); }

  const totalFrames = Math.ceil(totalDuration * fps);
  console.log(`  Duration: ${totalDuration.toFixed(1)}s | FPS: ${fps} | Frames: ${totalFrames} | Size: ${W}x${H}`);

  // Build time points
  const times = [];
  const interval = 1 / fps;
  for (let ft = 0; ft <= totalDuration; ft += interval) times.push(Math.round(ft * 1000) / 1000);
  while (times.length > totalFrames) times.pop();

  // Split into chunks
  const chunks = [];
  for (let i = 0; i < totalFrames; i += CHUNK_SIZE) {
    chunks.push({ start: i, end: Math.min(i + CHUNK_SIZE, totalFrames) });
  }

  console.log(`[2/4] Capturing ${totalFrames} frames in ${chunks.length} chunks...`);

  let globalFrameCount = 0;
  const captureStart = Date.now();

  for (let ci = 0; ci < chunks.length; ci++) {
    const { start, end } = chunks[ci];
    const chunkTotal = end - start;
    console.log(`\n--- Chunk ${ci + 1}/${chunks.length}: frames ${start}-${end - 1} (${chunkTotal} frames) ---`);

    await page.goto(htmlUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    // 立即暂停所有 timeline，防止自动播放干扰 seek
    await page.evaluate(() => {
      if (window.__timelines) {
        for (const k of Object.keys(window.__timelines)) {
          window.__timelines[k].pause();
        }
      }
    });
    await new Promise(r => setTimeout(r, 800)); // 仅等 GSAP 初始化

    const client = await page.target().createCDPSession();
    const chunkStart = Date.now();
    let lastPct = -1;
    let errors = 0;

    for (let i = start; i < end; i++) {
      const t = times[i];
      const frameNum = String(i).padStart(6, '0');
      const framePath = path.join(framesDir, `frame_${frameNum}.jpg`);

      try {
        await page.evaluate((seekTime) => {
          const timelines = window.__timelines;
          if (timelines) {
            for (const k of Object.keys(timelines)) {
              var tl = timelines[k];
              tl.pause();   // 确保暂停
              tl.seek(0);   // 回到起点
              tl.seek(seekTime); // 定位到目标时间
            }
          }
          // 不依赖 tl.call() 回调，直接根据时间计算并应用高亮
          if (window.resetHighlights) window.resetHighlights();
          if (window.computeHighlight && window.highlightFn) {
            window.highlightFn(window.computeHighlight(seekTime));
          }
        }, t);

        await new Promise(r => setTimeout(r, 25));

        const { data } = await client.send('Page.captureScreenshot', {
          format: 'jpeg', quality: 80,
          clip: { x: 0, y: 0, width: W, height: H, scale: 1 },
        });

        fs.writeFileSync(framePath, Buffer.from(data, 'base64'));
        globalFrameCount++;
        errors = 0;
      } catch (err) {
        errors++;
        if (errors > 15) throw new Error(`Frame ${i}: ${err.message}`);
        await new Promise(r => setTimeout(r, 500));
        i--;
        continue;
      }

      const pct = Math.floor(((i - start) / chunkTotal) * 100);
      if (pct > lastPct && pct % 10 === 0) {
        lastPct = pct;
        const el = ((Date.now() - chunkStart) / 1000).toFixed(0);
        const rate = ((i - start + 1) / ((Date.now() - chunkStart) / 1000)).toFixed(1);
        console.log(`  ${pct}% (${i-start+1}/${chunkTotal}) ${rate}f/s ${el}s | total: ${globalFrameCount}/${totalFrames}`);
      }
    }

    const chunkTime = ((Date.now() - chunkStart) / 1000).toFixed(1);
    console.log(`  Done Chunk ${ci+1}/${chunks.length} in ${chunkTime}s | ${globalFrameCount}/${totalFrames} total`);
  }

  await browser.close();
  const captureTime = ((Date.now() - captureStart) / 1000).toFixed(0);
  console.log(`\n  All ${totalFrames} frames captured in ${captureTime}s`);

  // FFmpeg encode
  console.log('[3/4] Encoding with FFmpeg...');
  const framePattern = path.join(framesDir, 'frame_%06d.jpg').replace(/\\/g, '/');
  const audioFile = overrideAudio || path.join(htmlDir, 'buonanotte_completa.mp3');
  const hasAudio = fs.existsSync(audioFile);

  // 音频已由 resync_audio.py 精确合成，包含开场静音，无需 itsoffset
  const ff = ['-y', '-framerate', String(fps), '-i', framePattern];
  if (hasAudio) {
    ff.push('-i', audioFile.replace(/\\/g, '/'));
    console.log(`  Audio: ${audioFile} (pre-synced, no delay needed)`);
  }
  ff.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-vf', 'scale=in_range=full:out_range=limited', '-pix_fmt', 'yuv420p', '-color_range', 'tv',
    '-g', String(fps*2), '-keyint_min', String(fps), '-sc_threshold', '0', '-movflags', '+faststart');
  if (hasAudio) ff.push('-c:a', 'aac', '-b:a', '192k');
  ff.push(outputMp4.replace(/\\/g, '/'));

  execSync(`ffmpeg ${ff.join(' ')}`, { stdio: 'inherit', timeout: 600000 });

  console.log('[4/4] Cleanup...');
  fs.rmSync(framesDir, { recursive: true });

  const sz = (fs.statSync(outputMp4).size / 1024 / 1024).toFixed(1);
  const totalTime = ((Date.now() - t0) / 1000).toFixed(0);
  console.log(`\nDone! ${outputMp4} (${sz} MB) in ${totalTime}s`);
}

render().catch(e => { console.error(e); process.exit(1); });
