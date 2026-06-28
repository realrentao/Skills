#!/usr/bin/env python3
"""Fix remaining Italian accents in data files, regenerate HTML, push"""
import os, re, sys, json, urllib.request, base64, time, importlib.util

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"

# Read fix_duplicate_sets for EXTRA items
spec = importlib.util.spec_from_file_location("fix", os.path.join(REPO, "fix_duplicate_sets.py"))
fix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix)

import cils_data as cd, celi_data as ced

# Apply accent fixes to in-memory data
ACCENT_FIXES = {
    "liberta": "libertà",
    "poverta": "povertà",
    "natalita": "natalità",
    "solidarieta": "solidarietà",
    "responsabilita": "responsabilità",
    "siccita": "siccità",
}

# Fix all items in all sections
for data, extra in [(cd.CILS, fix.EXTRA_CILS), (ced.CELI, fix.EXTRA_CELI)]:
    for lv in ["A1","A2","B1","B2","C1","C2"]:
        for sec in ["ascolto","lettura","grammatica","scrittura","orale"]:
            items = data[lv][sec]
            for idx, item in enumerate(items):
                new_item = list(item)
                changed = False
                # Fix opt string (element 1)
                if len(new_item) > 1 and isinstance(new_item[1], str):
                    for old, new in ACCENT_FIXES.items():
                        if old in new_item[1] and new not in new_item[1]:
                            new_item[1] = new_item[1].replace(old, new)
                            changed = True
                # Fix script text (element 3)  
                if len(new_item) > 3 and isinstance(new_item[3], str):
                    for old, new in ACCENT_FIXES.items():
                        if old in new_item[3] and new not in new_item[3]:
                            new_item[3] = new_item[3].replace(old, new)
                            changed = True
                if changed:
                    data[lv][sec][idx] = tuple(new_item)
            # Also add EXTRA items
            if sec == "ascolto" and lv in extra:
                for item in extra[lv]:
                    data[lv][sec].append(item)

# Now regenerate HTML using fix_duplicate_sets.py logic
CSS = open(os.path.join(REPO, "fix_duplicate_sets.py"), "r", encoding="utf-8").read()
css_start = CSS.find('CSS = """') + len('CSS = """')
css_end = CSS.find('"""', css_start)
CSS_VAL = CSS[css_start:css_end]
js_start = CSS.find('JS = r"""') + len('JS = r"""')
js_end = CSS.find('"""', js_start)
JS_VAL = CSS[js_start:js_end]

# Fix JS to use kwlist instead of kws
JS_VAL = JS_VAL.replace(
    "kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ans=q.getAttribute('data-answer')||kws[0]||'';var sc=kws(ut,kws);t+=sc;T+=sc",
    "kwlist=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ans=q.getAttribute('data-answer')||kwlist[0]||'';var sc=kws(ut,kwlist);t+=sc;T+=sc")
JS_VAL = JS_VAL.replace(
    "kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ref=q.getAttribute('data-reference')||'';var base=kws(ut,kws),bonus",
    "kwlist=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ref=q.getAttribute('data-reference')||'';var base=kws(ut,kwlist),bonus")

LEVELS = ["A1","A2","B1","B2","C1","C2"]
LV_NAMES = {"A1":"Base","A2":"Elementare","B1":"Intermedio","B2":"Intermedio-Avanzato","C1":"Avanzato","C2":"Padronanza"}

import add_answers as aa

