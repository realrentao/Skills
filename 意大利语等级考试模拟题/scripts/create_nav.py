#!/usr/bin/env python
"""Create navigation pages: multi-set structure"""
import os

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"

# All 6 sets × 6 levels
EXAM_SETS = {
    "CILS": {
        "name": "CILS",
        "org": "Università per Stranieri di Siena",
        "color": "#1a5276",
        "subsets": [
            ("CILS1", "Simulazione 1", "blue"),
            ("CILS2", "Simulazione 2", "blue"),
            ("CILS3", "Simulazione 3", "blue")
        ],
        "levels": [
            ("A1", "Principiante", "green"),
            ("A2", "Elementare", "teal"),
            ("B1", "Intermedio", "blue"),
            ("B2", "Intermedio sup.", "purple"),
            ("C1", "Avanzato", "coral"),
            ("C2", "Padronanza", "red"),
        ]
    },
    "CELI": {
        "name": "CELI",
        "org": "Università per Stranieri di Perugia",
        "color": "#6c3483",
        "subsets": [
            ("CELI1", "Simulazione 1", "purple"),
            ("CELI2", "Simulazione 2", "purple"),
            ("CELI3", "Simulazione 3", "purple")
        ],
        "levels": [
            ("Impatto (A1)", "Principiante", "green"),
            ("1 (A2)", "Elementare", "teal"),
            ("2 (B1)", "Intermedio", "blue"),
            ("3 (B2)", "Intermedio sup.", "purple"),
            ("4 (C1)", "Avanzato", "coral"),
            ("5 (C2)", "Padronanza", "red"),
        ]
    }
}

