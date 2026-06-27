# 意大利语5词教学配音格式说明

## 音频结构（每个单词）

每个单词的配音包含3个片段 + 1个间隔：

| 顺序 | 内容 | 语言 | 语速 | 说明 |
|---|---|---|---|---|
| 1 | 意大利语单词 | it-IT | +0% | 正常语速 |
| 2 | 中文翻译 | zh-CN | +0% | 标准语速 |
| 3 | 意大利语单词（慢读） | it-IT | -30% | 慢读，帮助跟读 |
| 4 | 间隔静音 | - | - | 1.5秒（1500ms） |

## edge-tts 参数

### 意大利语音色
- **Voice**: `it-IT-ElsaNeural`（女声，清晰）
- **备选**: `it-IT-IsabellaNeural`（女声，温柔）

### 中文音色
- **Voice**: `zh-CN-XiaoxiaoNeural`（女声，标准）
- **备选**: `zh-CN-YunxiNeural`（男声，标准）

### 语速控制
- **正常**: `rate="+0%"`
- **慢读**: `rate="-30%"`
- **快速**: `rate="+20%"`（不常用）

## 输出格式

- **格式**: MP3
- **采样率**: 44100 Hz
- **比特率**: 192 kbps
- **声道**: 立体声（默认）

## 谐音同音替换表

修复多音字在 edge-tts 中的错误发音：

| 汉字 | 错误发音 | 替换为 | 说明 |
|---|---|---|---|
| 长 | chang | 常 | 长短的长 |
| 重 | zhong | 崇 | 重量的重 |
| 行 | xing | 形 | 行走的行 |
| 乐 | le | 勒 | 快乐的乐 |
| 了 | le | 瞭 | 完了的了 |

在生成音频前，对中文文本应用这些替换。

## 代码示例

```python
import edge_tts
import asyncio
from pydub import AudioSegment

async def gen_segment(text, voice, rate, output_path):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

async def generate_word_audio(word_it, word_zh, phonetic):
    temp_dir = "temp_segs"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. 意大利语正常
    await gen_segment(word_it, "it-IT-ElsaNeural", "+0%", f"{temp_dir}/it.mp3")
    
    # 2. 中文（应用谐音替换）
    word_zh_fixed = apply_replacements(word_zh)
    await gen_segment(word_zh_fixed, "zh-CN-XiaoxiaoNeural", "+0%", f"{temp_dir}/zh.mp3")
    
    # 3. 意大利语慢读
    await gen_segment(word_it, "it-IT-ElsaNeural", "-30%", f"{temp_dir}/it_slow.mp3")
    
    # 拼接
    combined = AudioSegment.empty()
    for f in ["it.mp3", "zh.mp3", "it_slow.mp3"]:
        seg = AudioSegment.from_mp3(f"{temp_dir}/{f}")
        combined += seg
    
    # 添加间隔静音（1.5秒）
    silence = AudioSegment.silent(duration=1500)
    combined += silence
    
    return combined

# 拼接5个单词
final = AudioSegment.empty()
for word in words:
    seg = await generate_word_audio(word['it'], word['zh'], word['phonetic'])
    final += seg

# 导出
final.export("output.mp3", format="mp3", bitrate="192k", parameters=["-ar", "44100"])
```

## 注意事项

1. **Monkey-patch 修复**: edge-tts 默认硬编码 `xml:lang="en-US"`，需要 patch `voice_to_xml` 函数，将 `en-US` 替换为 `it-IT`。
2. **音频时长**: 使用 `pydub` 的 `len(audio)` 获取毫秒数，除以1000得到秒数。
3. **GSAP 时间线**: 根据音频实际时长精确校准，不要使用估算值。
