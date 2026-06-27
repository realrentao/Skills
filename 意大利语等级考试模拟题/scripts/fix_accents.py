#!/usr/bin/env python3
"""Fix missing Italian accents in data files, regenerate HTML, push to GitHub"""
import os, re, sys, json, urllib.request, base64, time, asyncio, edge_tts
sys.path.insert(0, r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami")

# Common Italian accent replacements
# Pattern: (exact word to replace, corrected word)
REPLACEMENTS = [
    # Words missing grave/acute accents
    (" perche ", " perché "),
    (" perche?", " perché?"),
    (" perche.", " perché."),
    (" perche,", " perché,"),
    ("'perche ", "'perché "),
    ("perche'", "perché"),
    ("Perche ", "Perché "),
    (" percio ", " perciò "),
    (" puo ", " può "),
    ("Puo ", "Può "),
    (" piu ", " più "),
    ("Piu ", "Più "),
    (" gia ", " già "),
    ("Gia ", "Già "),
    (" cosi ", " così "),
    ("Cosi ", "Così "),
    (" e la ", " è la "),
    (" e il ", " è il "),
    (" e un ", " è un "),
    (" e una ", " è una "),
    (" e in ", " è in "),
    (" e per ", " è per "),
    (" e molto ", " è molto "),
    (" e stato ", " è stato "),
    (" e stata ", " è stata "),
    (" e molto ", " è molto "),
    (" e qui ", " è qui "),
    (" e ora ", " è ora "),
    (" e una ", " è una "),
    ("E una ", "È una "),
    ("E un ", "È un "),
    ("E il ", "È il "),
    ("E la ", "È la "),
    ("E in ", "È in "),
    (" sara ", " sarà "),
    ("Sara ", "Sarà "),
    (" caffe ", " caffè "),
    ("Caffe ", "Caffè "),
    (" lunedi ", " lunedì "),
    (" martedi ", " martedì "),
    (" mercoledi ", " mercoledì "),
    (" giovedi ", " giovedì "),
    (" venerdi ", " venerdì "),
    ("Lunedi ", "Lunedì "),
    ("Martedi ", "Martedì "),
    ("Mercoledi ", "Mercoledì "),
    ("Giovedi ", "Giovedì "),
    ("Venerdi ", "Venerdì "),
    # Words ending with a (feminine) vs à (accented verb/suffix)
    (" citta ", " città "),
    ("Citta ", "Città "),
    (" universita ", " università "),
    ("Universita ", "Università "),
    (" meta ", " metà "),
    (" difficolta ", " difficoltà "),
    (" possibilita ", " possibilità "),
    (" universita'", "università"),
    (" papa ", " papà "),  # dad vs pope context - mostly dad in our data
    # Missing grave on final ì
    (" cosi'", " così"),
    # Words that end with accented vowels
    ("pero ", "però "),
    ("Pero ", "Però "),
    (" percio'", " perciò"),
    ("neanche ", "neanche "),  # no accent
    # è alone  
    (" e' ", " è "),
    (" studio'", " studiò"),
    # Ensure correct quoting in HTML context
    ("E' ", "È "),
]

def fix_text(text):
    """Apply accent replacements to text"""
    for old, new in REPLACEMENTS:
        if old in text:
            text = text.replace(old, new)
    return text

def fix_file(filepath):
    """Fix all accent issues in a data file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply replacements to string literals (content between quotes)
    original = content
    replacements_found = 0
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            replacements_found += 1
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return replacements_found
    return 0

# Fix data files
count = fix_file(r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami\cils_data.py")
count += fix_file(r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami\celi_data.py")
print(f"Data files fixed: {count} replacements")

# Verify syntax
import py_compile
py_compile.compile(r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami\cils_data.py", doraise=True)
py_compile.compile(r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami\celi_data.py", doraise=True)
print("Syntax OK")

# Regenerate HTML using fix_duplicate_sets.py logic
REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"
LEVELS = ["A1","A2","B1","B2","C1","C2"]

import cils_data, celi_data

CSS = open(os.path.join(REPO, "fix_duplicate_sets.py"), "r", encoding="utf-8").read()
css_start = CSS.find('CSS = """') + len('CSS = """')
css_end = CSS.find('"""', css_start)
CSS_VAL = CSS[css_start:css_end]
js_start = CSS.find('JS = r"""') + len('JS = r"""')
js_end = CSS.find('"""', js_start)
JS_VAL = CSS[js_start:js_end]

LV_NAMES = {"A1":"Base","A2":"Elementare","B1":"Intermedio","B2":"Intermedio-Avanzato","C1":"Avanzato","C2":"Padronanza"}

def sections_from_data(data, cert, lv, set_n):
    lines = []
    sec_names = {"ascolto":"Ascolto","lettura":"Lettura","grammatica":"Grammatica","scrittura":"Scrittura","orale":"Produzione orale"}
    sec_ids = ["ascolto","lettura","grammatica","scrittura","orale"]
    sec_max = {"ascolto":20,"lettura":20,"grammatica":20,"scrittura":20,"orale":20}
    sec_counts = {"ascolto":5,"lettura":2,"grammatica":3,"scrittura":1,"orale":1}
    
    # Import reference answers
    import add_answers as aa
    
    for sid, sec_id in enumerate(sec_ids):
        items = data[lv].get(sec_id, [])
        n_items = min(sec_counts[sec_id], len(items))
        base_idx = (set_n - 1) * n_items
        max_pts = sec_max[sec_id]
        
        lines.append(f'<div class="section" id="sec_{sec_id}">')
        lines.append(f'  <h2>Prova {sid+1} - {sec_names[sec_id]} <span style="font-weight:400;font-size:13px;color:#999;">(max {max_pts} pt)</span></h2>')
        
        for idx in range(n_items):
            data_idx = base_idx + idx
            if data_idx >= len(items):
                data_idx = idx % len(items)
            item = items[data_idx]
            pts = max_pts // n_items
            
            if sec_id == "ascolto":
                q, opts_str, ans, script = item[0], item[1], item[2], item[3]
                opts = opts_str.split("|")
                audio_name = f"{cert.lower()}_{set_n}_{idx+1}_{lv.lower()}"
                script_esc = script.replace("'", "&#39;")
                lines.append(f'  <div class="question stem" data-type="listen" data-ans="{ans}" data-points="{pts}" data-script="{script_esc}">')
                lines.append(f'    <button class="play-btn" data-audio-js="../audio/{audio_name}" onclick="playAudio(this)">Ascolta</button>')
                lines.append(f'    <button class="script-btn" onclick="showScript(this)">Testo</button>')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <div class="opts">')
                for oi, opt in enumerate(opts):
                    lines.append(f'      <label><input type="radio" name="q_{sec_id}_{idx}_{set_n}" value="{oi}"> {opt}</label>')
                lines.append(f'    </div>')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "lettura":
                q, opts_str, ans, text = item[0], item[1], item[2], item[3]
                opts = opts_str.split("|")
                lines.append(f'  <div class="question stem" data-type="read" data-ans="{ans}" data-points="{pts}">')
                lines.append(f'    <div class="text">{text}</div>')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <div class="opts">')
                for oi, opt in enumerate(opts):
                    lines.append(f'      <label><input type="radio" name="q_lettura_{idx}_{set_n}" value="{oi}"> {opt}</label>')
                lines.append(f'    </div>')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "grammatica":
                q, kw_str = item[0], item[1]
                first_ans = kw_str.split("|")[0]
                lines.append(f'  <div class="question" data-type="grammar" data-answer="{first_ans}" data-keywords="{kw_str}" data-points="{pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <input type="text" placeholder="Scrivi..." autocomplete="off">')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "scrittura":
                q, kws = item[0], item[1]
                ref = ""
                try: ref = aa.REFERENCES[cert]["scrittura"][lv][(set_n-1)*1 + data_idx % 5]
                except: ref = kws
                ref_esc = ref.replace("'", "&#39;").replace('"', "&quot;")
                lines.append(f'  <div class="question" data-type="scrittura" data-keywords="{kws}" data-reference="{ref_esc}" data-points="{max_pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <textarea rows="4" placeholder="Scrivi qui..." autocomplete="off"></textarea>')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "orale":
                q, kws = item[0], item[1]
                ref = ""
                try: ref = aa.REFERENCES[cert]["orale"][lv][(set_n-1)*1 + data_idx % 5]
                except: ref = kws
                ref_esc = ref.replace("'", "&#39;").replace('"', "&quot;")
                lines.append(f'  <div class="question" data-type="orale" data-keywords="{kws}" data-reference="{ref_esc}" data-points="{max_pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <textarea rows="4" placeholder="Rispondi qui..." autocomplete="off"></textarea>')
                lines.append(f'    <div class="feedback"></div></div>')
        
        lines.append('</div>')
    
    return "\n".join(lines)

# Enhanced JS with kwlist fix
JS_ENHANCED = JS_VAL.replace("""var inp=q.querySelector('input[type="text"]'),ut=inp?inp.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ans=q.getAttribute('data-answer')||kws[0]||'';var sc=kws(ut,kws);t+=sc;T+=sc""",
    """var inp=q.querySelector('input[type="text"]'),ut=inp?inp.value.trim():'',kwlist=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ans=q.getAttribute('data-answer')||kwlist[0]||'';var sc=kws(ut,kwlist);t+=sc;T+=sc""")
JS_ENHANCED = JS_ENHANCED.replace("""kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ref=q.getAttribute('data-reference')||'';var base=kws(ut,kws),bonus""",
    """kwlist=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ref=q.getAttribute('data-reference')||'';var base=kws(ut,kwlist),bonus""")

# Generate HTML
count = 0
for cert, data in [("CILS", cils_data.CILS), ("CELI", celi_data.CELI)]:
    for lv in LEVELS:
        for s in range(1, 6):
            out_dir = os.path.join(REPO, cert, lv, f"Set_{s}")
            os.makedirs(out_dir, exist_ok=True)
            title = f"{cert} - {LV_NAMES[lv]} ({lv}) - Simulazione {s}"
            body_html = sections_from_data(data, cert, lv, s)
            nav = f'<div class="top-band"></div><div class="container"><div class="header"><h1>{cert} <small>{LV_NAMES[lv]} ({lv}) - Simulazione {s}</small></h1><div class="meta">Certificazione di lingua italiana · 5 prove</div></div>'
            nav += '<div id="scoreBar" class="score-bar"><h2 id="totalScore">0/100</h2><p id="scoreMessage"></p></div>'
            nav += body_html
            nav += '<div id="answerReference" style="display:none;"><h3>Risultati</h3><table id="resultTable"><thead><tr><th>Sezione</th><th>Punteggio</th><th>Max</th></tr></thead><tbody id="resultBody"></tbody></table></div>'
            nav += '<div class="btn-row"><button class="btn primary" onclick="sub()">Invia e valuta</button><button class="btn secondary" onclick="reset()">Ricomincia</button></div></div>'
            full = f'<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title}</title><style>{CSS_VAL}</style></head><body>{nav}<script>{JS_ENHANCED}</script></body></html>'
            fp = os.path.join(out_dir, f"{cert}_{lv}_Set_{s}.html")
            with open(fp, "wb") as f:
                f.write(full.encode("utf-8"))
            count += 1

print(f"HTML regenerated: {count} pages")

# Generate nav page
nav_html = '<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Italiano Esami</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Lato",sans-serif;background:#FDF8F3;color:#2C1810}.top-band{height:4px;background:linear-gradient(90deg,#009246,#009246 33%,#FFF 33%,#FFF 66%,#CE2B37 66%,#CE2B37 100%)}h1{text-align:center;font-family:Georgia,serif;font-size:28px;margin:20px 0 8px}.subtitle{text-align:center;color:#666;font-size:14px;margin-bottom:30px}.cert-row{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:1100px;margin:0 auto}.cert-box{border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08)}.cert-header{padding:18px 22px;color:#FFF;font-family:Georgia,serif;font-size:17px;font-weight:600}.cert-header.cils{background:linear-gradient(135deg,#003D7A,#0055B3)}.cert-header.celi{background:linear-gradient(135deg,#7A0000,#B3002D)}.cert-body{padding:16px;background:#FFF}.level-card{margin-bottom:10px}.lv-header{font-weight:600;font-size:14px;padding:6px 0;border-bottom:1px solid #F0EAE4}.lv-body{display:flex;flex-wrap:wrap;gap:4px}.set-btn{display:inline-block;padding:4px 12px;border-radius:14px;font-size:12px;text-decoration:none;color:#FFF}.cert-header.cils~.cert-body .set-btn{background:#0055B3}.cert-header.celi~.cert-body .set-btn{background:#B3002D}@media(max-width:700px){.cert-row{grid-template-columns:1fr}}</style></head><body><div class="top-band"></div><h1>Italiano Esami</h1><p class="subtitle">60 simulazioni &middot; A1 &rarr; C2 &middot; 5 set per livello</p><div class="cert-row">'
for cert, color in [("CILS", "cils"), ("CELI", "celi")]:
    nav_html += f'<div class="cert-box"><div class="cert-header {color}">{cert} - Esami completi</div><div class="cert-body">'
    for lv in LEVELS:
        nav_html += f'<div class="level-card"><div class="lv-header">{lv} - {LV_NAMES[lv]}</div><div class="lv-body">'
        for s in range(1, 6):
            nav_html += f'<a href="{cert}/{lv}/Set_{s}/{cert}_{lv}_Set_{s}.html" class="set-btn">Set {s}</a>'
        nav_html += '</div></div>'
    nav_html += '</div></div>'
nav_html += '</div></div></body></html>'
with open(os.path.join(REPO, "index.html"), "w", encoding="utf-8") as f:
    f.write(nav_html)
print("Nav generated")

# Push to GitHub
TOKEN='${GITHUB_TOKEN}'
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
                data = json.dumps({"message": "Fix Italian accents (è, à, ì, ò, ù)", "content": content, "branch": "master", "sha": sha} if sha else {"message": "Fix Italian accents", "content": content, "branch": "master"})
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
    data = json.dumps({"message": "Fix Italian accents nav", "content": content, "branch": "master", "sha": sha} if sha else {"message": "Fix Italian accents nav", "content": content, "branch": "master"})
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
print("ALL DONE")
