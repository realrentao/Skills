#!/usr/bin/env python3
"""
重复合成音频 — 按照 HTML GSAP timeline 的精确时间间隔拼接
确保音频时间轴与画面时间轴完全一致
"""
import os, json
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "media")

# 从 timing.json 读取实际时长
with open(os.path.join(BASE_DIR, "timing.json"), "r", encoding="utf-8") as f:
    segs = json.load(f)

DURATIONS = [s["duration"] for s in segs]
GAP = 0.3            # 同一句话内的段间隔
GAP_SENTENCE = 2.0   # 句子之间的间隔
INTRO_DUR = 2.0      # 开场动画时长（静音）

# 计算每段在时间轴上的精确位置
segments = []
cursor = 0
for i in range(len(DURATIONS)):
    sent_idx = i // 3
    is_last = (i % 3 == 2)
    gap = GAP_SENTENCE if (is_last and i < len(DURATIONS) - 1) else GAP
    segments.append({
        "seg_idx": i,
        "start": cursor,
        "duration": DURATIONS[i],
        "end": cursor + DURATIONS[i],
        "gap_after": gap
    })
    cursor += DURATIONS[i] + gap

total_audio_dur = cursor
total_video_dur = INTRO_DUR + total_audio_dur + 2.0  # 含淡出

print(f"音频部分时长: {total_audio_dur:.3f}s")
print(f"视频总时长: {total_video_dur:.3f}s (开场{INTRO_DUR}s + 音频{total_audio_dur:.3f}s + 淡出2s)")

# 按时间轴拼接音频
# 先加 INTRO_DUR 的静音（开场动画）
result = AudioSegment.silent(duration=int(INTRO_DUR * 1000))

audio_cursor_ms = INTRO_DUR * 1000  # 当前时间轴位置（ms）

for i, seg in enumerate(segments):
    # 加上间隔静音（第一段无间隔）
    seg_start_ms = INTRO_DUR * 1000 + seg["start"] * 1000
    gap_needed = seg_start_ms - len(result)
    if gap_needed > 0:
        result += AudioSegment.silent(duration=gap_needed)

    # 加载该段音频
    fp = os.path.join(MEDIA_DIR, f"seg_{i:04d}.mp3")
    if not os.path.exists(fp):
        print(f"  [警告] 缺少 {fp}")
        continue

    audio = AudioSegment.from_mp3(fp)
    result += audio
    print(f"  段{i:2d}: 位置 {len(result)/1000:.3f}s, 音频 {DURATIONS[i]:.3f}s ({segs[i]['desc']})")

# 确保总长度覆盖视频总时长
target_ms = int(total_video_dur * 1000)
if len(result) < target_ms:
    result += AudioSegment.silent(duration=target_ms - len(result))

result = result.set_frame_rate(44100)
out_path = os.path.join(BASE_DIR, "buonanotte_completa_synced.mp3")
result.export(out_path, format="mp3", bitrate="192k")
print(f"\n[完成] 精确同步音频: {out_path} ({len(result)/1000:.1f}s)")

# 同时覆盖原文件
import shutil
shutil.copy2(out_path, os.path.join(BASE_DIR, "buonanotte_completa.mp3"))
print(f"[完成] 已覆盖 buonanotte_completa.mp3")
