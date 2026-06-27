---
name: "101-conversations"
description: "生成101 Conversations交互式意大利语听力练习页面。当用户需要从零构建整个项目、补全译文、生成音频、添加词汇、检查音频完整性时使用。项目是基于Olly Richards教材的101篇意大利语对话，包含角色语音、交互式播放器、词汇表和中文译文。"
agent_created: true
---

# 101 Conversations — 页面生成流水线

## 概述

将《101 Conversations in Intermediate Italian》(Olly Richards) 教材转化为交互式听力练习Web应用。核心产物是一个纯前端HTML页面（index.html）+ JSON数据文件，通过GitHub Pages部署。

**仓库**: `github.com/realrentao/italian-101-conversations`
**部署URL**: `https://realrentao.github.io/italian-101-conversations/`

## 前置条件

- Python 3.13+，已安装 `edge-tts` 包（`pip install edge-tts`）
- Git 和 GitHub CLI (`gh`)
- 项目目录: `D:\意大利语材料\101-conversations`
- GitHub PAT 配置在 `~/.workbuddy/MEMORY.md` 中

## 完整工作流

### 阶段1: 数据提取（一次性）

从EPUB提取101篇对话的结构化数据。

```python
# extract_epub.py — 通用EPUB解析
# extract_convs.py — 精确TOC匹配提取，输出 conversations_raw.json
# 最终数据合并到 conversations.json
```

**关键**: `conversations.json` 中的 `paragraphs` 数组包含两种格式：
- **叙述段落**: 纯文本（无冒号）
- **对话行**: `角色名:说话内容`（冒号在25字符内）

### 阶段2: 中文译文补全

向 `conversations.json` 中每个对话的 `translations` 数组添加中文译文。

**手动添加**（推荐用于少量对话）:
- 直接编辑 `conversations.json`，将译文按段落索引放入 `translations` 数组
- 每段译文与 `paragraphs` 一一对应
- 对话保留角色名+冒号格式（如 `阿戈斯蒂娜：……`）

**批量翻译**（仅用于大量对话时）:
- 使用 `phase1_translate.py` / `phase1_translate_v2.py`
- 使用 MyMemory API（带email提高限速）
- 每3篇自动保存一次进度，避免丢失

**添加中文标题**: 运行 `add_title_cn.py`（预定义101篇中文标题映射表）

### 阶段3: 音频生成

为每个段落生成角色匹配的edge-tts音频。

#### 3.1 生成原始音频

```python
# generate_all_voices.py — 主音频生成脚本
# 参数: start(起始索引0-based) end(结束索引)
# 输出: audio_conv/conv_{num}/{pIdx}.json
```

**角色检测逻辑**（在脚本中定义的函数）:
1. 检测段落中冒号前的说话人名称
2. 女性角色（`FEMALE_NAMES`）→ Elsa (`it-IT-ElsaNeural`)
3. 男性角色（`MALE_NAMES`）→ Diego (`it-IT-DiegoNeural`)
4. 旁白/无说话人 → Isabella (`it-IT-IsabellaNeural`)
5. 旁白使用 `it-IT-GiuseppeMultilingualNeural` 用于Zamboni角色
6. `get_audio()` 函数调用 edge-tts CLI 生成MP3并base64编码
7. 每段生成后 sleep 0.25秒避免限频
8. 如果中途中断，可从指定索引重新开始：`python generate_all_voices.py <start_idx> <end_idx>`
9. 生成时需设置 `PYTHONUTF8=1` 环境变量避免中文编码问题

#### 3.2 转换格式

```python
# conv_audio_conv_to_para.py — audio_conv → audio_para 格式转换
# 将 audio_conv/conv_{num}/{pIdx}.json 转为 audio_para/conv_{num}_{pIdx}.json
# 每个文件包含 {"b64": "...", "voice": "...", "speaker": "..."}
```

#### 3.3 音频完整性检查

所有音频文件生成后，必须有一次完整的 `audio_conv/` vs `audio_para/` 对比扫描。

**检查方法**: 对于每篇对话的每个段落，读取 `audio_conv/conv_{num}/{pIdx}.json` 的 `audio` 字段和 `audio_para/conv_{num}_{pIdx}.json` 的 `b64` 字段，对比base64字符串长度。若长度不一致（原始 > audio_para），说明audio_para被截断，需要用原始数据覆盖。

