---
name: 中意混合全文配音
description: 用 edge-tts 生成中意双语教学课程全文配音。核心：Monkey-patch 修复 edge-tts xml:lang 硬编码 en-US → 意大利语发音纯正。含多音字同音替换、原生 rate 控速、44100Hz/192kbps 输出。
agent_created: true
version: 1.1.0
---

# 中意混合全文配音

> edge-tts 生成中意双语教学课程全文配音的完整流水线。
> `segment_info.json → edge-tts (xml:lang 修正) → pydub 拼接 → 44100Hz/192kbps`

---

## 触发条件

- "做第X课配音"、"生成配音"
- "中意双语配音"、"意大利语课程配音"
- "用 edge-tts 生成"、"全文 TTS"
- 提供了 `segment_info.json` + 要求全文合成
- 用户反馈"发音不对"、"意大利语像英语"、"杂音"
- 用户反馈"意大利语用的是英语配音"、"有英式发音"

---

## 一、核心发现：edge-tts xml:lang 硬编码Bug

### 问题

edge-tts v7.2.8 内部 `mkssml()` 函数**固定写死**：

```python
# edge_tts/communicate.py
def mkssml(tc, escaped_text):
    return (
        "<speak ... xml:lang='en-US'>"   # ← 无论什么语音，始终 en-US！
        f"<voice name='{tc.voice}'>"
        ...
    )
```

后果：
- `it-IT-DiegoNeural` 语音 → SSML `xml:lang='en-US'` → Azure TTS 在英语语境下读意大利语
- 跨语言词汇（euro, pronto, in totale）被读成英语发音
- 之前所有用 `<speak xml:lang="it-IT">` 包装文本的方法均无效（edge-tts 内部覆盖）

### 修复：Monkey-patch

```python
import edge_tts.communicate

_original_mkssml = edge_tts.communicate.mkssml

def patched_mkssml(tc, escaped_text):
    result = _original_mkssml(tc, escaped_text)
    if 'it-IT' in tc.voice:
        result = result.replace("xml:lang='en-US'", "xml:lang='it-IT'")
    elif 'zh-CN' in tc.voice:
        result = result.replace("xml:lang='en-US'", "xml:lang='zh-CN'")
    return result

edge_tts.communicate.mkssml = patched_mkssml
```

⚠️ **必须在所有 `Communicate` 调用之前执行此 monkey-patch。**

---

## 二、完整流程

### 2.1 输入：segment_info.json

结构定义：
```json
[
  [编号, 描述, 文本内容, 预估时长秒, 语音类型, 速度],
  [1, "开场意语", "Ciao a tutti! ", 2.0, "it_male", 1.0],
  [2, "开场中文", "大家好！", 1.6, "cn_male", 1.0],
  [15, "词1慢读", "pronto", 2.5, "it_male", 0.68]
]
```

字段说明：
| 字段 | 说明 | 示例 |
|------|------|------|
| 编号 | 从1开始的序号 | 1 |
| 描述 | 片段用途说明 | "开场意语" |
| 文本 | TTS 朗读的原始文本 | "Ciao a tutti!" |
| 预估时长 | 仅供参考的预估秒数 | 2.0 |
| 语音类型 | `cn_male` / `it_male` / `it_female` | it_male |
| 速度 | 1.0=正常，0.68=慢速（学员跟读） | 0.68 |

### 2.2 语音映射

```python
VOICES = {
    'cn_male': 'zh-CN-YunxiNeural',
    'it_male': 'it-IT-DiegoNeural',
    'it_female': 'it-IT-ElsaNeural'
}
```

### 2.3 多音字处理

**问题**：`zh-CN-YunxiNeural` 读 "行业" 为 xíng yè（正确应为 háng yè）；读 "发" 为 fā（第一声，实际应为 fà 第四声）。

**方案**：文本层面同音字替换——比 SSML `<phoneme>` 标签更可靠（edge-tts 不解析标签内容）。

