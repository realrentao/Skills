---
name: ppt转视频完美版
description: "PPTX演示文稿+配音音频 转 完美同步MP4视频。完整流程：Whisper中文转写→按配音内容节奏分配翻页时间→逐动画手工微调TriggerDelayTime→CreateVideo导出→FFmpeg合并。触发词：PPT转视频、配音同步、翻页视频、PPT配音、动画对不上、教学视频"
agent_created: true
---

# PPT转视频完美版 技能

PPTX + MP3/M4A → 精确同步MP4视频。保留PPT原始设计+全部动画特效。

## 何时使用

- "把PPT做成视频"
- "PPT翻页跟配音保持一致"
- "保留PPT自带特效" / "动画对不上配音"
- "PPT配音同步"
- 涉及 PPTX 文件 + 音频文件 → MP4 视频

## 已验证课程

- 第01课_打招呼与电话预约（15页，144动画，11分钟）
- 第02课_发质判断（19页，170+动画，12分钟）

## 核心工作流（5步）

### 第1步：分析PPT内容和动画结构

```python
import win32com.client
ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True; ppt.WindowState = 1
pres = ppt.Presentations.Open("input.pptx")

for i in range(1, pres.Slides.Count + 1):
    slide = pres.Slides(i)
    seq = slide.TimeLine.MainSequence
    print(f"第{i}页: {seq.Count}个动画")
    for j in range(1, seq.Count + 1):
        effect = seq.Item(j)
        shape = effect.Shape
        text = shape.TextFrame.TextRange.Text.strip()[:60] if shape and shape.HasTextFrame else ""
        print(f"  动画{j}: {text}")
```

记录：总页数、各页动画数、动画文字内容。

### 第2步：转录音频（中文模型）

```python
import whisper
model = whisper.load_model('base')
result = model.transcribe('audio.mp3', language='zh')
for seg in result['segments']:
    print(f"[{seg['start']:.1f}s] {seg['text']}")
```

**关键**：用 `language='zh'`，不是其他语言。中文模型即使对意大利语音译不准确，中文内容完全准确。

### 第3步：分析配音节奏，确定翻页时间

**核心原则**：配音讲解顺序≠PPT页面顺序。翻页时间=配音提到该页内容的时间。

从转录中找出关键词：
- "第一组" "第一个词" → 词汇页翻页时机
- "第一轮" "第二轮" → 对话页翻页时机
- "语法一" "语法二" → 语法页翻页时机
- "第一句" "必背" → 句子页翻页时机

```python
SWITCH = {1:0, 2:32, 3:50, ...}  # 翻页时间
```

总时长验证：`sum(各页停留时间)` ≈ 音频实际时长（ffprobe测得）

### 第4步：设置逐动画精确触发

根据动画文字内容和转录时间点，手动计算每个动画的延迟时间：

```python
# 相对于翻页时刻的触发延迟（秒）
DELAYS = {
    3: [0,0, 4.0, 5.5, 7.0,     # 词1 (配音说"第一个词"时触发)
        0,0, 40.0, 41.5, 43.0],  # 词2
}

for page, delays in DELAYS.items():
    slide = pres.Slides(page)
    slide.SlideShowTransition.AdvanceOnTime = True
    slide.SlideShowTransition.AdvanceTime = page_duration
    
    seq = slide.TimeLine.MainSequence
    for j in range(1, seq.Count + 1):
        d = delays[j-1] if j-1 < len(delays) else 0
        e = seq.Item(j)
        e.Timing.TriggerType = 2  # msoAnimTriggerWithPrevious
        e.Timing.TriggerDelayTime = d
```

**动画分组技巧**：装饰元素(0s) → 意大利语(配音讲到时) → 中文释义(+1.5s)

### 第5步：导出视频 + 替换音频

```python
pres.SlideShowSettings.AdvanceMode = 1
pres.CreateVideo(video_path, True)  # 位置参数！
# 轮询文件大小直到稳定

import os
os.system(f'ffmpeg -y -i "{video_path}" -i "{audio_path}" '
          f'-c:v copy -c:a aac -b:a 192k '
          f'-map 0:v:0 -map 1:a:0 -shortest '
          f'-movflags +faststart "{final_path}"')
```

## 关键陷阱

1. **翻页时间≠页面内容时长**：配音讲词汇时PPT可能停在目标页。翻页时间=配音讲该页内容的时间。

2. **中文模型转写**：`language='zh'` 质量远超其他语言。

3. **CreateVideo位置参数**：`pres.CreateVideo(path, True)` 不能用关键字。

4. **PowerPoint窗口必须可见**：`Visible = True, WindowState = 1`。

5. **TriggerDelayTime**：相对于翻页时刻（不是绝对时间0）。

6. **WPS不可用**：SaveAs MP4仅574KB废片。

7. **总时长校验**：`sum(各页AdvanceTime)` 必须 ≈ 音频时长，否则FFmpeg -shortest会截断。

8. **PPT嵌入媒体问题**：如PPT含嵌入音频，CreateVideo可能立刻status=4失败，需删除嵌入媒体再导出。
