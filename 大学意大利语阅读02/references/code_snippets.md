# 音频生成 & 部署脚本模板

## edge-tts 音频生成（异步）
```python
import asyncio, json, base64, os

VOICE = "it-IT-IsabellaNeural"

async def generate_audio(text, out_path):
    temp = out_path + ".tmp.mp3"
    proc = await asyncio.create_subprocess_exec(
        "edge-tts", "--voice", VOICE, "--text", text,
        "--write-media", temp
    )
    await proc.communicate()
    with open(temp, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    os.remove(temp)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"b64": b64, "text": text}, f)
```

## GitHub Git Data API 批量部署
```python
import json, os, base64, urllib.request

def gh_api(method, path, data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=json.dumps(data).encode() if data else None, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return None

# 5步流程：
# 1. GET  git/refs/heads/main → HEAD SHA
# 2. POST git/blobs → files
# 3. POST git/trees → tree
# 4. POST git/commits → commit
# 5. PATCH git/refs/heads/main → push
```

## Section 边界检测（避坑版）
```python
# 找到 section 的起始和结束
ts = html.find('<section class="section-card testo" id="testo">')
# 找到下一个 section 的起始
ns = html.find('<section class="section-card vocab" id="vocabolario">', ts)
# section 内容 = html[ts:ns]

# ⚠️ Esercizi 没有 </section> 闭合
# ⚠️ 搜索 class 必须完整 "section-card testo" 而非 "section-card"
```

## base64 文件名编码
```python
import base64
fname = base64.b64encode(str(idx).encode()).decode().rstrip("=")
# 反向：base64.b64decode(fname + "=" * (-len(fname) % 4)).decode()
```