```python
def prepare_text(text, voice_key):
    if voice_key == 'cn_male':
        text = text.replace("行业", "杭业")  # 杭 = háng
        # ⚠️ 不要替换"发"→"髮" — Azure TTS 不认识繁体"髮"字，会导致"No audio received"
        # "发(fà)"拼音标注同样触发拒绝；直接保留简体"发"最安全
    return text
```

**关键经验**：
- 行业→杭业：安全可用，Azure TTS 接受
- ~~发→髮~~ **已废弃（2026-06-02）**：繁体"髮"导致 Azure TTS 返回 "No audio received"
- "发(fà)" 拼音标注同样会触发 Azure TTS 拒绝
- 美发课程中直接保留简体"发"字，zh-CN-YunxiNeural 在上下文中大多数情况能读 fà

通用规则：
| 原词 | 替换为 | 原因 |
|------|--------|------|
| 行业 (xíng yè) | 杭业 (háng yè) | 杭 = háng |
| 发 | （不做替换） | Azure TTS 不认识髮字，拼音标注也会导致拒绝 |

### 2.4 慢速控制：原生 rate

**问题**：ffmpeg atempo 后处理 → 24000→44100Hz 重采样 → 杂音。

**方案**：edge-tts 原生 `rate` 参数，TTS 引擎内部处理，零音质损失。

```python
SPEED_TO_RATE = {
    1.0: "+0%",     # 正常速度
    0.68: "-32%"    # 68% 慢速（学员跟读）
}
```

### 2.5 生成片段

```python
async def generate_one_segment(text, voice_key, speed, seg_idx):
    voice = VOICES[voice_key]
    rate = SPEED_TO_RATE.get(speed, "+0%")
    processed_text = prepare_text(text, voice_key)
    
    communicate = edge_tts.Communicate(processed_text, voice, rate=rate)
    await communicate.save(f"temp_segments/seg_{seg_idx:04d}.mp3")
```

### 2.6 🌟 关键改进（v2）：意语单词必须独立发音

**问题**：v1 阶段，中文段落混入意大利语单词的片段（如 `cn_male` 读 "接电话第一句就说 Pronto"），`zh-CN-YunxiNeural` 会把 `Pronto` 读成英语发音。

**方案**：**所有意大利语单词/短语必须拆成独立片段**，用 `it_male` / `it_female` 发音，决不可混入 `cn_male` 文本。

```python
# ❌ 错误：中意混合段
add("词1_解释", "接电话第一句就说 Pronto", ..., "cn_male")
# → Pronto 被中文语音读成英语

# ✅ 正确：拆分为中文→意语→中文
add("词1_解释2", "接电话第一句就说：", ..., "cn_male")
add("词1_示范", "Pronto！", ..., "it_male")
add("词1_解释3", "记住了吗？", ..., "cn_male")
# → Pronto 由 DiegoNeural 标准意语发音
```

**分词粒度参考**：第01课（约288行配音稿）v1 = 71段 → v2 = 214段 → v3 = 217段。
**第02课经验**：第02课（202行配音稿）v1 = 214段 → v2 = 261段。即使中文解释段中提及意语单词（如"注意 parrucchiere 是男理发师"），也要把意语词拆出独立 it_male 发音。拆分粒度可细化到单个单词级别（如 parrucchiere、Tuoi、capelli 等）。

#### 自动检查：扫描 cn_male 段是否还有意语残留

每次写完 `gen_segments_v2.py` 后，建议运行以下检查，确保没有遗漏：

