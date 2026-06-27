---
name: 课程配音制作
description: 意大利语/多语言课程配音拼接工作流：Whisper 音频识别 + 内容映射 + pydub 多片段拼接。将零散真人录音按教学逻辑编排合成完整的课程音频。
agent_created: true
---

# 课程配音制作

> 将零散真人录音按教学逻辑编排、拼接成完整课程音频的流程。
> `Whisper 转写 → 内容映射 → 编排顺序 → pydub 拼接 → 导出对照表`

---

## 触发条件

用户提到以下意图时触发：
- "做配音"、"课程配音"
- "音频拼接"、"拼接音频"
- "音频转写"、"Whisper"
- "做第X课音频"（有录音素材时）
- "识别音频"、"挑选音频"、"合并音频"

---

## 一、数据源与文件结构

### 工作区
```
D:/workbuddy工作区/2026-05-19-task-77/    # 工作目录
```

### 原始音频
```
D:/意大利语材料/意大利语美发课程全套资料/第一课音频/
```

### 逐字稿
```
D:/意大利语材料/意大利语美发课程全套资料/第01课_打招呼与电话预约_逐字稿.md
```

### 核心脚本
- `concat_lesson1.py` — 多片段拼接（改改 order 列表就能复用于其他课）

---

## 二、完整流程

### 2.1 Whisper 音频识别

用 OpenAI Whisper 批量转写音频文件：

```python
import whisper
model = whisper.load_model("medium")  # medium 兼顾准确率和速度
result = model.transcribe("filename.mp3", language=None)  # None = 自动检测
```

**注意事项**：
- 同一词的不同变调版本（如 `pronto.mp3` vs `pronto (-160).mp3`）优先用原版
- 识别结果异常的（如仅"作作"）对照原文件确认，无法判断时排除
- 意大利语词汇需人工确认识别是否正确

### 2.2 内容映射

将转写结果对照逐字稿，判断每个音频对应的教学环节：

| 命名模式 | 含义 | 示例 |
|:---|:---|:---|
| `01.mp3`, `02.mp3` 等 | 中文旁白（按教学顺序编号） | `01.mp3` → 开场白 |
| `pronto.mp3`, `buongiorno.mp3` 等 | 意大利语词汇录音，文件名即内容 | `pronto.mp3` → "Pronto" |
| `xxx (-160).mp3` | 变调版本，直接排除，用原版 | `pronto (-160).mp3` → 排除 |
| `per.mp3`, `quando.mp3` | 单字文件，被短语覆盖时排除 | 有 `Per quando_.mp3` 则 `per.mp3` 可排除 |

### 2.3 编排拼接

教学逻辑排列顺序：
```
开场 → 引入词汇 → 词汇录音 → 中文讲解 → 重复词汇 → 下一个词汇 → ...
```

每个片段间加 **200ms 静音** 让衔接自然。

### 2.4 代码模板

```python
from pydub import AudioSegment

AUDIO_DIR = "D:/意大利语材料/意大利语美发课程全套资料/第一课音频/"
OUTPUT_DIR = "D:/workbuddy工作区/2026-05-19-task-77/"

order = [
    ("01.mp3",            "📢 开场白"),
    ("02.mp3",            "📚 引入词汇"),
    ("pronto.mp3",        "🎯 Pronto"),
    ("04.mp3",            "💬 讲解：中文意思"),
    # ...
]

segments = []
for filename, desc in order:
    path = AUDIO_DIR + filename
    audio = AudioSegment.from_mp3(path)
    if segments:
        segments.append(AudioSegment.silent(duration=200))
    segments.append(audio)

result = segments[0]
for seg in segments[1:]:
    result += seg

result.export(OUTPUT_DIR + "lezione1_completa.mp3", format="mp3", bitrate="192k")
result.export(OUTPUT_DIR + "lezione1_completa.wav", format="wav")
```

### 2.5 输出内容对照表

记录每个片段的信息，格式示例：

| 序号 | 文件名 | 内容 | 时长 | 语言 |
|:---:|:---|:---|:---:|:---:|
| 1 | `01.mp3` | 开场白：课程介绍 | 30.8s | 🇨🇳 |
| 2 | `pronto.mp3` | **Pronto**（喂） | 1.6s | 🇮🇹 |

---

## 三、输出质量标准

| 检查项 | 要求 |
|:---|:---|
| 文件格式 | MP3 (192k) + WAV |
| 片段衔接 | 200ms 静音间隔 |
| 语言标注 | 对照表中标注每个片段的中/意 |
| 缺失标注 | 明确标注逐字稿中哪些环节无对应音频 |
| 排除说明 | 未用文件标注原因 |
| 时长记录 | 每个片段时长精确到 0.1s |

---

## 四、常见问题

1. **Whisper medium 对短词汇识别有限** → 单个意语词需人工确认识别结果
2. **部分环节无录音** → 标注缺失，告知用户
3. **变调版本 (-160)** → 直接排除，用原版
4. **03.mp3 录音质量异常** → 识别结果若为乱码则排除

---

## 五、Quick Start

```bash
# 1. 安装依赖
D:\Python\python.exe -m pip install pydub openai-whisper

# 2. Whisper 转写所有音频
python -c "
import whisper
m = whisper.load_model('medium')
for f in ['01.mp3', '02.mp3', ...]:
    r = m.transcribe(f, language=None)
    print(f'{f}: {r[\"text\"]}')
"

# 3. 修改 concat_lesson1.py 中的 order 列表 → 运行拼接
D:\Python\python.exe concat_lesson1.py
```
