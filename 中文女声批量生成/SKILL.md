---
title: "中文女声批量生成"
summary: "批量生成中文命名的多语言女声音频（MP3），文件名用中文，朗读内容任意"
version: "1.0.0"
---

# 中文女声批量生成

用 edge-tts 批量生成 MP3 音频。文件名用中文句子，朗读内容可以是任意语言（外语翻译等），适合「睡前意大利语1000句」这类双语学习材料的音频制作场景。

## 核心逻辑

1. **默认发音人**：`it-IT-IsabellaNeural`（意大利女声），可在脚本中修改 `VOICE` 变量切换为中文女声 `zh-CN-XiaoxiaoNeural` 或其他
2. **输入格式**：`(中文文件名, 朗读文本)` 对 — 文件名用来命名 `.mp3`，朗读文本是实际 TTS 的内容
3. **命名规则**：`中文句子.mp3`，保留原文标点（！？。，等）
4. **输出目录**：用户指定的目标目录

## 触发场景

- "给这些句子批量生成音频"
- "参考XX音频音色，生成音频，命名方式一样"
- 用户提供中文句子列表 + 参考音频

## 执行步骤

### 1. 确认环境

```
pip install edge-tts
```

### 2. 准备数据

句子列表格式：
```python
sentences = [
    ("中文文件名", "实际朗读内容"),
    ("晚上好！", "Buonasera!"),
]
```

### 3. 生成脚本模板

```python
import asyncio, os

TARGET = "目标目录"
VOICE = "it-IT-IsabellaNeural"   # 根据需要替换

sentences = [
    ("中文文件名", "朗读文本"),
]

async def gen():
    for cn_name, text in sentences:
        normal = os.path.join(TARGET, f"{cn_name}.mp3")
        temp  = os.path.join(TARGET, f"_temp_{cn_name}.mp3")

        print(f"▶ [{cn_name}] -> {text}")
        p = await asyncio.create_subprocess_exec(
            "edge-tts", "--voice", VOICE, "--text", text, "--write-media", temp
        )
        await p.communicate()

        if os.path.exists(temp):
            if os.path.exists(normal):
                os.remove(normal)
            os.rename(temp, normal)
            print(f"  ✓ {cn_name}.mp3")

    for f in os.listdir(TARGET):
        if f.startswith("_temp_"):
            os.remove(os.path.join(TARGET, f))

asyncio.run(gen())
```

### 4. 运行

```bash
python 脚本.py
```