```python
# 检查 cn_male 段中是否混有意语单词
ITALIAN_WORDS = ['Pronto','pronto','Buongiorno','buongiorno','Buonasera',
    'l\'appuntamento','Vorrei','prendere','Quanto','costa','taglio','piega',
    'giovedì','Pomeriggio','arrivederci','Arrivederci',
    'Per quando','Va bene','Non va','euro','In totale',
    'A giovedì','Ciao','Alle','perfetto',
    'capelli','fini','spessi','grassi','secchi','danneggiati','crespi','stressati',
    'radice','lunghezza','punte','Doppie','forfora','parrucchiere','parrucchiera',
    'cliente','salone','lavandino','Sì','specifico',
    'Venga','Vieni','Guardi','Guarda','Accomodati','Siediti','Hai',
    'tantissimi','facciamo','vediamo','Prima','shampoo',
    'acqua','calda','pressione','Usiamo','senza','solfati',
    'magari','colore','tuoi','Tuoi','sono','molto',
    'accomodi','Vuole','sedere','qui']

import json
with open('segment_info.json') as f:
    segs = json.load(f)
for s in segs:
    if s[4] == 'cn_male':
        for w in ITALIAN_WORDS:
            if w in s[2]:
                print(f'⚠️ #{s[0]} cn_male 含意语: "{s[2][:50]}"')
```

### 2.7 Python 字符串引号处理

在大段中文文本中常出现中文双引号  `"` / `"`（U+201C/U+201D），在 Python 代码中写为 `"" "你好" ""时，不可靠且易混淆。

**推荐方案**：使用独立的 `gen_segments_v2.py` 脚本生成 `segment_info.json`，主流水线读 JSON 而非嵌入 Python 代码，彻底规避引号问题。

```python
# gen_segments_v2.py 片段示例
add("语法一_拆_per_中", 
    "等于\u201c对于\u201d。",  # ← 使用 Unicode 转义，无歧义
    ..., "cn_male")
```

### 2.8 ⚠️ 拆段避坑：不要产生孤立标点

分段时，**纯标点/极短文本的独立片段会导致 Azure TTS 返回 "No audio received" 错误**。

```python
# ❌ 错误：纯标点独立成段
add("句号", "。", 0.3, "cn_male")    # ← Azure TTS 无法处理

# ✅ 正确：合并到相邻段落
add("意语+euro", "euro。", 1.0, "it_male")  # 标点交给发声段处理
```

**经验**：
- 纯标点片段（`"。"` `"， "` `"？"`）不要独立成段
- 极短文本（< 3个中文字符）也可能被 TTS 跳过 → 合并到上下文
- 中文标点如`）。`、`！`独立成段同样会触发 "No audio received" → 合并到相邻的 it_male 段
- 分割后用脚本检查：任何 `len(text.strip()) <= 2` 的 cn_male 段都需要合并

### 2.9 🔁 Azure TTS 限流与重试

大量片段并行生成时（200+ 段），Azure TTS 可能返回限流错误 `"No audio was received"`。

**方案**：
1. 失败片段自动重试（最多3次，间隔2秒）
2. 重试仍然失败的片段单独再跑
3. 所有重试成功后重新拼接即可，无需重跑全部

```python
async def retry_one(text, voice, rate, out_path, attempt=1):
    try:
        c = edge_tts.Communicate(text, voice, rate=rate)
        await c.save(out_path)
        return True
    except Exception:
        if attempt < 3:
            await asyncio.sleep(2)
            return await retry_one(text, voice, rate, out_path, attempt + 1)
        return False
```

### 2.10 合成最终音频

⚠️ **concat 必须用 `idx - 1` 映射文件索引**，不能用 `range(len(segments))`：
segment_info.json 的编号可能有间隔（如缺失 #91），`range(len)` 会导致索引错位。

```python
from pydub import AudioSegment

seg_files = []
for seg in segments:
    idx = seg[0]      # 编号 1-198
    seg_idx = idx - 1 # 文件索引 0-197
    fp = f"temp_segments/seg_{seg_idx:04d}.mp3"
    if os.path.exists(fp):
        seg_files.append(fp)

result = AudioSegment.from_mp3(seg_files[0])
for f in seg_files[1:]:
    result += AudioSegment.silent(duration=200)  # 200ms 间隔
    result += AudioSegment.from_mp3(f)

