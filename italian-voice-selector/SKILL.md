---
name: italian-voice-selector
description: 意大利语配音音色选择。当用户输入意大利语文本并指定音色（或让AI选择音色），使用 edge-tts 生成对应音频。触发词：意大利语配音、音色选择、意大利语音色、语音生成、TTS、配音音色。
agent_created: true
---

# 意大利语配音音色选择

## 概览

通过 edge-tts 为意大利语文本生成配音音频。用户输入文字 + 指定（或由 AI 推荐）音色，输出 MP3 音频文件。

## 可用音色

| 别名 | edge-tts Voice ID | 性别 | 特点 |
|------|-------------------|------|------|
| elena | `it-IT-ElsaNeural` | 女声 | 微软神经网络，音质好，任意文本 100% 成功 |
| isabella | `it-IT-IsabellaNeural` | 女声 | 微软神经网络，自然流畅 |
| cosimo | `it-IT-DiegoNeural` | 男声 | 微软神经网络，沉稳 |
| giuseppe | `it-IT-GiuseppeMultilingualNeural` | 男声 | 多语言支持，适合混合语境 |

所有音色无需任何凭证，任意文本可用。

## 使用方式

### 方式一：用户指定音色

用户说"用 elena 配这段文字：Buongiorno e benvenuti"时：

1. 从表格按别名或直接按 voice ID 匹配音色
2. 用 edge-tts 生成音频
3. 交付 MP3 文件

核心代码（直接执行，无需创建脚本文件）：

```python
import asyncio, edge_tts
voice_id = "it-IT-ElsaNeural"  # 从表格获取
text = "Buongiorno e benvenuti"
output_path = "output.mp3"
communicate = edge_tts.Communicate(text, voice_id)
asyncio.run(communicate.save(output_path))
```

### 方式二：不指定音色（AI 推荐）

用户只说"把这句配成意大利语配音：..."时：

1. 根据文本内容推荐合适的音色：
   - 女教师/课程讲解类 → elena（女声，清晰标准）
   - 男声对话类 → cosimo 或 giuseppe
   - 多语言混合 → giuseppe（多语言支持）
2. 告知用户选择的音色
3. 生成并交付音频

## 注意事项

- edge-tts 已安装在 `D:\Python\python.exe` 环境
- 使用系统 Python 路径：`D:\Python\python.exe`
- 生成的音频默认保存在当前工作目录，文件名用 sanitized text
- 如需批量处理，推荐使用 `italian_tts_batch.py` 脚本（位于项目根目录）
