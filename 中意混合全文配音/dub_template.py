"""
V5 — 修正 edge-tts SSML xml:lang 硬编码 en-US → 根据语音动态设置

根因发现：
  edge_tts 内部 mkssml() 函数固定输出：
    <speak ... xml:lang='en-US'>
  
  即使用户指定了 it-IT-DiegoNeural 语音，SSML 的语言属性始终是 en-US。
  Azure TTS 服务在 en-US 语境下读意大利语，对跨语言词汇（euro, pronto,
  in totale 等）会自动切换到英语发音，导致"部分意大利语读成英语"。

修复方案：
  Monkey-patch edge_tts.communicate.mkssml，根据 voice 动态设置 xml:lang：
  - it-IT-* 语音 → xml:lang='it-IT'
  - 其他 → xml:lang='en-US'（保持默认）

其他修复（继承 v4）：
  1. 「行业」→「杭业」同音替换（绕过 phoneme 限制）
  2. edge-tts 原生 rate 参数替代 atempo（零杂音）
  3. concat 用 seg.idx-1 映射（修复 off-by-one）
"""

import asyncio
import edge_tts
import edge_tts.communicate
import os
import json
import subprocess
from pydub import AudioSegment

# ======== Monkey-patch: 修正 SSML xml:lang ========
# edge-tts 内部 mkssml 固定写死 xml:lang='en-US'
# 这里根据 voice 动态修正为正确的语言代码
_original_mkssml = edge_tts.communicate.mkssml


def patched_mkssml(tc, escaped_text):
    result = _original_mkssml(tc, escaped_text)
    # 根据 voice 判断正确的语言代码
    if 'it-IT' in tc.voice:
        result = result.replace("xml:lang='en-US'", "xml:lang='it-IT'")
    elif 'zh-CN' in tc.voice:
        result = result.replace("xml:lang='en-US'", "xml:lang='zh-CN'")
    # 其他语言保持 en-US 默认
    return result


edge_tts.communicate.mkssml = patched_mkssml


WORK_DIR = "D:/workbuddy工作区/2026-05-20-task-93/"
OUTPUT_DIR = os.path.join(WORK_DIR, "output")
TEMP_DIR = os.path.join(WORK_DIR, "temp_segments")

VOICES = {
    'cn_male': 'zh-CN-YunxiNeural',
    'it_male': 'it-IT-DiegoNeural',
    'it_female': 'it-IT-ElsaNeural'
}

SPEED_TO_RATE = {
    1.0: "+0%",
    0.68: "-32%"
}


def prepare_text(text, voice_key):
    """
    预处理文本：解决「行业」→「杭业」
    意大利语不需要额外处理（xml:lang 已通过 monkey-patch 修正）
    """
    if voice_key == 'cn_male':
        text = text.replace("行业", "杭业")
    return text


async def generate_one_segment(text, voice_key, speed, seg_idx, desc):
    """
    edge-tts 生成单个片段（含正确的 xml:lang + 原生 rate）
    """
    filename = f"seg_{seg_idx:04d}.mp3"
    outpath = os.path.join(TEMP_DIR, filename)
    voice = VOICES[voice_key]
    rate = SPEED_TO_RATE.get(speed, "+0%")

    processed_text = prepare_text(text, voice_key)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            communicate = edge_tts.Communicate(processed_text, voice, rate=rate)
            await communicate.save(outpath)
            break
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 3 * (attempt + 1)
                print(f"  ⚠️ 重试 {attempt+1}/{max_retries}... ({e})")
                await asyncio.sleep(wait)
            else:
                raise

    audio = AudioSegment.from_mp3(outpath)
    duration = len(audio) / 1000.0
    return outpath, duration