result = result.set_frame_rate(44100)
result.export("lezione1_completa.mp3", format="mp3", bitrate="192k")
result.export("lezione1_completa.wav", format="wav")
```

---

## 三、输出质量标准

| 检查项 | 要求 |
|:---|:---|
| 采样率 | 44100 Hz |
| 比特率 | 192 kbps |
| 格式 | MP3 + WAV |
| 片段衔接 | 200ms 静音间隔 |
| 意大利语发音 | xml:lang='it-IT'（monkey-patch 保证） |
| 多音字 | 优先同音字替换（杭业/髮）；也可用 (pinyin) 括号标注法（如 得(dei3)），非SSML，edge-tts 会按标注发音 |
| 慢速片段 | 原生 rate 参数，不用 atempo |
| concat 索引 | `idx - 1` 映射，不用 `range(len)` |
| 中文语音 | `zh-CN-YunxiNeural` |
| 意语男声 | `it-IT-DiegoNeural` |
| 意语女声 | `it-IT-ElsaNeural` |
| 意语独立发音 | 意语单词不得混入 cn_male 段，必须拆成独立 it_male/female 片段 |
| 无孤立标点段 | 纯标点/极短文本段（< 3字符）不得独立，需合并到相邻段落 |
| 限流容错 | 失败片段自动重试（最多3次） |

---

## 四、推荐工作流（v2）

### 4.1 步骤

1. **生成分段 JSON**：用 `gen_segments_v2.py`（可复用）生成本课的 `segment_info.json`
   - 严格分离中意文本：所有意语单词用 `it_male`/`it_female` 独立发音
   - 中文双引号使用 Unicode 转义 `\u201c` `\u201d` 避坑
2. **运行配音流水线**：用 `dub_pipeline.py` 读取 JSON → edge-tts → pydub 拼接
3. **检查输出**：确认无英式发音的意大利语

### 4.2 流水线代码模板

完整模板位于 `dub_pipeline.py`，内容如下：

```python
#!/usr/bin/env python3
"""
中意混合全文配音流水线
读取 segment_info.json → edge-tts (xml:lang 修正) → pydub 拼接 → 44100Hz/192kbps
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

OUTPUT_DIR = r"D:\意大利语材料\...\第XX课音频"
SEGMENTS_JSON = os.path.join(OUTPUT_DIR, "segment_info.json")
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp_segments")

VOICES = {
    'cn_male': 'zh-CN-YunxiNeural',
    'it_male': 'it-IT-DiegoNeural',
    'it_female': 'it-IT-ElsaNeural'
}
SPEED_TO_RATE = {1.0: "+0%", 0.68: "-32%"}

def prepare_text(text, voice_key):
    if voice_key == 'cn_male':
        text = text.replace("行业", "杭业")
        # ⚠️ 不要用"发→髮"或"发(fà)" — Azure TTS 会拒绝
    return text

async def gen_seg(text, voice_key, speed, idx, attempt=1):
    try:
        c = edge_tts.Communicate(
            prepare_text(text, voice_key),
            VOICES[voice_key],
            rate=SPEED_TO_RATE.get(speed, "+0%")
        )
        await c.save(os.path.join(TEMP_DIR, f"seg_{idx:04d}.mp3"))
        return True
    except Exception:
        if attempt < 3:
            await asyncio.sleep(2)
            return await gen_seg(text, voice_key, speed, idx, attempt + 1)
        print(f"[失败] seg_{idx:04d} 重试3次仍失败")
        return False

async def gen_all(segs):
    results = await asyncio.gather(*[
        gen_seg(s[2], s[4], s[5], s[0]-1) for s in segs
    ])
    failed = sum(1 for r in results if not r)
    if failed:
        print(f"[警告] {failed} 个片段失败，需手动重试")

def concat(segs, base):
    result = None
    for s in segs:
        fp = os.path.join(TEMP_DIR, f"seg_{s[0]-1:04d}.mp3")
        if not os.path.exists(fp):
            continue
        if result is None:
            result = AudioSegment.from_mp3(fp)
        else:
            result += AudioSegment.silent(200)
            result += AudioSegment.from_mp3(fp)
    result = result.set_frame_rate(44100)
    result.export(f"{OUTPUT_DIR}/{base}_completa.mp3", format="mp3", bitrate="192k")
    result.export(f"{OUTPUT_DIR}/{base}_completa.wav", format="wav")

def main():
    os.makedirs(TEMP_DIR, exist_ok=True)
    with open(SEGMENTS_JSON) as f:
        segs = json.load(f)
    print(f"加载 {len(segs)} 个片段")
    asyncio.run(gen_all(segs))
    concat(segs, "lezioneXX")

if __name__ == "__main__":
    main()
```

脚本自动完成：
1. monkey-patch `mkssml`（xml:lang 修正）
2. 读取外部 `segment_info.json`
3. 并发生成所有片段
4. pydub 拼接 + 导出 44100Hz/192kbps

---

## 五、常见问题

1. **意大利语像英语** → 检查 monkey-patch 是否在 `Communicate` 之前执行
2. **意大利语单词被中文语音读成英语** → 意语单词必须拆成独立 it_male/female 片段，不可混入 cn_male 文本
3. **音频"乱码"（发闷）** → 检查采样率是否为 44100Hz，不要用 atempo 生成慢速片段
4. **多音字（行业 → xíng yè）** → 优先用同音字替换（杭业）；也可以直接在文本中加 (pinyin) 括号标注，如 "得(dei3)分两步做"——非 SSML，edge-tts 会按标注发音
5. **No audio received / Azure TTS 限流** → 加重试机制（重试最多3次，间隔2秒）；极短片段（纯标点如 `"。 "`）会导致失败，需合并到相邻段落
6. **末段丢失** → concat 循环用 `idx-1` 映射而非 `range(len)`
7. **SSML 标签不生效** → edge-tts v7 不解析用户传入的 SSML，所有标签当作文本朗读（时长膨胀 8.7x）
8. **Python SyntaxError（中文引号问题）** → 用 `gen_segments_v2.py` 生成外部 JSON 替代内嵌 Python 字符串
9. **edge-tts 升级后 monkey-patch 失效** → 检查新版本 `mkssml()` 签名是否变化
10. **"发→髮"替换导致 "No audio received"（2026-06-02 发现）** → Azure TTS 不认识繁体"髮"字，zh-CN-YunxiNeural 会拒绝该文本。同样"发(fà)"拼音标注也会被拒绝。直接保留简体"发"字最安全，YunxiNeural 在美发课上下文中大多数情况能读 fà

---

## 六、Quick Start

```bash
# 1. 安装依赖
D:\Python\python.exe -m pip install edge-tts pydub

# 2. 编写分段生成脚本 gen_segments_v2.py
#    - 严格分离中意文本（意语单词独立 it_male/female 发音）
#    - 中文双引号用 Unicode 转义 \u201c \u201d
#    - 输出到 OUTPUT_DIR/segment_info.json

# 3. 运行分段生成
D:\Python\python.exe gen_segments_v2.py

# 4. 修改 dub_pipeline.py 中的 OUTPUT_DIR 路径

# 5. 运行配音流水线
D:\Python\python.exe dub_pipeline.py
```

### 注意事项

- **意语单词必须独立发音**：这是 v2 最关键的改进——中文语音无法读好意大利语，所有意语词/短语必须拆成独立片段
- **每次写完 gen_segments 后先扫描一遍**：用 §2.6 的自动检查脚本扫描 cn_male 段是否还有意语残留
- **避免孤立标点段**：纯标点独立成段会导致 TTS 失败，合并到相邻段落
- **推荐 JSON 分离架构**：分段定义写到独立的 generator 脚本→输出 JSON→流水线读 JSON，避免 Python 引号冲突
- **并发限流**：200+ 段并行生成可能触发 Azure TTS 限流，流水线模板已内置重试（最多3次）
- **每课配音稿约 288 行 → 约 200+ 段**：分段越细，发音越准
