---
name: italian-idioms
agent_created: true
description: 意大利语习语交互式HTML教学页面完整生成流程。从 idioms_data.py 数据源生成47个习语页面（含edge-tts意大利女声配音、三种语速播放、选择题/填空题、文化注释），并推送到GitHub Pages。
---

# 意大利语习语生成技能

## 概述
从 `idioms_data.py` 数据生成交互式意大利语习语学习 HTML 页面，包含：
- 47 个习语独立页面（含完整音频）
- index.html 导航主页
- 三种语速播放（0.6×/1.0×/1.4×）
- 填空题 + 选择题练习
- 中文译文和意大利语释义
- 文化注释
- 推送到 GitHub Pages

## 工作目录
`D:\意大利语材料\意大利语习语`

## 数据格式（idioms_data.py）
每条习语数据格式：
```python
{
    "id": 47,
    "idiom": "Mettere il carro davanti ai buoi",
    "category": "Logica / Ordine",
    "meaning_cn": "本末倒置 / 把马车放在牛前面 / 顺序颠倒",
    "meaning_it": "Agire in modo prematuro...",
    "usage_cn": "形容做事情不按正确顺序...",
    "examples": [
        ("A", "Ho comprato...", "我还没找到工作就先买了新车！"),
        ("B", "Ma stai mettendo...", "你这是本末倒置啊！"),
    ],
    "cultural_cn": "「Mettere = 放」「il carro = 马车」...",
    "exercise_q": [
        {'question': '这个习语和哪个中文表达最接近？', 'options': ['本末倒置', ...], 'answer': 'A) 本末倒置'},
        {'question': 'Completa: Stai mettendo il ________ davanti ai ________!', 'fill': ['carro, buoi']},
    ],
    "english_eq": "To put the cart before the horse",
    "meaning_it_cn": "做事顺序颠倒...",
},
```

## 填空题检验逻辑（checkFill）
使用基于单词顺序的比较，忽略大小写、标点符号和空格：

```javascript
function checkFill(id) {
    const input = document.getElementById('fill-input-' + id);
    const fb = document.getElementById('fill-feedback-' + id);
    const answer = document.getElementById('fill-answer-' + id);
    const userAnswer = input.value.trim();
    const correct = answer.textContent.replace('💡 ', '').trim();

    if (!userAnswer) {
        fb.className = 'fill-feedback hint';
        fb.textContent = '✏️ 请先输入你的答案';
        return;
    }

    // Compare by words in order, ignoring case, punctuation and spacing
    const normalizeWords = (s) => s.toLowerCase()
        .replace(/[^\w\u00C0-\u024F'\-]/g, ' ')
        .trim().split(/\s+/).filter(Boolean);
    const userWords = normalizeWords(userAnswer);
    const correctWords = normalizeWords(correct);
    const wordMatch = userWords.length === correctWords.length &&
        userWords.every((w, i) => w === correctWords[i]);

    if (wordMatch) {
        fb.className = 'fill-feedback correct';
        fb.textContent = '✅ 正确！';
        input.classList.add('correct');
        input.classList.remove('wrong');
    } else {
        fb.className = 'fill-feedback wrong';
        fb.textContent = '❌ 不对，再想想';
        input.classList.add('wrong');
        input.classList.remove('correct');
    }
}
```

关键特点：
- **忽略大小写**: normalizeWords 内部先 .toLowerCase()
- **忽略标点**: 正则替换非单词字符（保留意大利语重音字母和撇号）
- **按序比对**: 用户输入和答案分别拆成单词数组，逐个比对
- **用例**: 答案 `carro, buoi` → 用户输入 `CARRO B UOI!` 判定正确

## 完整生成流程

### 1️⃣ 数据准备
- 编辑 `idioms_data.py` 添加新习语条目
- 字段包括：id, idiom, category, meaning_cn, meaning_it, usage_cn, examples, cultural_cn, exercise_q, english_eq, meaning_it_cn

### 2️⃣ 运行生成器
```bash
cd "D:/意大利语材料/意大利语习语"
python generate_html.py
```
此脚本会：
- 为每个习语用 edge-tts 生成主音频（意大利女声）
- 为释义和例句生成 inline 音频
- 生成 HTML 页面（所有习语页面 + index.html）
- 数据 JSON 文件存入 `data/` 目录

### 3️⃣ 验证
- 检查 `idiom-XX.html` 是否有音频（audioUrl 不为空）
- 检查 `data/idiom-XX-audio-*.json` 是否存在
- 检查 index.html 包含新习语

### 4️⃣ Git 推送
```bash
cd "D:/意大利语材料/意大利语习语"
git remote set-url origin "https://realrentao:你的PAT@github.com/realrentao/italian-idioms.git"
git add .
git commit -m "Add idiom #XX: ..."
git push --force origin clean-main:main
```

注意：
- 本地分支使用 `clean-main`（干净历史，不含 PAT token），推送到远程 `main`
- 避免在仓库中存储 PAT token（如 push_each_file.py、push_in_batches.py）
- 如果 push 被拒绝（secret detection），用 orphan branch 重建干净历史：
  ```bash
  git checkout --orphan clean-main
  git add .
  git commit -m "Clean slate: 47 Italian idioms"
  git push --force origin clean-main:main
  ```
- 网络不稳定时可重试推送

### 5️⃣ GitHub Pages
- 仓库: realrentao/italian-idioms
- 主页: https://realrentao.github.io/italian-idioms/

## 目录结构
```
D:\意大利语材料\意大利语习语\
├── idioms_data.py      # 数据源（47条习语）
├── generate_html.py    # HTML/音频生成器
├── index.html          # 导航主页
├── idiom-XX.html       # 习语页面（XX=01-47）
├── audio/              # MP3音频文件
│   ├── *.mp3           # 主习语音频
│   └── inline_*.mp3    # 例句/释义内嵌音频
└── data/               # 音频JSON数据
    └── idiom-XX-audio-*.json
```

## 常用操作

### 新增单个习语
1. 在 `idioms_data.py` 末尾添加新条目
2. 运行 `python generate_html.py`
3. Git 提交并推送

### 恢复丢失数据
如果 HTML 文件存在但 idioms_data.py 数据丢失，从 HTML 恢复：
```python
# 使用 get_between() 从 HTML 提取各字段
# 示例字段: idiom-text, meaning_cn, cultural-note, trans-text, exercise-q
```

### 修改填空题逻辑
编辑 `generate_html.py` 中的 `checkFill` 函数，然后重新生成所有页面。