async def main():
    # ======== 第 1 步：加载片段信息 ========
    info_path = os.path.join(OUTPUT_DIR, "segment_info.json")
    with open(info_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    print("=" * 70)
    print("V5 修复方案")
    print("-" * 70)
    print("  ✅ Monkey-patch edge-tts mkssml → xml:lang 动态设置为 it-IT / zh-CN")
    print("  ✅ 「行业」→「杭业」同音替换")
    print("  ✅ edge-tts 原生 rate 参数替代 atempo（零杂音）")
    print("=" * 70)

    # ======== 第 2 步：筛选需要重新生成的片段 ========
    # V5 只重新生成意大利语片段（xml:lang 修正）+ 行业片段
    print("\n📋 重新生成的片段（xml:lang 修正 + 行业修复）：")

    to_regenerate = []

    for seg in segments:
        idx, desc, text, dur, voice_key, speed = seg
        seg_idx = idx - 1
        reason_parts = []

        if voice_key in ('it_male', 'it_female'):
            reason_parts.append("xml:lang→it-IT")
        if voice_key == 'cn_male' and '行业' in text:
            reason_parts.append("行业→杭业")

        if reason_parts:
            reason = ", ".join(reason_parts)
            to_regenerate.append((idx, text, voice_key, speed, seg_idx, desc, reason))
            print(f"  #{idx:3d} [{voice_key:10s} {speed:4.2f}x] {desc:30s} → {reason}")

    print(f"\n  共 {len(to_regenerate)} 个片段需要重新生成")

    # ======== 第 3 步：重新生成片段 ========
    print("\n" + "=" * 70)
    print("生成中（xml:lang 修正 + 原生 rate）...")
    print("=" * 70)

    ok_count = 0
    fail_count = 0

    for idx, text, voice_key, speed, seg_idx, desc, reason in to_regenerate:
        old_file = os.path.join(TEMP_DIR, f"seg_{seg_idx:04d}.mp3")
        if os.path.exists(old_file):
            os.remove(old_file)

        safe_desc = desc[:40].strip()
        print(f"\n  [#{idx}] {safe_desc}")
        display_text = prepare_text(text, voice_key)
        print(f"          {voice_key} rate={SPEED_TO_RATE.get(speed)} "
              f"xml:lang={'it-IT' if 'it' in voice_key else 'zh-CN'}")
        if len(display_text) > 60:
            display_text = display_text[:60] + "..."
        print(f"          文本: {display_text}")

        try:
            _, dur = await generate_one_segment(text, voice_key, speed, seg_idx, desc)
            print(f"  ✅ 成功 ({dur:.1f}s)")
            ok_count += 1
        except Exception as e:
            print(f"  ❌ 失败: {e}")
            fail_count += 1

    print(f"\n  成功: {ok_count}, 失败: {fail_count}")

    # ======== 第 4 步：合成最终音频 ========
    print("\n" + "=" * 70)
    print("合成最终音频...")
    print("=" * 70)

    # 按 seg.idx → file_index 映射（修复 off-by-one）
    seg_files = []
    missing = []
    for seg in segments:
        idx = seg[0]
        seg_idx = idx - 1
        fp = os.path.join(TEMP_DIR, f"seg_{seg_idx:04d}.mp3")
        if os.path.exists(fp) and os.path.getsize(fp) > 1000:
            seg_files.append(fp)
        else:
            missing.append(idx)

    if missing:
        print(f"⚠️ 缺失 {len(missing)} 个片段: {missing[:10]}...")
        if len(missing) > 10:
            print(f"   （仅显示前10个）")

    if not seg_files:
        print("❌ 无可用片段，终止")
        return

    print(f"  加载第 1 段: {os.path.basename(seg_files[0])}")
    result = AudioSegment.from_mp3(seg_files[0])

    for f in seg_files[1:]:
        result += AudioSegment.silent(duration=200)
        result += AudioSegment.from_mp3(f)

    total_duration = len(result) / 1000.0
    print(f"  总音频段数: {len(seg_files)}")
    print(f"  总时长: {total_duration:.1f}s ({total_duration/60:.1f}分钟)")

    # 导出 — 44100Hz/192kbps
    mp3_path = os.path.join(OUTPUT_DIR, "lezione1_completa_fixed_v5.mp3")
    wav_path = os.path.join(OUTPUT_DIR, "lezione1_completa_fixed_v5.wav")

    print(f"\n  导出 MP3: {mp3_path}")
    result = result.set_frame_rate(44100)
    result.export(mp3_path, format="mp3", bitrate="192k")

    print(f"  导出 WAV: {wav_path}")
    result.export(wav_path, format="wav")

    mp3_size = os.path.getsize(mp3_path)
    print(f"\n{'=' * 70}")
    print(f"✅ V5 修复完成！")
    print(f"  📁 MP3: {mp3_path} ({mp3_size/1024/1024:.1f}MB)")
    print(f"  📊 时长: {total_duration/60:.1f}分钟")
    print(f"  🎯 xml:lang 已修正为 it-IT → 意大利语发音纯正")

    # 质量验证
    result_verify = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=sample_rate,channels:format=duration,size,bit_rate',
        '-of', 'default=noprint_wrappers=1', mp3_path
    ], capture_output=True, text=True)
    print(f"\n📊 质量验证:")
    print(result_verify.stdout)


if __name__ == "__main__":
    asyncio.run(main())
