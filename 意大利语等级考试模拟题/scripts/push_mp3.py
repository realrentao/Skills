#!/usr/bin/env python3
"""Push MP3 files to GitHub - the key to working audio"""
import os, base64, json, urllib.request, time, glob

TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = "realrentao"
REPO = "italiano-esami"
LOCAL = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"

def push_mp3(rel_path):
    fp = os.path.join(LOCAL, *rel_path.split("/"))
    size = os.path.getsize(fp)
    url = "https://api.github.com/repos/{}/{}/contents/{}".format(OWNER, REPO, rel_path)
    
    # Check if file exists (get SHA)
    sha = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url)
            req.add_header("Authorization", "Bearer {}".format(TOKEN))
            req.add_header("Accept", "application/vnd.github.v3+json")
            with urllib.request.urlopen(req, timeout=15) as r:
                sha = json.loads(r.read())["sha"]
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                break  # New file, no SHA needed
            time.sleep(2)
        except: time.sleep(2)
    
    with open(fp, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    data = {"message": "MP3 audio for exams", "content": content, "branch": "master"}
    if sha: data["sha"] = sha
    
    for attempt in range(3):
        try:
            req2 = urllib.request.Request(url, method="PUT", data=json.dumps(data).encode())
            req2.add_header("Authorization", "Bearer {}".format(TOKEN))
            req2.add_header("Accept", "application/vnd.github.v3+json")
            req2.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req2, timeout=300) as r:
                result = json.loads(r.read())
            s = result.get("content", {}).get("sha", "?")[:7]
            print("OK {} {}KB {}".format(rel_path, size//1024, s))
            return True
        except Exception as e:
            if attempt < 2: time.sleep(5)
            else: print("FAIL {}: {}".format(rel_path, str(e)[:60]))
    return False

# Find all MP3 files
mp3_files = []
for exam in ["CILS", "CELI"]:
    for level in ["A1","A2","B1","B2","C1","C2"]:
        audio_dir = os.path.join(LOCAL, exam, level, "audio")
        if os.path.exists(audio_dir):
            for f in sorted(glob.glob(os.path.join(audio_dir, "*.mp3"))):
                rel = os.path.relpath(f, LOCAL).replace("\\", "/")
                mp3_files.append(rel)

print("Pushing {} MP3 files to GitHub...".format(len(mp3_files)))
success = 0
for f in mp3_files:
    if push_mp3(f): success += 1
    time.sleep(0.3)

print("\n{}/{} MP3 files pushed".format(success, len(mp3_files)))
