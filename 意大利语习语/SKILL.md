---
name: 意大利语习语
description: >
  意大利语习语交互式HTML教学工具。从结构化数据生成包含edge-tts音频、中文译文、交互式练习、速度控制的完整HTML教学页面。
  当用户说"做意大利语页面"、"意大利语习语"、"idiom"、"创建习语"、"添加习语"或需要生成意大利语教学内容时使用。
agent_created: true
---

# 意大利语习语 (Italian Idioms Interactive HTML Generator)

## 概述

生成意大利语习语交互式HTML教学页面。每页包含核心模块：

- **习语标题 + 音频播放**（edge-tts 意大利女声 IsabellaNeural）
- **含义**（意大利语 + 中文 + 英语 + 可收纳中文译文 + 音频）
- **例句**（对话形式 + 可收纳中文译文 + 逐句音频）
- **文化注释**
- **交互式练习**（选择题 + 填空题带输入框）
- **语速控制**（0.6× / 1.0× / 1.4×）
- **页面间导航**

所有音频存储为独立JSON文件（base64编码），按需加载。

## 项目结构

```
project/
├── generate_html.py        # 主生成器（CSS样式 + 页面模板 + 音频生成）
├── idioms_data.py           # 数据结构（31个习语的全部数据）
├── audio/                   # edge-tts生成的MP3音频文件
│   ├── <base64>.mp3          # 主习语音频（base64文件名）
│   └── inline_<hash>.mp3    # 含义/例句音频（hash去重）
├── data/
│   ├── idiom-XX-audio-meaning.json   # 含义音频的base64数据
│   └── idiom-XX-audio-ex-N.json      # 例句音频的base64数据
├── index.html               # 导航页（搜索+分类筛选）
├── idiom-01~35.html         # 35个习语详情页（持续增加）
└── github_push.py           # 推送到GitHub工具
```

## 数据格式（idioms_data.py）

每个习语包含以下字段：

```python
{
    "id": 1,                          # 序号
    "idiom": "In bocca al lupo!",     # 习语原文
    "meaning_cn": "祝你好运！",        # 中文含义
    "meaning_it": "Espressione...",   # 意大利语解释
    "meaning_it_cn": "对一项困难...",  # 意大利语解释的中文译文
    "usage_cn": "用于考试、面试...",   # 用法说明
    "english_eq": "Break a leg!",     # 英语对应表达
    "cultural_cn": "直译...",         # 文化注释
    "category": "Auguri",             # 分类标签（意大利语）
    "examples": [                      # 例句（成对出现）
        ("A", "Domani ho...", "明天我有..."),  # (说话人, 意大利语, 中文译文)
        ("B", "In bocca al lupo!", "祝你好运！")
    ],
    "exercise_q": [                   # 练习题
        {"question": "...", "options": ["A", "B", "C", "D"], "answer": "C"},
        {"question": "...", "fill": ["正确答案"]},  # 单空
        # 多空填空题（用 / 分隔）：
        {"question": "...", "fill": ["parola1", "parola2", "parola3"]}
    ]
}
```

## 工作流程

### 1. 添加新习语

打开 `idioms_data.py`，在 `IDIOMS` 列表末尾追加新条目。注意保持分类标签在 `CATEGORY_CN` 映射表中。

### 2. 生成音频 + HTML

```bash
cd D:/workbuddy工作区/2026-06-19-22-24-56
python -c "from generate_html import generate_all; generate_all()"
```

这将依次：
0. 用 edge-tts 生成所有主习语音频（跳过已存在的）—— **必须步骤，否则主播放按钮无声**
1. 扫描所有需要音频的意大利语文本
2. 用 edge-tts 生成 MP3 并缓存到 `audio/`
3. 将音频转换为 base64，写入 `data/idiom-XX-audio-*.json`
4. 生成全部 HTML 页面

### 3. 部署到 CloudStudio

```python
workbuddy_cloudstudio_deploy(directory="项目目录", entry="index.html")
```

### 4. 部署到 GitHub

```bash
# 先创建仓库并启用 GitHub Pages
# 然后推送到 GitHub

cd 项目目录
python github_push.py
```

## 核心函数说明

- `safe_filename(key)` — 生成URL安全的base64文件名
- `slugify(text)` — 生成URL友好的slug
- `generate_categories()` — 从数据提取唯一分类
- `get_inline_texts(idiom)` — 获取需要音频的所有文本
- `text_hash(text)` — 为文本生成MD5哈希（用于去重）
- `generate_inline_audio_files()` — 生成所有inline音频MP3文件
- `build_inline_audio_json(audio_cache)` — 构建独立的base64 JSON文件
- `generate_index_html()` — 生成导航页
- `generate_idiom_page(idiom)` — 生成习语详情页
- `generate_all()` — 完整流水线

## SVG国旗

已内置意大利、中国、英国国旗的SVG函数：
- `svg_flag_it()` — 绿白红三色旗
- `svg_flag_cn()` — 红底金星旗
- `svg_flag_en()` — 米字旗

## JS播放逻辑

- **主习语音频**：引用 `audio/<safe_filename>.mp3`
- **inline音频**：每个独立JSON文件，通过 `data-audio` 属性引用
  - `data-audio="meaning"` → `data/idiom-XX-audio-meaning.json`
  - `data-audio="ex-0"` → `data/idiom-XX-audio-ex-0.json`

点击按钮时按需加载对应的JSON文件并解码为 Audio 播放，支持 `playbackRate` 变速。
