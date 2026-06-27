---
name: batch-image-resize
description: 批量图像转正+缩放技能。用户说"转正"、"修方向"、"图片横向像素1080"、"批量处理图片"时触发。读取用户已有脚本 `D:\Spyer项目\图像转正修改尺寸.py`，通过 Agent 工具执行。
agent_created: true
---

# batch-image-resize

批量图像转正 + 缩放到指定宽度的技能。

## 触发条件

用户提到以下意图时触发：
- "图片转正"、"转正"
- "修方向"、"修正方向"
- "横向像素1080"、"缩放到1080"
- "批量处理图片"（图像相关时）
- "用那个脚本"、"用你记住的脚本处理"

## 执行方式

用 Agent 工具执行脚本：

```
prompt: 请用 D:\Python\python.exe 执行以下脚本：
C:\Users\迪丽希斯\.workbuddy\skills\batch-image-resize\scripts\图像转正修改尺寸.py
把完整输出告诉我，包括处理了多少张图片，有无报错。
```

**注意**：ACP模式下 PowerShell 无法捕获 Python 输出，**必须用 Agent 工具执行**。

## 脚本说明

技能内置脚本路径：`C:\Users\迪丽希斯\.workbuddy\skills\batch-image-resize\scripts\图像转正修改尺寸.py`（优先使用）
- 读取 `D:\BaiduNetdiskDownload` 文件夹
- 根据 EXIF Orientation 标签自动转正（支持 Orientation 1-8）
- 缩放宽度到 1080px，保持比例
- 直接覆盖原图（无备份）

## 常用参数

- 脚本路径：`D:\Spyer项目\图像转正修改尺寸.py`
- Python 路径：`D:\Python\python.exe`
- 图片目录：`D:\BaiduNetdiskDownload`
- 目标宽度：1080px（可按需修改脚本中的 `target_width` 变量）
