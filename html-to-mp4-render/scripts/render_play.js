#!/usr/bin/env node
/**
 * render_play.js — Real-time playback + screenshot capture
 *
 * Instead of seeking the timeline frame by frame, this plays the audio
 * and syncs GSAP to audio.currentTime (already built into lezione HTML).
 * Captures screenshots at target FPS while the audio plays.
 *
 * Usage: node render_play.js <htmlFile> <outputMp4> [--fps 15]
 */
const puppeteer = require('C:/ProgramData/WorkBuddy/chromium-env/1xej3f3/.workbuddy/binaries/node/workspace/node_modules/puppeteer-core');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: node render_play.js <htmlFile> <outputMp4> [--fps 15]');
  process.exit(1);
}
const htmlFile = path.resolve(args[0]);
const outputMp4 = path.resolve(args[1]);
const fps = parseInt(args[args.indexOf('--fps') + 1]) || 15;

if (!fs.existsSync(htmlFile)) { console.error('HTML not found'); process.exit(1); }

const htmlDir = path.dirname(htmlFile);
const framesDir = path.join(htmlDir, '_render_frames');
if (fs.existsSync(framesDir)) fs.rmSync(framesDir, { recursive: true });
fs.mkdirSync(framesDir, { recursive: true });

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const htmlUrl = `file:///${htmlFile.replace(/\\/g, '/')}`;

async function render() {
  const t0 = Date.now();
  console.log('[0/4] Launching Edge...');
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: EDGE_PATH,
    args: [
      '--no-sandbox', '--disable-gpu', '--window-size=1920,1080',
      '--disable-extensions', '--disable-features=TranslateUI',
      '--autoplay-policy=no-user-gesture-required',
    ],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

  // Allow autoplay
  const cdp = await page.target().createCDPSession();
  await cdp.send('Page.enable');

  console.log('[1/4] Loading page + starting playback...');
  await page.goto(htmlUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);

  // Hide any UI controls
  await page.evaluate(() => {
    // Hide scrollbars, controls, cursor
    const style = document.createElement('style');
    style.textContent = `
      *::-webkit-scrollbar { display: none !important; }
      body { cursor: none !important; overflow: hidden !important; }
      audio, video { display: none !important; }
    `;
    document.head.appendChild(style);

    // Trigger audio play + GSAP sync (already in HTML, but force it)
    const audio = document.getElementById('audio');
    if (audio) {
      audio.currentTime = 0;
      audio.play().catch(() => {});
    }
  });

  // Wait for playback to actually start
  await new Promise(r => setTimeout(r, 3000));

  // Get duration
  const totalDuration = await page.evaluate(() => {
    return parseFloat(document.getElementById('audio')?.dataset?.duration || 794);
  });
  console.log(`  Duration: ${totalDuration}s | FPS: ${fps}`);

  // Start capturing frames while audio plays
  const totalFrames = Math.ceil(totalDuration * fps);
  console.log(`[2/4] Capturing ${totalFrames} frames at ${fps} fps (real-time playback)...`);

  const frameInterval = 1000 / fps; // ms between frames
  let frameCount = 0;
  const captureStart = Date.now();
  let lastReport = 0;

  const client = await page.target().createCDPSession();

  while (frameCount < totalFrames) {
    const frameNum = String(frameCount).padStart(6, '0');
    const framePath = path.join(framesDir, `frame_${frameNum}.jpg`);

    // Check if audio is still playing
    const isPlaying = await page.evaluate(() => {
      const audio = document.getElementById('audio');
      return audio && !audio.paused && !audio.ended;
    });

    if (!isPlaying && frameCount > 10) {
      console.log(`  Audio ended at frame ${frameCount}/${totalFrames}`);
      break;
    }

    try {
      const { data } = await client.send('Page.captureScreenshot', {
        format: 'jpeg', quality: 80,
        clip: { x: 0, y: 0, width: 1920, height: 1080, scale: 1 },
      });
      fs.writeFileSync(framePath, Buffer.from(data, 'base64'));
      frameCount++;
    } catch (err) {
      console.error(`  Frame ${frameCount} error: ${err.message}`);
      await new Promise(r => setTimeout(r, 500));
      continue;
    }

    // Report every 5 seconds
    const elapsed = (Date.now() - captureStart) / 1000;
    if (elapsed - lastReport >= 5) {
      lastReport = elapsed;
      const pct = ((frameCount / totalFrames) * 100).toFixed(1);
      const actualFps = (frameCount / elapsed).toFixed(1);
      console.log(`  ${pct}% | ${frameCount}/${totalFrames} frames | ${actualFps}fps | ${elapsed.toFixed(0)}s / ${totalDuration}s`);
    }

    // Wait for next frame time
    const nextFrameTime = captureStart + frameCount * frameInterval;
    const waitMs = Math.max(1, nextFrameTime - Date.now());
    await new Promise(r => setTimeout(r, waitMs));
  }

  const captureTime = ((Date.now() - captureStart) / 1000).toFixed(1);
  console.log(`  ✓ Captured ${frameCount} frames in ${captureTime}s`);

  await browser.close();

  // If we captured fewer frames than expected, pad with the last frame
  while (frameCount < totalFrames) {
    const lastFrame = path.join(framesDir, `frame_${String(frameCount - 1).padStart(6, '0')}.jpg`);
    if (fs.existsSync(lastFrame)) {
      const newFrame = path.join(framesDir, `frame_${String(frameCount).padStart(6, '0')}.jpg`);
      fs.copyFileSync(lastFrame, newFrame);
      frameCount++;
    } else {
      break;
    }
  }

  // FFmpeg encode
  console.log(`[3/4] Encoding ${frameCount} frames to MP4...`);
  const framePattern = path.join(framesDir, 'frame_%06d.jpg').replace(/\\/g, '/');
  const audioName = path.basename(htmlFile, '.html').replace(/^lezione/, 'lezione') + '.mp3';
  const audioPath = path.resolve(htmlDir, 'assets', audioName);
  const hasAudio = fs.existsSync(audioPath);

  const ff = ['-y', '-framerate', String(fps), '-i', framePattern];
  if (hasAudio) ff.push('-i', audioPath.replace(/\\/g, '/'));
  ff.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-vf', 'scale=in_range=full:out_range=limited', '-pix_fmt', 'yuv420p', '-color_range', 'tv',
    '-g', String(fps*2), '-keyint_min', String(fps), '-sc_threshold', '0', '-movflags', '+faststart');
  if (hasAudio) ff.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
  ff.push(outputMp4.replace(/\\/g, '/'));

  execSync(`ffmpeg ${ff.join(' ')}`, { stdio: 'inherit', timeout: 600000 });

  console.log('[4/4] Cleanup...');
  fs.rmSync(framesDir, { recursive: true });

  const sz = (fs.statSync(outputMp4).size / 1024 / 1024).toFixed(1);
  const tt = ((Date.now() - t0) / 1000).toFixed(1);
  console.log(`\n✅ ${outputMp4} | ${sz} MB | ${tt}s`);
}

render().catch(err => { console.error('FAILED:', err); process.exit(1); });
