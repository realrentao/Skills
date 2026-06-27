---
name: 意大利语动词变位表制作
description: 从零创建或扩展现有的意大利语动词变位查询网页（HTML+JS），含A-Z索引、7大语式矩阵表格、动词详情、例句短语。当用户要求制作动词变位页面、补全动词变位数据、添加动词时使用。
agent_created: true
---

# 意大利语动词变位表制作 Skill

## 概述

构建一个意大利语动词变位查询的单页 HTML 应用。核心特征：左侧按 A-Z 字母索引浏览动词，选中动词后自动展示 7 大语式（直陈式/虚拟式/条件式/命令式/不定式/副动词/分词）的矩阵变位表；右侧展示动词详情（含义/类别/特征/例句/短语/时态速览）。

## 页面结构

### 布局
- 双栏 grid 布局：左栏变位表 + 右栏动词详情
- 顶部：标题 + 搜索栏 + A-Z 圆角字母索引按钮
- 色系：米白 #FDF6F0 背景 | 金色 #B8860B 点缀 | 蓝色 #1E5AA8 左栏 | 红色 #8B2500 右栏
- 手机端响应式：单列、紧凑间距、变位表字体放大

### 核心组件

1. **A-Z 字母索引**：水平排列的圆形按钮（36×36px），点击点亮字母，联动显示动词列表
2. **动词列表**：该字母开头的动词列表，每条显示动词原形 + 中文 + 规则/不规则标签
3. **7 大语式矩阵表**：选中动词后，按语式分组展示全部变位
   - 语式：直陈式(8时态)、虚拟式(4时态)、条件式(2时态)、命令式(1时态)、不定式(2)、副动词(2)、分词(2)
   - 直陈式 8 个时态拆成 2 张 4 列表格上下排列
   - 人称行 × 时态列的横向矩阵（6 行人称 × N 列时态）
   - 非人称语式（不定式/副动词/分词）使用网格卡片
   - 空语式自动隐藏
4. **动词详情**：原形/含义/类别标签/变位特征/助动词/时态速览卡片/例句/短语

## 数据架构

### verbData（显示数据）
`const verbData = { "a": [{ infinito, meaning, category, tags, aux, features, examples, phrases, tenses }] }`

### VCONJ（变引引擎元数据）
```js
const VCONJ = {
  "parlare": {type:"are", stem:"parl", aux:"avere", pp:"parlato"},
  // type: "are" | "ere" | "ire" | "ire-isc" | "care" | "iare" | "are-rfl" | "irr"
  // 不规则动词添加手动覆盖字段：pres, rem, fut, cond, cong, impv
  "andare":  {type:"irr"}, // 数据在 verbData.tenses 中手动填写
}
```

### 变位引擎（conjVerbs 函数）
- 为每个动词生成 21 个时态的变位数据
- 规则动词：`rules[type]` 中的词尾 + `stem` 拼接
- 自动复合时态：`auxT(tense_key).map(a => a + " " + pp)`
- 手动覆盖优先：`end(k, override)` 中的 override 参数
- 自反动词：自动添加 `mi/ti/si/ci/vi/si` 前缀
- 命令式第一人称：空字符串 `""`，渲染时留白

### getRules（变位规则定义）
定义 8 种变位类型的词尾：`are`, `are-rfl`, `care`, `iare`, `ere`, `ire`, `ire-isc`
每类含：pres, imperf, rem, fut, cond, cong, cong_imp, impv, inf, ger, ppres

### AUX（助动词变位）
avere 和 essere 的：pres, imperf, rem, fut, cong, cong_imp, cond, gerundio

## 样式规则

### 金色高亮词尾
- `Io/Tu/Lui`(索引0,1,2)：高亮最后 2 字符
- `Noi/Voi/Loro`(索引3,4,5)：高亮最后 3 字符
- 非人称形式默认高亮 2 字符
- `.highlight`：color #B8860B, font-weight bold

### 不规则动词标识
- `cell-irregular`：极浅暖金色背景 #FFFCF5
- 规则动词保持白色背景

### 命令式第一人称
impv 数组的第一个元素为 `""`，渲染时直接输出空字符串

## 工作流程

### 添加新动词（关键流程，严格遵守）

**推荐方式：Python JSON 操作（安全、不会出错）**

```python
import json
with open('D:/path/verb-data.js', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find('{')
end = content.rfind('};') + 1
json_str = content[start:end]
data = json.loads(json_str)

# 追加新动词到对应字母段
new_verb = {"infinito":"xxx", "meaning":"...", "category":"...", "tags":["regular"], "aux":"avere", "level":"A2", "features":"...", "examples":[...], "phrases":[...], "tenses":{}}
data["对应字母"].append(new_verb)

# ⚠️ 排序（必须！每次添加后都要排序）
for letter in data:
    data[letter] = sorted(data[letter], key=lambda v: v['infinito'].lower())

# 写回
new_json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
new_content = content[:start] + new_json_str + content[end:]
with open('D:/path/verb-data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
```