NAV_CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; color: #fff; }
  .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
  h1 { text-align: center; font-size: 32px; font-weight: 300; letter-spacing: 2px; margin-bottom: 8px; }
  .subtitle { text-align: center; font-size: 14px; opacity: .6; margin-bottom: 40px; }
  .exam-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 30px 0; }
  .exam-card { background: rgba(255,255,255,.08); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; text-decoration: none; color: #fff; border: 1px solid rgba(255,255,255,.1); transition: all .3s ease; display: flex; flex-direction: column; }
  .exam-card:hover { transform: translateY(-4px); background: rgba(255,255,255,.14); border-color: rgba(255,255,255,.3); box-shadow: 0 20px 40px rgba(0,0,0,.3); }
  .exam-card .level { font-size: 28px; font-weight: 700; }
  .exam-card .desc { font-size: 13px; opacity: .7; margin-top: 4px; }
  .exam-card .badge { display: inline-block; font-size: 11px; padding: 2px 10px; border-radius: 10px; margin-top: 10px; }
  .badge.green { background: rgba(46,204,113,.3); color: #2ecc71; }
  .badge.teal { background: rgba(26,188,156,.3); color: #1abc9c; }
  .badge.blue { background: rgba(52,152,219,.3); color: #3498db; }
  .badge.purple { background: rgba(155,89,182,.3); color: #9b59b6; }
  .badge.coral { background: rgba(231,76,60,.3); color: #e74c3c; }
  .badge.red { background: rgba(192,57,43,.3); color: #c0392b; }
  .badge.orange { background: rgba(230,126,34,.3); color: #e67e22; }
  .back-link { display: inline-block; color: rgba(255,255,255,.6); text-decoration: none; font-size: 13px; margin-bottom: 20px; }
  .back-link:hover { color: #fff; }
  .back-link::before { content: '← '; }
  .exam-type { text-align: center; margin: 30px 0; }
  .exam-type a { display: inline-block; padding: 16px 48px; border-radius: 12px; text-decoration: none; color: #fff; font-size: 18px; margin: 10px; transition: all .3s; border: 1px solid rgba(255,255,255,.15); }
  .exam-type a:hover { transform: scale(1.02); background: rgba(255,255,255,.1); }
  .info-section { text-align: center; margin-top: 50px; padding: 30px; background: rgba(255,255,255,.05); border-radius: 16px; }
  .info-section p { font-size: 13px; opacity: .7; line-height: 1.8; }
"""

def gen_main_index():
    html = f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Esami Italiani Online — CILS &amp; CELI</title><style>{NAV_CSS}</style></head>
<body>
<div class="container">
  <span class="italian-flag" style="display:inline-flex;width:32px;height:22px;border-radius:3px;overflow:hidden;vertical-align:middle;margin-right:6px;"><span style="flex:1;background:#009246;"></span><span style="flex:1;background:#fff;"></span><span style="flex:1;background:#ce2b37;"></span></span>
  <h1 style="display:inline-block;vertical-align:middle;">Esami di Italiano</h1>
  <p class="subtitle">Simulazioni interattive CILS e CELI — 3 set ciascuno</p>
  
  <div class="exam-type">
    <a href="CILS/index.html" style="background:linear-gradient(135deg,#1a5276,#2e86c1);">📝 CILS<br><span style="font-size:12px;opacity:.8;">Università di Siena</span></a>
    <a href="CELI/index.html" style="background:linear-gradient(135deg,#6c3483,#a569bd);">📝 CELI<br><span style="font-size:12px;opacity:.8;">Università di Perugia</span></a>
  </div>

  <div class="info-section">
    <h3 style="font-weight:400;margin-bottom:10px;">Come funziona</h3>
    <p>
      Ogni certificazione offre <strong>3 set di simulazioni</strong>.<br>
      Ogni prova contiene 5 sezioni: Ascolto · Lettura · Grammatica · Scrittura · Produzione orale<br>
      Ascolta i file audio e premi <strong>"Invia e valuta"</strong> per ricevere il tuo punteggio.
    </p>
  </div>
</div>
</body></html>"""
    with open(os.path.join(REPO, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html (main)")

def gen_exam_type_index(exam_type, info):
    """Generate CILS/index.html or CELI/index.html — list of subsets"""
    cards = ""
    for subset_name, desc, color in info["subsets"]:
        cards += f"""  <a href="{subset_name}/index.html" class="exam-card">
    <span class="level">{subset_name}</span>
    <span class="desc">{desc}</span>
    <span class="badge {color}">{subset_name}</span>
  </a>
"""
    html = f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{exam_type} — Scegli il set</title><style>{NAV_CSS}</style></head>
<body>
<div class="container">
  <a class="back-link" href="../index.html">Torna alla home</a>
  <h1>📝 {exam_type} — Scegli il set</h1>
  <p class="subtitle">{info['org']}</p>
  <div class="exam-grid">
{cards}
  </div>
</div>
</body></html>"""
    out_dir = os.path.join(REPO, exam_type)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ {}/index.html".format(exam_type))

def gen_subset_index(exam_type, info, subset_name):
    """Generate CILS1/index.html etc — list of levels"""
    cards = ""
    for lv_name, desc, color in info["levels"]:
        # Extract level code: "A1" from "Impatto (A1)" or just "A1" from "A1"
        import re
        m = re.search(r'\(([^)]+)\)', lv_name)
        lv_key = m.group(1) if m else lv_name.split()[0]
        # Try set-prefixed name first (CILS2_A1.html), fall back to old style (CILS_A1.html)
        prefixed = "{}_{}.html".format(subset_name, lv_key)
        old_style = "{}_{}.html".format(subset_name[:4], lv_key)
        out_dir = os.path.join(REPO, exam_type, subset_name)
        file_name = prefixed if os.path.exists(os.path.join(out_dir, prefixed)) else old_style
        cards += f"""  <a href="{file_name}" class="exam-card">
    <span class="level">{lv_name}</span>
    <span class="desc">{desc}</span>
    <span class="badge {color}">{subset_name} {lv_key}</span>
  </a>
"""
    html = f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{exam_type} {subset_name} — Livelli</title><style>{NAV_CSS}</style></head>
<body>
<div class="container">
  <a class="back-link" href="../index.html">Torna ai set {exam_type}</a>
  <h1>📝 {exam_type} {subset_name}</h1>
  <p class="subtitle">Scegli il livello</p>
  <div class="exam-grid">
{cards}
  </div>
</div>
</body></html>"""
    out_dir = os.path.join(REPO, exam_type, subset_name)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ {}/{}/index.html".format(exam_type, subset_name))

def main():
    gen_main_index()
    for etype, info in EXAM_SETS.items():
        gen_exam_type_index(etype, info)
        for subset_name, _, _ in info["subsets"]:
            gen_subset_index(etype, info, subset_name)
    print("\n✅ All navigation pages created!")

if __name__ == "__main__":
    main()
