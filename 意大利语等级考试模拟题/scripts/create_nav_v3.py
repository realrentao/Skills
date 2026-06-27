#!/usr/bin/env python3
"""Create navigation for CILS/CELI dual-section structure"""
import os

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"
LEVELS = ["A1","A2","B1","B2","C1","C2"]
LV_NAMES = {"A1":"Base","A2":"Elementare","B1":"Intermedio","B2":"Intermedio-Avanzato","C1":"Avanzato","C2":"Padronanza"}

nav_css = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Lato',-apple-system,'Segoe UI',sans-serif;background:#FDF8F3;color:#2C1810}
.top-band{height:4px;background:linear-gradient(90deg,#009246 0%,#009246 33%,#FFF 33%,#FFF 66%,#CE2B37 66%,#CE2B37 100%)}
.container{max-width:1000px;margin:0 auto;padding:40px 20px}
.header{text-align:center;margin-bottom:40px}
.header h1{font-family:'Playfair Display',Georgia,serif;font-size:34px;margin-bottom:6px}
.header p{font-size:14px;color:#666}
.cert-row{display:flex;gap:30px;margin-bottom:30px}
.cert-box{flex:1;background:#FFF;border:1px solid #E8DCD0;border-radius:8px;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,0.06)}
.cert-header{color:#FFF;padding:16px 20px;font-family:'Playfair Display',Georgia,serif;font-size:20px}
.cert-header.cils{background:linear-gradient(135deg,#003D7A,#0055B3)}
.cert-header.celi{background:linear-gradient(135deg,#6A1B1A,#8B2C2A)}
.cert-body{padding:20px}
.level-card{margin-bottom:12px;border:1px solid #E8DCD0;border-radius:8px;overflow:hidden}
.lv-header{background:#FAF5F0;padding:8px 14px;font-weight:600;font-size:14px;border-bottom:1px solid #E8DCD0}
.lv-body{padding:10px 14px;display:flex;gap:6px;flex-wrap:wrap}
.set-btn{display:inline-block;padding:6px 14px;background:#FFF;color:#2C1810;border:1px solid #009246;border-radius:6px;text-decoration:none;font-size:13px;transition:all 0.2s}
.set-btn:hover{background:#009246;color:#FFF}
.footer{text-align:center;margin-top:40px;font-size:13px;color:#999}"""

def gen_main():
    certs = [
        ("CILS", "cils", "CILS - Universita per Stranieri di Siena", "Certificazione di italiano generale"),
        ("CELI", "celi", "CELI - Universita per Stranieri di Perugia", "Certificazione di italiano generale"),
    ]
    cert_boxes = ""
    for name, cls, title, desc in certs:
        levels = ""
        for lv in LEVELS:
            sets = "".join(f'<a href="{name}/{lv}/Set_{s}/{name}_{lv}_Set_{s}.html" class="set-btn">Set {s}</a>' for s in range(1,6))
            levels += f'<div class="level-card"><div class="lv-header">{lv} - {LV_NAMES[lv]}</div><div class="lv-body">{sets}</div></div>'
        cert_boxes += f'<div class="cert-box"><div class="cert-header {cls}">{title}</div><div class="cert-body">{levels}</div></div>'
    
    html = f"""<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Simulazioni - Italiano</title><style>{nav_css}</style></head><body>
<div class="top-band"></div>
<div class="container">
<div class="header">
  <h1>Lingua Italiana</h1>
  <p>60 simulazioni complete · CILS e CELI · A1 → C2 · 5 set per livello</p>
</div>
<div class="cert-row">{cert_boxes}</div>
<div class="footer">Italian Business Style &copy; 2026</div>
</div></body></html>"""
    
    with open(os.path.join(REPO, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Main navigation created!")

gen_main()