**修复方法**: 直接将 `audio_conv` 中的 `audio` 字段值赋给 `audio_para` 的 `b64` 字段。

### 阶段4: 词汇表与词汇发音

#### 4.1 词汇数据

`conversations.json` 中每个对话的 `vocab` 数组包含词汇条目：
```json
{"word": "lo squillo", "meaning": "电话铃声 / phone ring"}
```
- `meaning` 格式: `中文释义 / English meaning`

#### 4.2 生成词汇音频

```python
# gen_vocab_audio.py — 批量生成所有词汇的edge-tts音频
# 输出: vocab_para/vocab_{num}_{idx}.json
```

#### 4.3 补缺失词汇音频

```python
# gen_missing_vocab.py — 扫描vocab_para目录，补生成缺失文件
# gen_missing_remaining.py — 补生成最后3个特定缺失词汇
```

### 阶段5: 前端页面

`index.html` 是单页应用的前端，无需额外框架或构建步骤。

**核心功能**:
- 左侧边栏：对话列表（101篇）、搜索、已读进度
- 右侧主区域：段落卡片（每段含播放按钮、语速控制、译文折叠）
- 词汇表：可点击播放词汇发音
- 音频加载：按需从 `audio_para/` 加载base64音频
- 角色分音色播放
- 三档语速（0.6x/1x/1.4x）
- 已读进度存入 localStorage

**关键JS函数**:
| 函数 | 作用 |
|------|------|
| `preloadData()` | 页面加载时异步fetch `conversations.json` |
| `showConversation(idx)` | 渲染指定对话的内容 |
| `loadParaAudio(num, pIdx)` | 按需加载 `audio_para/conv_{num}_{pIdx}.json` |
| `loadAndPlay(convIdx, paraIdx)` | 加载并播放指定段落音频 |
| `togglePlay()` | 切换播放/暂停 |
| `playAll(convIdx)` | 连续播放全部段落 |
| `speakWord(convNum, vocabIdx)` | 播放词汇发音 |
| `setSpeed(convIdx, paraIdx, speed)` | 设置0.6x/1x/1.4x语速 |

### 阶段6: 部署

通过GitHub Pages从main分支直接部署：

```bash
cd D:\意大利语材料\101-conversations

# 确保 .gitignore 包含以下关键保留规则：
# !conversations.json
# !audio_para/*.json
# !vocab_para/*.json

git add .
git commit -m "生成/更新页面"
git push origin main
```

推送后等待1-2分钟，访问 `https://realrentao.github.io/italian-101-conversations/`。

### 阶段7: 日常维护

**添加新译文**:
1. 读取 `conversations.json` 中找到对应的对话(num)
2. 向 `translations` 数组添加中文译文（按段落索引）
3. 译文格式：叙述段直译，对话段保留`角色名：`前缀

**修复音频问题**:
1. 对比 `audio_conv/` 与 `audio_para/` 的同名文件base64数据长度
2. 若不一致，用 `audio_conv` 的原始数据覆盖 `audio_para`

**推送更新**:
```bash
git add conversations.json audio_para/ vocab_para/
git commit -m "更新内容描述"
git push origin main
```

## 重要注意事项

1. **GitHub Token**: 读 `~/.workbuddy/MEMORY.md` 获取，不要硬编码
2. **Git user config**: name=realrentao, email=realrentao@users.noreply.github.com
3. **音频生成环境**: Python 需要使用 `-X utf8` 参数避免中文编码错误
4. **编码问题**: 所有JSON文件必须使用 UTF-8 编码保存
5. **译文字段**: 若 `translations` 数组不存在或为空，前端显示"点击「译文」按钮将自动加载中文翻译"
6. **git忽略规则**: `.gitignore` 中有 `*.json` 全局忽略规则，需要通过 `!` 显式保留关键文件
7. **音频缓存冗余**: `audio_cache_new/` 和 `audio_para/` 存有相同数据，`audio_cache_new/` 仅在重新生成时有用

## 参考

- `references/data-model.md`: 完整数据模型和文件格式
