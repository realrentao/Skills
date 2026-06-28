#!/usr/bin/env python3
"""Generate 60 independent exam pages + 300 audio files + push to GitHub"""
import os, sys, base64, asyncio, edge_tts, json, urllib.request, time, re

# Import data
sys.path.insert(0, r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami")
import cils_data, celi_data

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"
LEVELS = ["A1","A2","B1","B2","C1","C2"]
LV_NAMES = {"A1":"Base","A2":"Elementare","B1":"Intermedio","B2":"Intermedio-Avanzato","C1":"Avanzato","C2":"Padronanza"}
TOKEN = os.environ.get('GITHUB_TOKEN', '')

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Lato',sans-serif;background:#FDF8F3;color:#2C1810}
.top-band{height:4px;background:linear-gradient(90deg,#009246,#009246 33%,#FFF 33%,#FFF 66%,#CE2B37 66%,#CE2B37 100%)}
.container{max-width:900px;margin:0 auto;padding:30px 20px 50px}
.header{background:linear-gradient(135deg,#2C1810,#4A2C1A);color:#FFF;padding:30px 35px;border-radius:8px;margin-bottom:24px;position:relative;overflow:hidden}
.header::before{content:'';position:absolute;top:0;right:0;width:120px;height:100%;background:repeating-linear-gradient(-45deg,transparent,transparent 8px,rgba(255,255,255,0.03) 8px,rgba(255,255,255,0.03) 16px)}
.header h1{font-family:Georgia,serif;font-weight:600;font-size:26px;margin-bottom:4px}
.header .meta{font-size:13px;opacity:0.7}
.score-bar{background:#FFF;border:1px solid #E8DCD0;border-radius:8px;padding:16px 24px;margin:0 0 24px;display:flex;align-items:center;justify-content:space-between}
.score-bar h2{font-size:20px;color:#009246;font-weight:700}
.score-bar p{font-size:13px;color:#666}
.section{background:#FFF;border:1px solid #E8DCD0;border-radius:8px;margin-bottom:18px;overflow:hidden}
.section h2{font-family:Georgia,serif;font-size:17px;padding:14px 22px;background:#FAF5F0;border-bottom:1px solid #E8DCD0;color:#2C1810}
.question{padding:16px 22px;border-bottom:1px solid #F0EAE4}
.question:last-child{border-bottom:none}
.question-text{font-weight:500;margin:8px 0;font-size:15px;line-height:1.5}
.text{background:#FAF5F0;border-left:3px solid #009246;padding:12px 16px;margin:8px 0;border-radius:0 6px;font-size:13px;line-height:1.6;color:#444}
.opts label{display:block;padding:7px 12px;margin:3px 0;border-radius:6px;cursor:pointer;font-size:14px}
.opts label:hover{background:#F5F0EB}
.opts input[type="radio"]{margin-right:8px;accent-color:#009246}
input[type="text"],textarea{width:100%;padding:10px 14px;border:1px solid #D4C8BC;border-radius:6px;font-size:14px}
.feedback{margin-top:8px;padding:8px 12px;border-radius:6px;font-size:13px;display:none}
.feedback.correct{display:block;background:#E8F5E9;color:#1B5E20;border-left:3px solid #009246}
.feedback.wrong{display:block;background:#FFEBEE;color:#B71C1C;border-left:3px solid #CE2B37}
.play-btn{padding:6px 16px;background:#2C1810;color:#FFF;border:none;border-radius:20px;cursor:pointer;font-size:12px}
.play-btn:hover{background:#4A2C1A}
.play-btn.playing{background:#CE2B37}
.play-btn.loading{background:#B8860B}
.script-btn{padding:4px 14px;background:#FFF;color:#B8860B;border:1px solid #B8860B;border-radius:20px;cursor:pointer;font-size:11px;margin-left:6px}
.script-btn:hover{background:#FFF8E1}
.script-text{margin-top:8px;padding:12px;background:#FFFBEB;border-radius:6px;font-size:13px;line-height:1.6;border-left:3px solid #B8860B;color:#5D4037}
.btn-row{text-align:center;padding:20px 0}
.btn{padding:12px 28px;border:none;border-radius:6px;cursor:pointer;font-size:14px;font-weight:600;margin:0 8px}
.btn.primary{background:#009246;color:#FFF}
.btn.primary:hover{background:#007A3B}
.btn.secondary{background:#FFF;color:#2C1810;border:1px solid #D4C8BC}
#answerReference{background:#FFF;border:1px solid #E8DCD0;border-radius:8px;padding:20px;margin-top:20px}
#answerReference h3{font-family:Georgia,serif;color:#009246}
#resultTable{width:100%;border-collapse:collapse;font-size:13px}
#resultTable th{background:#2C1810;color:#FFF;padding:8px 12px;text-align:left}
#resultTable td{padding:8px 12px;border-bottom:1px solid #F0EAE4}"""

JS = r"""var _audioCtx=null,_audioGen=0;
function _gAC(){if(!_audioCtx)_audioCtx=new(window.AudioContext||window.webkitAudioContext)();return _audioCtx}
function _stopC(){if(window._curSource){try{_curSource.stop()}catch(e){}window._curSource=null}if(window._curBtn){window._curBtn.classList.remove('playing');window._curBtn.innerHTML='Ascolta';window._curBtn=null}}
function playAudio(b){var s=b.getAttribute('data-audio-js')||b.getAttribute('data-audio-src');if(!s)return;var jm=b.getAttribute('data-audio-js');if(b.classList.contains('playing')){_stopC();return}_stopC();var g=++_audioGen;b.classList.add('loading');b.innerHTML='...';window._curBtn=b;
if(jm){window._audioLoaded=function(v){window._audioLoaded=null;if(g!==_audioGen)return;b.classList.remove('loading');var p=v.split(','),r=atob(p[1]),a=new ArrayBuffer(r.length),u=new Uint8Array(a);for(var i=0;i<r.length;i++)u[i]=r.charCodeAt(i);_pB(a)};var sc=document.createElement('script');sc.src=s+'.js?'+Date.now();sc.onerror=function(){b.classList.remove('loading');window._audioLoaded=null;b.innerHTML='Riprova'};document.head.appendChild(sc)}
else{fetch(s).then(function(r){if(!r.ok)throw Error(r.status);return r.arrayBuffer()}).then(function(a){if(g===_audioGen)_pB(a)}).catch(function(){b.classList.remove('loading');b.innerHTML='Riprova'})}}
function _pB(a){var c=_gAC();if(c.state==='suspended')c.resume();var b=window._curBtn;c.decodeAudioData(a,function(bu){var s=c.createBufferSource();s.buffer=bu;s.connect(c.destination);s.start(0);window._curSource=s;if(b){b.classList.remove('loading');b.classList.add('playing');b.innerHTML='Ferma'}s.onended=function(){_stopC()}},function(){if(b){b.classList.remove('loading');b.innerHTML='Riprova'}})}
function showScript(bn){var q=bn.closest('.question.stem')||bn.parentElement;if(!q)return;var st=q.getAttribute('data-script');if(!st)return;var e=q.querySelector('.script-text');if(!e){e=document.createElement('div');e.className='script-text';e.style.display='none';bn.parentNode.insertBefore(e,bn.nextSibling)}if(e.style.display==='none'||!e.textContent){e.textContent=st;e.style.display='block';bn.textContent='Nascondi testo'}else{e.style.display='none';bn.textContent='Testo'}}
function _n(s){return s.toLowerCase().replace(/[\s'\'`\u2018\u2019\.]+/g,' ').trim()}
function kws(t,k){if(!t||!k.length)return 0;var n=_n(t),h=0;k.forEach(function(w){if(n.indexOf(_n(w))>=0)h++});if(h===0&&t.trim().length>10)return 2;return Math.round((h/k.length)*20)}
function wc(t){return t.trim().split(/\s+/).filter(function(w){return w.length>0}).length}
function sub(){var T=0,M=0,D=[];document.querySelectorAll('.section').forEach(function(s){var t=0,m=0;s.querySelectorAll('.question').forEach(function(q){var tp=q.getAttribute('data-type'),pt=parseInt(q.getAttribute('data-points'))||4;m+=pt;M+=pt;
if(tp==='listen'||tp==='read'){var a=parseInt(q.getAttribute('data-ans')),sl=q.querySelector('input[type="radio"]:checked'),o=q.querySelectorAll('.opts label'),u=sl?o[parseInt(sl.value)].textContent.trim():'-',c=o[a]?o[a].textContent.trim():'-';if(sl&&parseInt(sl.value)===a){t+=pt;T+=pt;q.querySelector('.feedback').className='feedback correct';q.querySelector('.feedback').innerHTML='Corretto! ('+pt+'/'+pt+')'}else{q.querySelector('.feedback').className='feedback wrong';q.querySelector('.feedback').innerHTML='Risposta: '+u+' | Corretta: '+c+' (0/'+pt+')'}var st=q.getAttribute('data-script');if(st)q.querySelector('.feedback').innerHTML+='<br><span style="font-size:12px;color:#666;">'+st+'</span>'}
else if(tp==='grammar'){var inp=q.querySelector('input[type="text"]'),ut=inp?inp.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w});var sc=kws(ut,kws);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Corretto':'Parziale')+' ('+sc+'/'+pt+')'}
else if(tp==='scrittura'||tp==='orale'){var ta=q.querySelector('textarea'),ut=ta?ta.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),base=kws(ut,kws),bonus=Math.min(5,Math.floor(wc(ut)/10)),sc=Math.min(pt,base+bonus);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Buono':'Da migliorare')+' ('+sc+'/'+pt+')'}});D.push({name:s.querySelector('h2').textContent.replace(/<span.*/,'').trim(),score:t,max:m})});
var p=Math.round((T/M)*100);document.getElementById('totalScore').textContent=T+'/'+M;var msg=document.getElementById('scoreMessage');
if(p>=85)msg.innerHTML='<span class="score-grade" style="background:#E8F5E9;color:#009246;">Eccellente!</span>';else if(p>=70)msg.innerHTML='<span class="score-grade" style="background:#E3F2FD;color:#1565C0;">Buono!</span>';else if(p>=55)msg.innerHTML='<span class="score-grade" style="background:#FFF8E1;color:#B8860B;">Discreto</span>';else if(p>=40)msg.innerHTML='<span class="score-grade" style="background:#FBE9E7;color:#E65100;">Insufficiente</span>';else msg.innerHTML='<span class="score-grade" style="background:#FFEBEE;color:#CE2B37;">Grave</span>';
var rf=document.getElementById('answerReference');if(rf){rf.style.display='block';var tb=document.getElementById('resultBody');if(tb){tb.innerHTML='';D.forEach(function(d){tb.innerHTML+='<tr><td>'+d.name+'</td><td>'+d.score+'</td><td>'+d.max+'</td></tr>'})}}window.scrollTo({top:0,behavior:'smooth'})}
function reset(){document.querySelectorAll('input[type="radio"]').forEach(function(r){r.checked=false});document.querySelectorAll('input[type="text"]').forEach(function(t){t.value=''});document.querySelectorAll('textarea').forEach(function(t){t.value=''});document.querySelectorAll('.feedback').forEach(function(f){f.className='feedback';f.innerHTML=''});document.querySelectorAll('.script-text').forEach(function(s){s.style.display='none'});document.querySelectorAll('.script-btn').forEach(function(b){b.textContent='Testo'});document.getElementById('totalScore').textContent='0/100';document.getElementById('scoreMessage').innerHTML='';var rf=document.getElementById('answerReference');if(rf)rf.style.display='none';window.scrollTo({top:0,behavior:'smooth'})}"""

def sections_from_data(data, cert, lv, set_n):
    """Build HTML sections from question data"""
    lines = []
    sec_names = {"ascolto":"Ascolto","lettura":"Lettura","grammatica":"Grammatica","scrittura":"Scrittura","orale":"Produzione orale"}
    sec_ids = ["ascolto","lettura","grammatica","scrittura","orale"]
    sec_max = {"ascolto":20,"lettura":20,"grammatica":20,"scrittura":20,"orale":20}
    sec_counts = {"ascolto":5,"lettura":2,"grammatica":3,"scrittura":1,"orale":1}
    
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
                lines.append(f'  <div class="question" data-type="grammar" data-keywords="{kw_str}" data-points="{pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <input type="text" placeholder="Scrivi..." autocomplete="off">')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "scrittura":
                q, kws = item[0], item[1]
                word_count = "80-100" if lv in ["A1","A2"] else ("100-120" if lv in ["B1","B2"] else "120-150")
                lines.append(f'  <div class="question" data-type="scrittura" data-keywords="{kws}" data-points="{max_pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <textarea rows="4" placeholder="Scrivi qui..." autocomplete="off"></textarea>')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "orale":
                q, kws = item[0], item[1]
                lines.append(f'  <div class="question" data-type="orale" data-keywords="{kws}" data-points="{max_pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <textarea rows="4" placeholder="Rispondi qui..." autocomplete="off"></textarea>')
                lines.append(f'    <div class="feedback"></div></div>')
        
        lines.append('</div>')
    
    return "\n".join(lines)

def gen_html():
    """Generate all 60 HTML pages"""
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
                
                full = f'<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title}</title><style>{CSS}</style></head><body>{nav}<script>{JS}</script></body></html>'
                
                fp = os.path.join(out_dir, f"{cert}_{lv}_Set_{s}.html")
                with open(fp, "wb") as f:
                    f.write(full.encode("utf-8"))
                print(f"  HTML {cert}/{lv}/Set_{s}: {len(full)//1024}KB")
                count += 1
    print(f"HTML done: {count} pages")

async def gen_audio():
    """Generate all audio JS files"""
    VOICE = 'it-IT-IsabellaNeural'
    total = 0
    
    for cert, data in [("CILS", cils_data.CILS), ("CELI", celi_data.CELI)]:
        for lv in LEVELS:
            items = data[lv].get("ascolto", [])
            audio_dir = os.path.join(REPO, cert, lv, "audio")
            os.makedirs(audio_dir, exist_ok=True)
            
            for s in range(1, 6):
                for idx in range(5):
                    data_idx = (s - 1) * 5 + idx
                    if data_idx >= len(items):
                        data_idx = idx % len(items)
                    
                    script = items[data_idx][3]
                    audio_name = f"{cert.lower()}_{s}_{idx+1}_{lv.lower()}"
                    js_path = os.path.join(audio_dir, f"{audio_name}.js")
                    txt_path = os.path.join(audio_dir, f"{audio_name}.txt")
                    
                    # Write transcript
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(script + "\n")
                    
                    # Generate audio
                    communicate = edge_tts.Communicate(script, VOICE, rate="+5%")
                    await communicate.save("_tmp.mp3")
                    
                    with open("_tmp.mp3", "rb") as f:
                        b64 = "data:audio/mpeg;base64," + base64.b64encode(f.read()).decode()
                    os.remove("_tmp.mp3")
                    
                    js_code = f'(function(){{var b64="{b64}";if(window._audioLoaded)window._audioLoaded(b64);}})();'
                    with open(js_path, "w", encoding="utf-8") as f:
                        f.write(js_code)
                    
                    total += 1
                    if total % 30 == 0:
                        print(f"  Audio: {total}/300", flush=True)
    
    print(f"Audio done: {total} files")

def push_all():
    """Push all files to GitHub"""
    files = ["index.html"]
    for cert in ["CILS", "CELI"]:
        for lv in LEVELS:
            for s in range(1, 6):
                files.append(f"{cert}/{lv}/Set_{s}/{cert}_{lv}_Set_{s}.html")
            ad = os.path.join(REPO, cert, lv, "audio")
            if os.path.exists(ad):
                for f in sorted(os.listdir(ad)):
                    files.append(f"{cert}/{lv}/audio/{f}")
    
    pushed = 0
    for rel in files:
        fp = os.path.join(REPO, *rel.split("/"))
        if not os.path.exists(fp):
            continue
        sz = os.path.getsize(fp)
        if sz < 100 and rel.endswith(".txt"):
            continue  # skip empty txt
        
        url = f"https://api.github.com/repos/realrentao/italiano-esami/contents/{rel}"
        sha = None
        try:
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json"})
            sha = json.loads(urllib.request.urlopen(req, timeout=10).read())["sha"]
        except: pass
        
        with open(fp, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        data = {"message": "Independent CILS/CELI questions", "content": content, "branch": "master"}
        if sha: data["sha"] = sha
        
        req2 = urllib.request.Request(url, method="PUT", data=json.dumps(data).encode(), headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
        try:
            json.loads(urllib.request.urlopen(req2, timeout=30).read())
            pushed += 1
        except: pass
        time.sleep(0.2)
    
    print(f"Pushed: {pushed}/{len(files)} files")

def gen_nav():
    """Generate navigation page"""
    html = '<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Italiano Esami - Simulazioni CILS e CELI</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Lato",sans-serif;background:#FDF8F3;color:#2C1810;min-height:100vh}.top-band{height:4px;background:linear-gradient(90deg,#009246,#009246 33%,#FFF 33%,#FFF 66%,#CE2B37 66%,#CE2B37 100%)}.container{max-width:1100px;margin:0 auto;padding:30px 20px}h1{text-align:center;font-family:Georgia,serif;font-size:28px;margin:20px 0 8px;color:#2C1810}.subtitle{text-align:center;color:#666;font-size:14px;margin-bottom:30px}.cert-row{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:1100px;margin:0 auto}.cert-box{border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08)}.cert-header{padding:18px 22px;color:#FFF;font-family:Georgia,serif;font-size:17px;font-weight:600}.cert-header.cils{background:linear-gradient(135deg,#003D7A,#0055B3)}.cert-header.celi{background:linear-gradient(135deg,#7A0000,#B3002D)}.cert-body{padding:16px;background:#FFF}.level-card{margin-bottom:10px}.lv-header{font-weight:600;font-size:14px;color:#2C1810;padding:6px 0;border-bottom:1px solid #F0EAE4;margin-bottom:6px}.lv-body{display:flex;flex-wrap:wrap;gap:4px}.set-btn{display:inline-block;padding:4px 12px;border-radius:14px;font-size:12px;text-decoration:none;color:#FFF;transition:opacity 0.15s}.cert-header.cils~.cert-body .set-btn{background:#0055B3}.cert-header.celi~.cert-body .set-btn{background:#B3002D}.set-btn:hover{opacity:0.8}@media(max-width:700px){.cert-row{grid-template-columns:1fr}}</style></head><body><div class="top-band"></div><div class="container"><h1>Italiano Esami</h1><p class="subtitle">60 simulazioni complete &middot; A1 &rarr; C2 &middot; 5 set per livello</p><div class="cert-row">'
    
    for cert, color in [("CILS", "cils"), ("CELI", "celi")]:
        html += f'<div class="cert-box"><div class="cert-header {color}">{cert} - Esami completi</div><div class="cert-body">'
        for lv in LEVELS:
            html += f'<div class="level-card"><div class="lv-header">{lv} - {LV_NAMES[lv]}</div><div class="lv-body">'
            for s in range(1, 6):
                html += f'<a href="{cert}/{lv}/Set_{s}/{cert}_{lv}_Set_{s}.html" class="set-btn">Set {s}</a>'
            html += '</div></div>'
        html += '</div></div>'
    
    html += '</div></div></body></html>'
    
    with open(os.path.join(REPO, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("Nav generated")

if __name__ == "__main__":
    print("=== Step 1: Generate Nav ===")
    gen_nav()
    
    print("\n=== Step 2: Generate 60 HTML pages ===")
    gen_html()
    
    print("\n=== Step 3: Generate 300 Audio files ===")
    asyncio.run(gen_audio())
    
    print("\n=== Step 4: Push to GitHub ===")
    push_all()
    
    print("\n=== ALL DONE ===")
