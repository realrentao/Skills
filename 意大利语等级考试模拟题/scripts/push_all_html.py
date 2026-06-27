#!/usr/bin/env python3
"""Push ALL HTML files to GitHub - final fix"""
import base64, json, urllib.request, os, time

TOKEN = "${GITHUB_TOKEN}"
OWNER = "realrentao"
REPO = "italiano-esami"
LOCAL = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"

FILES = [
    "index.html", "CILS/index.html", "CELI/index.html",
    "CILS/CILS_A1.html", "CILS/CILS_A2.html", "CILS/CILS_B1.html",
    "CILS/CILS_B2.html", "CILS/CILS_C1.html", "CILS/CILS_C2.html",
    "CELI/CELI_A1.html", "CELI/CELI_A2.html", "CELI/CELI_B1.html",
    "CELI/CELI_B2.html", "CELI/CELI_C1.html", "CELI/CELI_C2.html",
]

def push(path):
    fp = os.path.join(LOCAL, *path.split("/"))
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(OWNER, REPO, path)
    
    sha = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url)
            req.add_header("Authorization", "Bearer {}".format(TOKEN))
            req.add_header("Accept", "application/vnd.github.v3+json")
            resp = urllib.request.urlopen(req, timeout=15)
            sha = json.loads(resp.read())["sha"]
            break
        except Exception as e:
            if "409" in str(e):
                sha = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
                break
            time.sleep(2)
    
    if not sha:
        print("SKIP {} (no sha)".format(path))
        return False
    
    with open(fp, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    data = json.dumps({"message": "Final fix: all pages use independent JS audio", "content": content, "sha": sha, "branch": "master"}).encode()
    
    for attempt in range(3):
        try:
            req2 = urllib.request.Request(url, method="PUT", data=data)
            req2.add_header("Authorization", "Bearer {}".format(TOKEN))
            req2.add_header("Accept", "application/vnd.github.v3+json")
            req2.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req2, timeout=120) as r:
                result = json.loads(r.read())
                s = result["content"]["sha"][:7]
            size = os.path.getsize(fp) // 1024
            print("OK {} {}KB {}".format(path, size, s))
            return True
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                print("FAIL {}: {}".format(path, str(e)[:60]))
                return False

if __name__ == "__main__":
    print("=" * 60)
    print("Pushing all HTML files to GitHub")
    print("=" * 60)
    success = 0
    for f in FILES:
        if push(f):
            success += 1
        time.sleep(0.5)
    print("\n{}/{} files pushed".format(success, len(FILES)))
