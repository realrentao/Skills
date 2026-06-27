#!/usr/bin/env python
"""Generate IT(normal)+CN(normal)+IT(slow -30%) combined audio for Italian teaching pages"""
import asyncio
import edge_tts
import os
import tempfile
from pydub import AudioSegment

SETS = {
    'fruit': [
        ("l'ananas",  '菠萝'),
        ("l'uva",     '葡萄'),
        ('la banana',  '香蕉'),
        ("l'arancia", '橘子'),
        ('la mela',    '苹果'),
    ],
    'numbers': [
        ('uno',     '一'),
        ('due',     '二'),
        ('tre',     '三'),
        ('quattro', '四'),
        ('cinque',  '五'),
    ],
    'color': [
        ('verde',  '绿色'),
        ('blu',    '蓝色'),
        ('rosso',  '红色'),
        ('giallo', '黄色'),
        ('viola',  '紫色'),
    ],
}

IT_VOICE = 'it-IT-ElsaNeural'
ZH_VOICE = 'zh-CN-XiaoxiaoNeural'
ASSETS = 'D:/意大利语材料/意大利语手势竖版单个/assets'
TMP = tempfile.gettempdir()

async def gen_one(text, voice, rate='+0%'):
    tmp = f'{TMP}/_tmp_{hash(text+voice+rate)}.mp3'
    try:
        comm = edge_tts.Communicate(text=text+'.', voice=voice, rate=rate)
        await comm.save(tmp)
        seg = AudioSegment.from_file(tmp)
        return seg
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

async def main():
    durations = {}
    for prefix, words in SETS.items():
        print(f'\n====== {prefix}_01 ======')
        card_durs = []
        for i, (it_text, zh_text) in enumerate(words):
            print(f'\n--- 第{i+1}词: {it_text} - {zh_text} ---')

            it1 = await gen_one(it_text, IT_VOICE, '+0%')
            print(f'  IT常速: {len(it1)/1000:.3f}s')

            cn = await gen_one(zh_text, ZH_VOICE, '+0%')
            print(f'  CN常速: {len(cn)/1000:.3f}s')

            it2 = await gen_one(it_text, IT_VOICE, '-30%')
            print(f'  IT慢速-30%: {len(it2)/1000:.3f}s')

            combined = it1 + cn + it2
            dur = len(combined) / 1000
            print(f'  组合总时长: {dur:.3f}s')
            card_durs.append(dur)

            out_path = f'{ASSETS}/{prefix}_01_0{i+1}.mp3'
            combined.export(out_path, format='mp3', bitrate='192k')

        durations[prefix] = card_durs

    print(f'\n✅ 全部完成!')
    for prefix, durs in durations.items():
        print(f'  {prefix}: {[round(d, 3) for d in durs]}')

if __name__ == '__main__':
    asyncio.run(main())
