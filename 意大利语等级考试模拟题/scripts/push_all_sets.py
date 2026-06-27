#!/usr/bin/env python3
"""Push all HTML files from all 6 exam sets to GitHub via API"""
import os, base64, json, urllib.request, time, glob

# === CONFIG ===
TOKEN = "<github-token>"
OWNER = "<github-username>"
REPO = "<github-repo-name>"
LOCAL = r"<repo-dir>"

def push(path, retries=3):
    fp = os.path.join(LOCAL, *path.split("/"))
    if not os.path.exists(fp):
        print("SKIP {} (not found)".format(path))
        return False
    
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(OWNER, REPO, path)
    
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
    
    data = {"message": "Update exam pages", "content": content, "branch": "master"}
    if sha: data["sha"] = sha
    
    for a in range(retries):
        try:
            req2 = urllib.request.Request(url, method="PUT", data=json.dumps(data).encode())
            req2.add_header("Authorization", "Bearer {}".format(TOKEN))
            req2.add_header("Accept", "application/vnd.github.v3+json")
            req2.add_header("Content-Type", "application/json")
            resp2 = urllib.request.urlopen(req2, timeout=120)
            s = json.loads(resp2.read()).get("content", {}).get("sha", "?")[:7]
            print("OK {} {}KB {}".format(path, os.path.getsize(fp)//1024, s))
            return True
        except:
            if a < retries-1: time.sleep(3)
    print("FAIL {}".format(path))
    return False

# Find all HTML files
files = ["index.html"]
for root, dirs, fnames in os.walk(LOCAL):
    for fn in fnames:
        if fn.endswith(".html"):
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, LOCAL).replace("\\", "/")
            if rel not in files:
                files.append(rel)

files.sort()
print("Pushing {} files...".format(len(files)))
for f in files:
    push(f)
    time.sleep(0.3)
print("\nDone!")
