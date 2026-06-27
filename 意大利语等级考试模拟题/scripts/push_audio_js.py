#!/usr/bin/env python3
"""Push all base64 audio JS files to GitHub"""
import os, base64, json, urllib.request, time, glob

# === CONFIG ===
TOKEN = "<github-token>"
OWNER = "<github-username>"
REPO = "<github-repo-name>"
LOCAL = r"<repo-dir>"

def push(rel_path, retries=3):
    fp = os.path.join(LOCAL, *rel_path.split("/"))
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(OWNER, REPO, rel_path)
    
    sha = None
    for a in range(retries):
        try:
            req = urllib.request.Request(url)
            req.add_header("Authorization", "Bearer {}".format(TOKEN))
            req.add_header("Accept", "application/vnd.github.v3+json")
            resp = urllib.request.urlopen(req, timeout=15)
            sha = json.loads(resp.read())["sha"]
            break
        except urllib.error.HTTPError as e:
            if e.code == 404: break
            time.sleep(2)
        except: time.sleep(2)
    
    with open(fp, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    data = {"message": "Audio JS files", "content": content, "branch": "master"}
    if sha: data["sha"] = sha
    
    for a in range(retries):
        try:
            req2 = urllib.request.Request(url, method="PUT", data=json.dumps(data).encode())
            req2.add_header("Authorization", "Bearer {}".format(TOKEN))
            req2.add_header("Accept", "application/vnd.github.v3+json")
            req2.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req2, timeout=300) as r:
                s = json.loads(r.read()).get("content", {}).get("sha", "?")[:7]
            sz = os.path.getsize(fp) // 1024
            print("  {} {}KB {}".format(rel_path, sz, s))
            return True
        except Exception as e:
            if a < retries-1: time.sleep(5)
    print("  FAIL {}".format(rel_path))
    return False

# Find all .js audio files
js_files = []
for exam in ["CILS", "CELI"]:
    for set_name in ["CILS1","CILS2","CILS3","CELI1","CELI2","CELI3"]:
        for root, dirs, fnames in os.walk(os.path.join(LOCAL, exam, set_name)):
            for fn in fnames:
                if fn.endswith(".js"):
                    fp = os.path.join(root, fn)
                    rel = os.path.relpath(fp, LOCAL).replace("\\", "/")
                    js_files.append(rel)

js_files.sort()
print("Pushing {} audio JS files...".format(len(js_files)))
for f in js_files:
    push(f)
    time.sleep(0.3)
print("\nDone!")
