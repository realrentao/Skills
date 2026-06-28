#!/usr/bin/env python3
"""Final comprehensive accent fix for ALL HTML files + push"""
import os, re, sys, json, urllib.request, base64, time

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"
LEVELS = ["A1","A2","B1","B2","C1","C2"]
TOKEN = os.environ.get('GITHUB_TOKEN', '')

# Comprehensive list of accent fixes (raw text replacements)
RAW_FIXES = [
    # università
    ("universita ", "università "),
    ("universita.", "università."),
    ("universita'", "università"),
    # città
    (" In citta<", " In città<"),
    (" In citta.", " In città."),
    ("citta ", "città "),
    ("Citta ", "Città "),
    # è (verb "to be")
    (" e la ", " è la "),
    (" e il ", " è il "),
    (" e un ", " è un "),
    (" e una ", " è una "),
    (" e in ", " è in "),
    (" e per ", " è per "),
    (" e molto ", " è molto "),
    (" e ora ", " è ora "),
    (" e qui ", " è qui "),
    (" e stato ", " è stato "),
    (" e stata ", " è stata "),
    (" e molto ", " è molto "),
    (" e sempre ", " è sempre "),
    (" e anche ", " è anche "),
    ("E una ", "È una "),
    ("E un ", "È un "),
    ("E il ", "È il "),
    ("E la ", "È la "),
    ("E in ", "È in "),
    # perché
    (" perche ", " perché "),
    (" perche.", " perché."),
    (" perche?", " perché?"),
    ("perche' ", "perché "),
    ("Perche ", "Perché "),
    # più
    (" piu ", " più "),
    ("Piu ", "Più "),
    # può
    (" puo ", " può "),
    ("Puo ", "Può "),
    # già
    (" gia ", " già "),
    ("Gia ", "Già "),
    # così
    (" cosi ", " così "),
    ("Cosi ", "Così "),
    # caffè
    (" caffe ", " caffè "),
    # sarà
    (" sara ", " sarà "),
    ("Sara ", "Sarà "),
    # perciò
    (" percio ", " perciò "),
    # days of week
    (" lunedi ", " lunedì "),
    (" martedi ", " martedì "),
    (" mercoledi ", " mercoledì "),
    (" giovedi ", " giovedì "),
    (" venerdi ", " venerdì "),
    # other common
    (" difficolta ", " difficoltà "),
    (" possibilita ", " possibilità "),
    (" societa ", " società "),
    ("Societa ", "Società "),
    (" attivita ", " attività "),
]

count_modified = 0
count_issues_fixed = 0

for cert in ["CILS", "CELI"]:
    for lv in LEVELS:
        for s in range(1, 6):
            fp = os.path.join(REPO, cert, lv, f"Set_{s}", f"{cert}_{lv}_Set_{s}.html")
            with open(fp, "r", encoding="utf-8") as f:
                html = f.read()
            
            original = html
            file_issues = 0
            for old, new in RAW_FIXES:
                if old in html:
                    n = html.count(old)
                    file_issues += n
                    html = html.replace(old, new)
            
            if html != original:
                with open(fp, "wb") as f:
                    f.write(html.encode("utf-8"))
                count_modified += 1
                count_issues_fixed += file_issues

print(f"Fixed {count_issues_fixed} accent issues across {count_modified} HTML files")

# Also fix data files for future regenerations
def fix_data_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in RAW_FIXES:
        if old in content:
            content = content.replace(old, new)
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

fix_data_file(os.path.join(REPO, "cils_data.py"))
fix_data_file(os.path.join(REPO, "celi_data.py"))
print("Data files updated")

# Push to GitHub
print("Pushing to GitHub...")
pushed = 0
for cert in ["CILS", "CELI"]:
    for lv in LEVELS:
        for s in range(1, 6):
            rel = f"{cert}/{lv}/Set_{s}/{cert}_{lv}_Set_{s}.html"
            fp = os.path.join(REPO, *rel.split("/"))
            url = f"https://api.github.com/repos/realrentao/italiano-esami/contents/{rel}"
            for attempt in range(3):
                sha = None
                try:
                    r = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json"})
                    sha = json.loads(urllib.request.urlopen(r, timeout=10).read())["sha"]
                except: pass
                with open(fp, "rb") as f:
                    content = base64.b64encode(f.read()).decode()
                data = json.dumps({"message": "Fix remaining accents in texts and scripts", "content": content, "branch": "master", "sha": sha} if sha else {"message": "Fix remaining accents", "content": content, "branch": "master"})
                r2 = urllib.request.Request(url, method="PUT", data=data.encode(), headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
                try:
                    json.loads(urllib.request.urlopen(r2, timeout=30).read())
                    pushed += 1
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 409 and attempt < 2:
                        time.sleep(2); continue
                    break
            time.sleep(0.3)

# Push nav
fp = os.path.join(REPO, "index.html")
url = "https://api.github.com/repos/realrentao/italiano-esami/contents/index.html"
for attempt in range(3):
    sha = None
    try:
        r = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json"})
        sha = json.loads(urllib.request.urlopen(r, timeout=10).read())["sha"]
    except: pass
    with open(fp, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    data = json.dumps({"message": "Fix accents nav", "content": content, "branch": "master", "sha": sha} if sha else {"message": "Fix accents nav", "content": content, "branch": "master"})
    r2 = urllib.request.Request(url, method="PUT", data=data.encode(), headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
    try:
        json.loads(urllib.request.urlopen(r2, timeout=30).read())
        pushed += 1
        break
    except urllib.error.HTTPError as e:
        if e.code == 409 and attempt < 2:
            time.sleep(2); continue
        break

print(f"Pushed: {pushed} files")
