---
title: "SKILL.md"
summary: "意大利语音频批量生成 — 三语速 MP3 生成工作流"
read_when:
  - 用户需要为意大利语句子批量生成 MP3 音频文件
  - 用户提到"三语速""250""-160""生成音频""意大利语发音"
---

# 意大利语音频批量生成

该 skill 使用 edge-tts + ffmpeg 为意大利语句子批量生成三种语速（正常/快速/慢速）的 MP3 音频文件，命名规则与指定目录中的参考文件保持一致。

## 核心逻辑

1. **发音人**：`it-IT-IsabellaNeural`（女性意大利语发音人），与参考文件音色一致
2. **三种语速**：
   - 正常语速：edge-tts 直接输出，后缀为 `.mp3`
   - 快速语速：ffmpeg atempo=1.48，后缀为 `(250).mp3`
   - 慢速语速：ffmpeg atempo=0.686，后缀为 `(-160).mp3`
3. **文件名规范化**：
   - 问号 `?` → 下划线 `_`
   - 保留其他特殊字符（`!` `.` `'` `è` `ì` 等）
   - 句尾句号保留在文件名中（如 `Sono triste..mp3` 正常）
4. **目标目录**：根据用户指定的路径或默认的 `音频/XX-YY句/` 目录

## 执行步骤

### 1. 确认环境
- 确保 `edge-tts` 已安装（`pip install edge-tts`）
- 确保 `ffmpeg` 可用（包含 `ffprobe`）
- 确认目标目录存在

### 2. 读取用户提供的句子列表
- 句子按行分割或从用户输入提取
- 每句数量不限

### 3. 生成音频（Python asyncio 脚本）

```python
import asyncio
import subprocess
import os

VOICE = "it-IT-IsabellaNeural"
TEMPO_FAST = 1.48    # 快速倍率
TEMPO_SLOW = 0.686   # 慢速倍率

def sanitize_filename(text: str) -> str:
    """文件名规范化"""
    return text.replace("?", "_").replace("/", "_").replace("\\", "_")

async def generate_sentence(sentence: str, target_dir: str):
    base = sanitize_filename(sentence)
    normal_file = os.path.join(target_dir, f"{base}.mp3")
    fast_file = os.path.join(target_dir, f"{base}(250).mp3")
    slow_file = os.path.join(target_dir, f"{base}(-160).mp3")
    temp_file = os.path.join(target_dir, f"_temp_{base}.mp3")

    # 生成正常语速
    proc = await asyncio.create_subprocess_exec(
        "edge-tts", "--voice", VOICE, "--text", sentence,
        "--write-media", temp_file
    )
    await proc.communicate()

    # 复制为正常版
    os.rename(temp_file, normal_file)

    # 生成快速版
    fast_temp = os.path.join(target_dir, f"_fast_{base}.mp3")
    subprocess.run(["ffmpeg", "-y", "-i", normal_file,
        "-filter:a", f"atempo={TEMPO_FAST}",
        "-codec:a", "libmp3lame", "-q:a", "2", fast_temp])
    os.rename(fast_temp, fast_file)

    # 生成慢速版
    slow_temp = os.path.join(target_dir, f"_slow_{base}.mp3")
    subprocess.run(["ffmpeg", "-y", "-i", normal_file,
        "-filter:a", f"atempo={TEMPO_SLOW}",
        "-codec:a", "libmp3lame", "-q:a", "2", slow_temp])
    os.rename(slow_temp, slow_file)
```

### 4. 清理临时文件
删除 `_temp_*`, `_fast_*`, `_slow_*` 临时文件。

### 5. 验证（可选）
使用 `ffprobe` 检查音频时长，确认三速比例符合预期：
- 快速版时长 ≈ 正常版 × (1/1.48) ≈ 正常版 × 0.676
- 慢速版时长 ≈ 正常版 × (1/0.686) ≈ 正常版 × 1.458

## 触发指令示例

- "给这些意大利语句子生成三语速音频"
- "生成音频，参考 XXX.mp3 的音色和命名方式"
- "每句话生成三个速度版本"
