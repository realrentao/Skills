#!/usr/bin/env node
/**
 * render_v8.js — Single-browser all-chunk render (avoids restart crashes)
 *
 * Key insight: launching/closing Edge repeatedly causes CDP disconnects.
 * Solution: launch once, page.reload() between chunks.
 *
 * Usage: node render_v8.js <htmlFile> <outputMp4> [--fps 30]
 */
// Dynamically resolve puppeteer-core from project node_modules (fallback to cwd parent)
const path = require('path');
let puppeteer;
const dirs = [process.cwd(), path.dirname(process.execPath), __dirname, 'C:/Users/迪丽希斯/.workbuddy/binaries/node/workspace'];
for (const d of dirs) {
  try { puppeteer = require(path.join(d, 'node_modules', 'puppeteer-core')); break; } catch {}
  try { puppeteer = require(path.join(d, '..', 'node_modules', 'puppeteer-core')); break; } catch {}
}
if (!puppeteer) { console.error('puppeteer-core not found in node_modules'); process.exit(1); }
const fs = require('fs');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: node render_v8.js <htmlFile> <outputMp4> [--fps 15]');
  process.exit(1);
}
const htmlFile = path.resolve(args[0]);
const outputMp4 = path.resolve(args[1]);
const fps = parseInt(args[args.indexOf('--fps') + 1]) || 15;
const width = parseInt(args[args.indexOf('--width') + 1]) || 1920;
const height = parseInt(args[args.indexOf('--height') + 1]) || 1080;
const CHUNK_SIZE = 500;

if (!fs.existsSync(htmlFile)) { console.error('HTML not found'); process.exit(1); }

const htmlDir = path.dirname(htmlFile);
const framesDir = path.join(htmlDir, '_render_frames');
if (fs.existsSync(framesDir)) fs.rmSync(framesDir, { recursive: true });
fs.mkdirSync(framesDir, { recursive: true });

const EDGE_PATH = path.join(process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)', 'Microsoft', 'Edge', 'Application', 'msedge.exe');
const htmlUrl = `file:///${htmlFile.replace(/\\/g, '/')}`;

async function render() {
  const t0 = Date.now();

  // Launch browser ONCE
  console.log('[0/4] Launching Edge (single session)...');
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: EDGE_PATH,
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--disable-gpu', '--disable-dev-shm-usage',
      `--window-size=${width},${height}`,
      '--disable-extensions', '--disable-background-networking',
      '--disable-sync', '--no-first-run',
      '--disable-features=TranslateUI', '--mute-audio',
    ],
  });

  // Probe duration
  console.log('[1/4] Probing...');
  let page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto(htmlUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 4000));

  const info = await page.evaluate(() => ({
    duration: window.totalDuration || parseFloat(document.getElementById('audio')?.dataset?.duration || 0),
    hasAudio: !!document.getElementById('audio')?.getAttribute('src'),
  }));

  const totalDuration = info.duration;
  if (!totalDuration || totalDuration <= 0) { console.error('No duration'); await browser.close(); process.exit(1); }

  const totalFrames = Math.ceil(totalDuration * fps);
  console.log(`  Duration: ${totalDuration.toFixed(1)}s | FPS: ${fps} | Frames: ${totalFrames}`);

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

  console.log(`[2/4] Capturing ${totalFrames} frames in ${chunks.length} chunks (single browser)...`);

  let globalFrameCount = 0;
  const captureStart = Date.now();

  for (let ci = 0; ci < chunks.length; ci++) {
    const { start, end } = chunks[ci];
    const chunkTotal = end - start;
    console.log(`\n--- Chunk ${ci + 1}/${chunks.length}: frames ${start}-${end - 1} (${chunkTotal} frames) ---`);

    // Reload page for each chunk (clean state, avoid memory leaks)
    await page.goto(htmlUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise(r => setTimeout(r, 3000));

    const client = await page.target().createCDPSession();
    const chunkStart = Date.now();
    let lastPct = -1;
    let errors = 0;

    for (let i = start; i < end; i++) {
      const t = times[i];
      const frameNum = String(i).padStart(6, '0');
      const framePath = path.join(framesDir, `frame_${frameNum}.jpg`);

      try {
        // seek(0) first to reset all from() tween initial states, then seek to target
        await page.evaluate((seekTime) => {
          const tl = window.tl;
          const timelines = window.__timelines;
          if (tl) { tl.seek(0); tl.seek(seekTime); }
          if (timelines) {
            for (const k of Object.keys(timelines)) {
              timelines[k].seek(0);
              timelines[k].seek(seekTime);
            }
          }
        }, t);

        await new Promise(r => setTimeout(r, 25));

        const { data } = await client.send('Page.captureScreenshot', {
          format: 'jpeg', quality: 80,
          clip: { x: 0, y: 0, width, height, scale: 1 },
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
    console.log(`  ✓ Chunk ${ci+1}/${chunks.length} done in ${chunkTime}s | ${globalFrameCount}/${totalFrames} total`);
  }

  await browser.close();

  const captureTime = ((Date.now() - captureStart) / 1000).toFixed(0);
  console.log(`\n  ✓ All ${totalFrames} frames in ${captureTime}s`);

  // FFmpeg encode
  console.log('[3/4] Encoding...');
  const framePattern = path.join(framesDir, 'frame_%06d.jpg').replace(/\\/g, '/');
  // Try multiple possible audio filenames
  const baseName = path.basename(htmlFile, '.html');
  const audioCandidates = [
    path.resolve(htmlDir, 'assets', baseName + '.mp3'),
    path.resolve(htmlDir, 'assets', baseName.replace(/_light$/, '') + '.mp3'),
    path.resolve(htmlDir, 'assets', baseName.replace(/_vertical$/, '') + '.mp3'),
  ];
  let audioPath = null;
  for (const c of audioCandidates) {
    if (fs.existsSync(c)) { audioPath = c; break; }
  }
  // Fallback: scan assets/ for any .mp3
  if (!audioPath) {
    const files = fs.readdirSync(path.join(htmlDir, 'assets')).filter(f => f.endsWith('.mp3'));
    if (files.length === 1) audioPath = path.join(htmlDir, 'assets', files[0]);
  }
  const hasAudio = !!audioPath;

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