def gen_html(data, cert, lv, s):
    lines = []
    sec_names = {"ascolto":"Ascolto","lettura":"Lettura","grammatica":"Grammatica","scrittura":"Scrittura","orale":"Produzione orale"}
    sec_ids = ["ascolto","lettura","grammatica","scrittura","orale"]
    sec_max = {"ascolto":20,"lettura":20,"grammatica":20,"scrittura":20,"orale":20}
    sec_counts = {"ascolto":5,"lettura":2,"grammatica":3,"scrittura":1,"orale":1}
    
    for sid, sec_id in enumerate(sec_ids):
        items = data[lv].get(sec_id, [])
        n_items = min(sec_counts[sec_id], len(items))
        base_idx = (s - 1) * n_items
        max_pts = sec_max[sec_id]
        
        lines.append(f'<div class="section" id="sec_{sec_id}"><h2>Prova {sid+1} - {sec_names[sec_id]} <span style="font-weight:400;font-size:13px;color:#999;">(max {max_pts} pt)</span></h2>')
        
        for idx in range(n_items):
            data_idx = base_idx + idx
            if data_idx >= len(items): data_idx = idx % len(items)
            item = items[data_idx]
            pts = max_pts // n_items
            
            if sec_id == "ascolto":
                q, opts_str, ans, script = item[0], item[1], item[2], item[3]
                opts = opts_str.split("|")
                audio_name = f"{cert.lower()}_{s}_{idx+1}_{lv.lower()}"
                script_esc = script.replace("'", "&#39;")
                lines.append(f'<div class="question stem" data-type="listen" data-ans="{ans}" data-points="{pts}" data-script="{script_esc}"><button class="play-btn" data-audio-js="../audio/{audio_name}" onclick="playAudio(this)">Ascolta</button><button class="script-btn" onclick="showScript(this)">Testo</button><div class="question-text">{q}</div><div class="opts">')
                for oi, opt in enumerate(opts):
                    lines.append(f'<label><input type="radio" name="q_{sec_id}_{idx}_{s}" value="{oi}"> {opt}</label>')
                lines.append('</div><div class="feedback"></div></div>')
            
            elif sec_id == "lettura":
                q, opts_str, ans, text = item[0], item[1], item[2], item[3]
                opts = opts_str.split("|")
                lines.append(f'<div class="question stem" data-type="read" data-ans="{ans}" data-points="{pts}"><div class="text">{text}</div><div class="question-text">{q}</div><div class="opts">')
                for oi, opt in enumerate(opts):
                    lines.append(f'<label><input type="radio" name="q_lettura_{idx}_{s}" value="{oi}"> {opt}</label>')
                lines.append('</div><div class="feedback"></div></div>')
            
            elif sec_id == "grammatica":
                q, kw_str = item[0], item[1]
                first_ans = kw_str.split("|")[0]
                lines.append(f'<div class="question" data-type="grammar" data-answer="{first_ans}" data-keywords="{kw_str}" data-points="{pts}"><div class="question-text">{q}</div><input type="text" placeholder="Scrivi..." autocomplete="off"><div class="feedback"></div></div>')
            
            elif sec_id == "scrittura":
                q, kws = item[0], item[1]
                ref = ""
                try: ref = aa.REFERENCES[cert]["scrittura"][lv][(s-1)*1 + data_idx % 5]
                except: ref = kws
                ref_esc = ref.replace("'", "&#39;").replace('"', "&quot;")
                lines.append(f'<div class="question" data-type="scrittura" data-keywords="{kws}" data-reference="{ref_esc}" data-points="{max_pts}"><div class="question-text">{q}</div><textarea rows="4" placeholder="Scrivi qui..." autocomplete="off"></textarea><div class="feedback"></div></div>')
            
            elif sec_id == "orale":
                q, kws = item[0], item[1]
                ref = ""
                try: ref = aa.REFERENCES[cert]["orale"][lv][(s-1)*1 + data_idx % 5]
                except: ref = kws
                ref_esc = ref.replace("'", "&#39;").replace('"', "&quot;")
                lines.append(f'<div class="question" data-type="orale" data-keywords="{kws}" data-reference="{ref_esc}" data-points="{max_pts}"><div class="question-text">{q}</div><textarea rows="4" placeholder="Rispondi qui..." autocomplete="off"></textarea><div class="feedback"></div></div>')
        
        lines.append('</div>')
    
    return "\n".join(lines)

# Generate all 60 pages
count = 0
for cert, data in [("CILS", cd.CILS), ("CELI", ced.CELI)]:
    for lv in LEVELS:
        for s in range(1, 6):
            out_dir = os.path.join(REPO, cert, lv, f"Set_{s}")
            os.makedirs(out_dir, exist_ok=True)
            title = f"{cert} - {LV_NAMES[lv]} ({lv}) - Simulazione {s}"
            body = gen_html(data, cert, lv, s)
            nav = f'<div class="top-band"></div><div class="container"><div class="header"><h1>{cert} <small>{LV_NAMES[lv]} ({lv}) - Simulazione {s}</small></h1><div class="meta">Certificazione di lingua italiana · 5 prove</div></div>'
            nav += '<div id="scoreBar" class="score-bar"><h2 id="totalScore">0/100</h2><p id="scoreMessage"></p></div>'
            nav += body
            nav += '<div id="answerReference" style="display:none;"><h3>Risultati</h3><table id="resultTable"><thead><tr><th>Sezione</th><th>Punteggio</th><th>Max</th></tr></thead><tbody id="resultBody"></tbody></table></div>'
            nav += '<div class="btn-row"><button class="btn primary" onclick="sub()">Invia e valuta</button><button class="btn secondary" onclick="reset()">Ricomincia</button></div></div>'
            full = f'<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title}</title><style>{CSS_VAL}</style></head><body>{nav}<script>{JS_VAL}</script></body></html>'
            fp = os.path.join(out_dir, f"{cert}_{lv}_Set_{s}.html")
            with open(fp, "wb") as f: f.write(full.encode("utf-8"))
            count += 1

print(f"HTML regenerated: {count} pages")

# Push to GitHub
TOKEN = os.environ.get('GITHUB_TOKEN', '')
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
                    sha = json.loads(urllib.request.urlopen(r, timeout=8).read())["sha"]
                except: pass
                with open(fp, "rb") as f:
                    content = base64.b64encode(f.read()).decode()
                data = json.dumps({"message": "Fix accents data sources", "content": content, "branch": "master", "sha": sha} if sha else {"message": "Fix accents data", "content": content, "branch": "master"})
                r2 = urllib.request.Request(url, method="PUT", data=data.encode(), headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
                try:
                    json.loads(urllib.request.urlopen(r2, timeout=10).read())
                    pushed += 1
                    break
                except: pass
            time.sleep(0.15)

print(f"Pushed: {pushed} files")
