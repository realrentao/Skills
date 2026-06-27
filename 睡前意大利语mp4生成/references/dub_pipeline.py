#!/usr/bin/env python3
"""
睡前意大利语配音流水线 — edge-tts → pydub 拼接
"""
import os, sys, json, asyncio

try:
    import edge_tts, edge_tts.communicate
    from pydub import AudioSegment
except ImportError as e:
    print(f"[错误] 缺少依赖: {e}")
    sys.exit(1)

# Monkey-patch xml:lang
_orig = edge_tts.communicate.mkssml
def patched(tc, escaped_text):
    r = _orig(tc, escaped_text)
    if 'it-IT' in tc.voice:
        r = r.replace("xml:lang='en-US'", "xml:lang='it-IT'")
    elif 'zh-CN' in tc.voice:
        r = r.replace("xml:lang='en-US'", "xml:lang='zh-CN'")
    return r
edge_tts.communicate.mkssml = patched

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEGMENTS_JSON = os.path.join(BASE_DIR, "segment_info.json")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
TEMP_DIR = os.path.join(BASE_DIR, "temp_segments")

VOICES = {
    'cn_female': 'zh-CN-XiaoxiaoNeural',
    'it_female': 'it-IT-ElsaNeural'
}
SPEED_TO_RATE = {1.0: "+0%", 0.68: "-32%"}

def prepare_text(text, voice_key):
    if voice_key == 'cn_female':
        text = text.replace("行业", "杭业")
    return text

async def gen_seg(text, voice_key, speed, idx, attempt=1):
    try:
        c = edge_tts.Communicate(
            prepare_text(text, voice_key),
            VOICES[voice_key],
            rate=SPEED_TO_RATE.get(speed, "+0%")
        )
        out_path = os.path.join(TEMP_DIR, f"seg_{idx:04d}.mp3")
        await c.save(out_path)
        # Also copy to media dir
        media_path = os.path.join(MEDIA_DIR, f"seg_{idx:04d}.mp3")
        if not os.path.exists(media_path):
            import shutil
            shutil.copy2(out_path, media_path)
        return True
    except Exception as e:
        print(f"[重试] seg_{idx:04d} 第{attempt}次失败: {e}")
        if attempt < 3:
            await asyncio.sleep(2)
            return await gen_seg(text, voice_key, speed, idx, attempt + 1)
        print(f"[失败] seg_{idx:04d} 重试3次仍失败")
        return False

async def get_audio_duration(mp3_path):
    """获取MP3文件时长（秒）"""
    audio = AudioSegment.from_mp3(mp3_path)
    return len(audio) / 1000.0

async def gen_all(segs):
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(MEDIA_DIR, exist_ok=True)
    tasks = []
    for s in segs:
        tasks.append(gen_seg(s[2], s[4], s[5], s[0] - 1))
    results = await asyncio.gather(*tasks)
    failed = sum(1 for r in results if not r)
    if failed:
        print(f"[警告] {failed} 个片段失败")
    else:
        print("[成功] 所有片段生成完成")
    
    # 获取实际时长并更新 JSON
    durations = []
    for s in segs:
        idx = s[0] - 1
        fp = os.path.join(MEDIA_DIR, f"seg_{idx:04d}.mp3")
        if os.path.exists(fp):
            d = await get_audio_duration(fp)
            durations.append(d)
            print(f"  seg_{idx:04d}: {d:.2f}s - {s[1]}")
        else:
            durations.append(s[3])
    
    # 输出带实际时长的 JSON 用于页面
    result_segs = []
    for i, s in enumerate(segs):
        result_segs.append({
            "idx": s[0],
            "desc": s[1],
            "text": s[2],
            "duration": durations[i],
            "voice": s[4],
            "speed": s[5]
        })
    
    timing_json = os.path.join(BASE_DIR, "timing.json")
    with open(timing_json, "w", encoding="utf-8") as f:
        json.dump(result_segs, f, ensure_ascii=False, indent=2)
    print(f"[信息] 时长信息已写入 {timing_json}")
    
    return durations

def concat(segs):
    """拼接完整音频"""
    result = None
    for s in segs:
        fp = os.path.join(TEMP_DIR, f"seg_{s[0]-1:04d}.mp3")
        if not os.path.exists(fp):
            continue
        if result is None:
            result = AudioSegment.from_mp3(fp)
        else:
            result += AudioSegment.silent(300)  # 300ms 间隔
            result += AudioSegment.from_mp3(fp)
    if result is None:
        print("[错误] 没有可拼接的音频")
        return
    result = result.set_frame_rate(44100)
    out_mp3 = os.path.join(BASE_DIR, "buonanotte_completa.mp3")
    result.export(out_mp3, format="mp3", bitrate="192k")
    print(f"[完成] 合成音频: {out_mp3}")

async def main():
    with open(SEGMENTS_JSON, encoding="utf-8") as f:
        segs = json.load(f)
    print(f"加载 {len(segs)} 个片段")
    
    durations = await gen_all(segs)
    concat(segs)
    
    # 总时长
    total = sum(durations) + (len(durations) - 1) * 0.3
    print(f"[信息] 总时长: {total:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