**手动方式（不推荐，易出错）：**

1. **同时更新两处**：在 verbData 追加条目 + 在 VCONJ 追加元数据，缺一不可
2. verbData 条目格式：`{ infinito, meaning, category, tags, aux, features, examples, phrases, tenses:{} }`
3. VCONJ 格式：`"verbo": {type:"are", stem:"xxx", aux:"avere", pp:"xxx"}`

#### ⚠️ 添加时绝对不能做的事（从错误中总结）
- ❌ **不要在 verbData/VCONJ 中间插入条目**——只能在对应字母段末尾追加
- ❌ **不要删除或修改已有任何内容**——包括现有的动词、注释、代码结构
- ❌ **不要在 verb 条目之间的 `}` 和下一个 `{` 之间漏掉逗号**——必须为 `},` 后换行再 `{`
- ❌ **不要改动文件开头的 CSS 样式、HTML 结构、或 JS 函数代码**
- ❌ **不要改动 moodGroups、pronouns、AUX、getRules、conjVerbs 等引擎代码**

#### ✅ 正确的追加方式
```js
// verbData 中：找到对应字母段末尾（即字母段数组的 ] 前），在最后一个动词的 }, 后追加
"a": [
    ...已有动词...
    },
    {  ← 注意前面是 }, 有逗号！
        infinito: "nuovoverbo",
        ...
        tenses: {}
    }
],

// VCONJ 中：在对应字母段注释后追加一行
// A  ← 字母段注释
"nuovoverbo": {type:"are", stem:"nuovo", aux:"avere", pp:"nuovato"},
"parlare":    {type:"are", stem:"parl", aux:"avere", pp:"parlato"},
```

### 检查清单（每次添加完后执行）
1. 在浏览器本地预览页面，确认页面能正常加载
2. 选中新添加的动词，确认 7 个语式都能正常展示
3. **排序检查（每次添加完必须执行！）**：用 Python 对所有字母段的动词按 `infinito` 字母序重排：
   ```python
   for letter in data:
       data[letter] = sorted(data[letter], key=lambda v: v['infinito'].lower())
   ```
4. 用 Node.js 快速验证 JSON 解析正常：`require('fs'); eval(code.replace(/window.*$/m, ''));`
5. 确认 VCONJ 和 verbData 的条目数匹配（每个 verbData 的动词都应在 VCONJ 中有对应）
6. **推送到 GitHub（每次修改完必须执行！）**：用 Python urllib + GitHub API 上传 3 个文件，详见下方推送脚本

### 推送 GitHub Pages（每次修改完后执行）

仓库：`realrentao/italiano-verbi` | Token：见 ~/.workbuddy/MEMORY.md | Pages：`https://realrentao.github.io/italiano-verbi/`

**重要：本地文件映射到 GitHub 路径：**
- 本地 `engine.js` → GitHub `engine.js`
- 本地 `verbi-italiani.html` → GitHub `index.html`
- 本地 `verb-data.js` → GitHub `verb-data.js`

**推送脚本（Python）：**
```python
import json, base64, urllib.request

token = 'YOUR_GITHUB_TOKEN'  # 从 ~/.workbuddy/MEMORY.md 获取
owner, repo, branch = 'realrentao', 'italiano-verbi', 'main'

def get_sha(path):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('User-Agent', 'WorkBuddy')
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())['sha']

files = [
    ('engine.js', 'D:/意大利语材料/意大利语动词变位/engine.js'),
    ('index.html', 'D:/意大利语材料/意大利语动词变位/verbi-italiani.html'),
    ('verb-data.js', 'D:/意大利语材料/意大利语动词变位/verb-data.js'),
]

for github_path, local_path in files:
    sha = get_sha(github_path)
    with open(local_path, 'rb') as f:
        content = f.read()
    b64 = base64.b64encode(content).decode('utf-8')
    payload = json.dumps({'message': '更新动词数据', 'content': b64, 'sha': sha, 'branch': branch}).encode()
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{github_path}'
    req = urllib.request.Request(url, data=payload, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'WorkBuddy')
    urllib.request.urlopen(req)
```

### 补全不规则动词数据
手动填写 21 个时态数组（直陈式8+虚拟式4+条件式2+命令式1+不定式2+副动词2+分词2）

## 注意事项
- **字母序强制规则**：每次添加新动词后，必须对该字母段的动词重新按 `infinito` 字母序排序，确保动词列表始终有序展示
- 所有 impv 数组第一个元素必须为 `""`（第一人称留白）
- 自反动词的 gerundio/participio 后缀：andosi, endosi
- essere 的 21 个时态数据手动填写在 verbData 中（不依赖引擎生成）
- 动词的 `features` 字段用 `<br>` 分隔各要点
- 例句用 `{it: "...", cn: "..."}` 格式，至少 2-3 句含不同时态
- 短语用 `"原形 — 中文"` 格式，至少 2-3 条
