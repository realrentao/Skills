# 常用代码片段参考

## 音频拆分脚本

```python
import json, os, base64, shutil

BASE = "."  # 项目目录
AUDIO_DIR = os.path.join(BASE, "audio")
if os.path.exists(AUDIO_DIR):
    shutil.rmtree(AUDIO_DIR)
os.makedirs(AUDIO_DIR)

def safe_filename(key):
    key_bytes = key.encode('utf-8')
    return base64.urlsafe_b64encode(key_bytes).decode('ascii').rstrip('=')

# 拆分单词音频
with open(os.path.join(BASE, "audio_data.json"), 'r', encoding='utf-8') as f:
    audio_data = json.load(f)
word_dir = os.path.join(AUDIO_DIR, "w")
os.makedirs(word_dir)
word_map = {}
for key, b64 in audio_data.items():
    fname = safe_filename(key) + ".json"
    with open(os.path.join(word_dir, fname), 'w', encoding='utf-8') as f:
        json.dump({"b64": b64}, f, ensure_ascii=False)
    word_map[key] = f"audio/w/{fname}"
with open(os.path.join(AUDIO_DIR, "w_map.json"), 'w', encoding='utf-8') as f:
    json.dump(word_map, f, ensure_ascii=False)

# 拆分段落音频
with open(os.path.join(BASE, "testo_audio.json"), 'r', encoding='utf-8') as f:
    testo_data = json.load(f)
para_dir = os.path.join(AUDIO_DIR, "p")
os.makedirs(para_dir)
para_map = {}
for key, item in testo_data.items():
    fname = safe_filename(key) + ".json"
    with open(os.path.join(para_dir, fname), 'w', encoding='utf-8') as f:
        json.dump(item, f, ensure_ascii=False)
    para_map[key] = f"audio/p/{fname}"
with open(os.path.join(AUDIO_DIR, "p_map.json"), 'w', encoding='utf-8') as f:
    json.dump({"paragraphs": para_map}, f, ensure_ascii=False)
```

## GitHub 部署脚本模板

```python
import json, os, base64

BASE = "."
TOKEN = "ghp_..."  # 从 MEMORY.md 读取
OWNER = "realrentao"
REPO = "university-italian-reading"
BRANCH = "main"

import urllib.request

def gh_api(method, path, data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode('utf-8')
    else: body = None
    try:
        with urllib.request.urlopen(req, data=body, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode(); print(f"HTTP {e.code}: {err[:200]}"); return None

# 1. 获取当前 HEAD
ref = gh_api("GET", f"git/refs/heads/{BRANCH}")
current_sha = ref["object"]["sha"]

# 2. 收集所有文件
files = []
# HTML
with open(os.path.join(BASE, "lezione1.html"), 'rb') as f:
    files.append({"path": "lezione1.html", "content": base64.b64encode(f.read()).decode(), "encoding": "base64"})
# 音频文件
for root, dirs, fnames in os.walk(os.path.join(BASE, "audio")):
    for fn in sorted(fnames):
        if not fn.endswith('.json'): continue
        fp = os.path.join(root, fn)
        rel = os.path.relpath(fp, BASE).replace('\\', '/')
        with open(fp, 'rb') as f:
            files.append({"path": rel, "content": base64.b64encode(f.read()).decode(), "encoding": "base64"})

# 3. 创建 blobs
blobs = []
for f in files:
    payload = {"content": f["content"], "encoding": f["encoding"]}
    blob = gh_api("POST", "git/blobs", payload)
    if blob: blobs.append({"path": f["path"], "mode": "100644", "type": "blob", "sha": blob["sha"]})

# 4. 创建 tree + commit + 更新 ref
tree = gh_api("POST", "git/trees", {"base_tree": current_sha, "tree": blobs})
commit = gh_api("POST", "git/commits", {
    "message": "commit message",
    "tree": tree["sha"], "parents": [current_sha]
})
gh_api("PATCH", f"git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False})
```
