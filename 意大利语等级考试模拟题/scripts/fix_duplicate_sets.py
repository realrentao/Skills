#!/usr/bin/env python3
"""
Fix: Add 10 more ascolto items to each level (except CILS A1 which already has 25).
Current: Only 15 items per level -> only 3 unique sets out of 5.
Fix: Add 10 items -> 25 items -> 5 unique sets.
Then regenerate HTML + audio + push.
"""
import os, sys, base64, asyncio, edge_tts, json, urllib.request, time, re
sys.path.insert(0, r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami")
import cils_data, celi_data

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"
LEVELS = ["A1","A2","B1","B2","C1","C2"]
TOKEN = '${GITHUB_TOKEN}'

# ── Extra ascolto items to add ──
# Each has: (question, "opt1|opt2|opt3|opt4", answer_index, "script_text")

EXTRA_CILS = {
    "A2": [
        ("Come stai oggi?","Bene grazie|Non molto bene|Così così|Male",0,"Oggi sto bene grazie, sono contento di vederti."),
        ("Cosa fai di bello?","Niente di speciale|Lavoro|Studio|Esco",0,"Niente di speciale, solo una passeggiata al parco."),
        ("Dove pranzi di solito?","A casa|In mensa|Al ristorante|Al bar",1,"Di solito pranzo alla mensa dell universita."),
        ("Che macchina hai?","Fiat|BMW|Audi|Mercedes",0,"Ho una Fiat Panda del 2018."),
        ("Quanto tempo ci vuole?","10 minuti|20 minuti|30 minuti|Un ora",2,"Ci vogliono circa trenta minuti a piedi."),
        ("Cosa metti nella valigia?","Vestiti|Libri|Scarpe|Regali",0,"Metto i vestiti e il necessario per la settimana."),
        ("Hai animali domestici?","Un gatto|Un cane|Un pesce|Nessuno",1,"Ho un cane di nome Rocky molto affettuoso."),
        ("Ti piace cucinare?","Si molto|No per niente|A volte|Non so",0,"Mi piace cucinare soprattutto la pasta fatta in casa."),
        ("Dove fai la spesa?","Al supermercato|Dal fruttivendolo|Al mercato|Online",0,"Faccio la spesa al supermercato vicino casa."),
        ("Che musica ascolti?","Pop|Rock|Classica|Jazz",0,"Ascolto musica pop italiana come De Gregori."),
    ],
    "B1": [
        ("Cosa dicono i sondaggi?","Aumento fiducia|Calo consensi|Stabili|Non rilevano",0,"Sondaggi mostrano aumento fiducia nel governo."),
        ("Quale scoperta scientifica?","Nuovo vaccino|Nuovo farmaco|Nuova terapia|Nuovo esame",0,"Scoperto nuovo vaccino contro il raffreddore comune."),
        ("Cosa prevede la legge?","Più tutele|Meno tasse|Più diritti|Meno burocrazia",0,"La legge prevede più tutele per i lavoratori precari."),
        ("Quale evento si avvicina?","Elezioni|Referendum|Votazioni|Parlamento",0,"Si avvicinano le elezioni amministrative di maggio."),
        ("Cosa segnalano medici?","Aumento casi|Diminuzione|Stabili|Sotto controllo",0,"Medici segnalano aumento casi di allergie stagionali."),
        ("Novità nel trasporto?","Nuova linea metro|Nuovo tram|Nuovo bus|Nuova ferrovia",0,"Nuova linea metropolitana colleghera periferia e centro."),
        ("Cosa apre in città?","Museo|Teatro|Biblioteca|Centro culturale",0,"Apre nuovo museo di arte contemporanea in centro."),
        ("Quale campagna parte?","Sensibilizzazione|Raccolta fondi|Volontariato|Donazioni",0,"Parte campagna di sensibilizzazione contro lo spreco alimentare."),
        ("Cosa lancia l appello?","Aiutare i poveri|Salvare l ambiente|Educare i giovani|Curare i malati",1,"Appello di ambientalisti per salvare le foreste italiane."),
        ("Cosa chiedono sindacati?","Aumento salari|Riduzione orari|Più ferie|Meno precariato",0,"Sindacati chiedono aumento salari del 5%."),
    ],
    "B2": [
        ("Cosa analizza il rapporto?","Mercato immobiliare|Mercato azionario|Mercato del lavoro|Mercato energetico",0,"Rapporto sul mercato immobiliare prezzi in calo del 10%."),
        ("Quale decisione UE?","Nuova direttiva|Nuovo regolamento|Nuovo trattato|Nuova sanzione",0,"Ue approva nuova direttiva sulla sostenibilità aziendale."),
        ("Cosa emerge dall indagine?","Frodi fiscali|Evasione contributi|Riciclaggio|Corruzione",0,"Indagine svela frodi fiscali per 2 miliardi di euro."),
        ("Quale progetto parte?","Infrastrutture|Digitale|Sanitario|Scolastico",1,"Parte progetto digitale per portare banda larga in tutto il paese."),
        ("Cosa preoccupa esperti?","Crisi climatica|Perdita biodiversità|Inquinamento|Esaurimento risorse",1,"Esperti preoccupati per perdita biodiversità nei mari."),
        ("Quale vertice si tiene?","G20|G7|ONU|NATO",0,"Vertice G20 a Roma sui temi dell economia globale."),
        ("Nuova tecnologia?","Realtà aumentata|Intelligenza artificiale|Blockchain|IoT",1,"Nuova tecnologia AI per diagnosi mediche precoci."),
        ("Cosa prevede la manovra?","Tagli spesa|Nuove tasse|Investimenti|Risparmi",0,"Manovra economica prevede tagli alla spesa pubblica."),
        ("Quale riforma parte?","Riforma fisco|Riforma burocrazia|Riforma giustizia|Riforma sanità",1,"Parte riforma della burocrazia per semplificare procedure."),
        ("Cosa dicono analisti?","Crescita PIL|Recessione|Stagnazione|Ripresa",0,"Analisti prevedono crescita del PIL dello 0.8%."),
    ],
    "C1": [
        ("Seminario letteratura?","Manierismo|Barocco|Rinascimento|Neoclassicismo",2,"Seminario sul Rinascimento letterario italiano autori minori."),
        ("Relatore sostiene?","Canone letterario|Anticanone|Decostruzione|Filologia",0,"Relatore sostiene necessità di ripensare canone letterario."),
        ("Cosa analizza la ricerca?","Paleografia|Archivistica|Diplomatica|Filologia",0,"Ricerca paleografica su nuovi manoscritti medievali."),
        ("Convegno sociologia?","Società algoritmica|Società digitale|Società informazionale|Società della conoscenza",0,"Società algoritmica decisioni automatizzate e controllo sociale."),
        ("Tesi sostenuta?","Autonomia tecnologia|Neutralità tecnologia|Determinismo|Costruttivismo",3,"Tecnologia non neutrale incorpora valori e interessi."),
        ("Dibattito filosofia?","Libero arbitrio|Compatibilismo|Determinismo|Indeterminismo",0,"Dibattito sul libero arbitrio nelle neuroscienze contemporanee."),
        ("Conferenza economia?","Economia comportamentale|Economia classica|Economia marxista|Economia austriaca",0,"Economia comportamentale critica razionalità dell homo oeconomicus."),
        ("Cosa emerge?","Bias cognitivi|Euristiche|Anomalie|Paradossi",0,"Bias cognitivi influenzano scelte economiche."),
        ("Ruolo cultura?","Soft power|Hard power|Smart power|Sharp power",0,"Cultura come soft power nelle relazioni internazionali."),
        ("Esempio citato?","Italia|Francia|Regno Unito|Germania",0,"Italia esempio di diplomazia culturale nel mediterraneo."),
    ],
    "C2": [
        ("Ontologia?","Heidegger|Husserl|Sartre|Merleau-Ponty",0,"Heidegger ontologia dell esserci e differenza ontologica."),
        ("Filosofia linguaggio?","Wittgenstein primo|Wittgenstein secondo|Frege|Russell",1,"Wittgenstein secondo giochi linguistici e forme di vita."),
        ("Etica contemporanea?","Neo-aristotelismo|Kantismo|Utilitarismo|Contrattualismo",0,"Neo-aristotelismo fioritura umana e virtù."),
        ("Teoria politica?","Post-colonialismo|Decolonialità|Subalternità|Europa-centricità",0,"Teoria post-coloniale critica eurocentrismo sapere."),
        ("Spivak?","Subalterno|Canone|Differenza|Voce",0,"Spivak subalterno non può parlare doppia violenza epistemica."),
        ("Critica femminismo?","Intersezionalità|Differenza|Uguaglianza|Parità",0,"Intersezionalità Crenshaw sovrapposizione discriminazioni."),
        ("Saggio architettura?","Architettura liquida|Decostruttivismo|High-tech|Bio-architettura",0,"Architettura liquida Zaha Hadid forme fluide digitali."),
        ("Biologia filosofia?","Vita nuda|Potere vita|Antropocene|Capitallocene",0,"Vita nuda Agamben inclusione esclusione politica."),
        ("Società moderna?","Società del controllo|Società panottico|Società rete|Società piattaforma",0,"Società del controllo Deleuze sorveglianza diffusa."),
        ("Estetica musica?","Dodecafonia|Atonalità|Serialismo|Post-serialismo",0,"Dodecafonia Schoenberg crisi sistema tonale classico."),
    ],
}

EXTRA_CELI = {
    "A1": [
        ("Di dove sei signore?","Di Milano|Di Roma|Di Napoli|Di Firenze",1,"Sono di Roma ma vivo a Milano per lavoro."),
        ("Hai fratelli o sorelle?","Una sorella|Un fratello|Due fratelli|Sono figlio unico",3,"Sono figlio unico purtroppo non ho fratelli."),
        ("Esci stasera?","Si esco|No sto a casa|Non lo so|Forse",1,"No stasera resto a casa sono molto stanco."),
        ("Che programmi hai?","Vado al cinema|Vado a teatro|Vado a cena|Vado in palestra",2,"Stasera vado a cena con alcuni colleghi di lavoro."),
        ("Ti piace viaggiare?","Si moltissimo|Abbastanza|Non tanto|Per niente",0,"Mi piace moltissimo viaggiare ho visitato 20 paesi."),
        ("Dove sei nato?","In Italia|In Francia|In Spagna|In Germania",0,"Sono nato in Italia a Verona."),
        ("Che ora fai di solito?","Mi alzo alle 7|Mi alzo alle 8|Mi alzo alle 6|Mi alzo alle 9",0,"Mi alzo alle 7 per andare al lavoro."),
        ("Cosa fai stasera?","Leggo un libro|Guardo un film|Ascolto musica|Vado a dormire",1,"Stasera guardo un film al cinema con gli amici."),
        ("Dove hai comprato la borsa?","In centro|Al mercato|Online|In boutique",2,"Ho comprato questa borsa online in saldo."),
        ("Hai già mangiato?","Si ho mangiato|No non ancora|Tra poco|Non ho fame",1,"No non ho ancora mangiato ceniamo insieme?"),
    ],
    "A2": [
        ("Cosa hai sognato?","Un viaggio|Un volo|Un incontro|Un ricordo",1,"Ho sognato di volare sopra la mia città."),
        ("Cosa bolle in pentola?","Minestrone|Pasta|Carne|Pesce",0,"Sto preparando un buon minestrone di verdure."),
        ("Che regalo hai ricevuto?","Un libro|Un profumo|Una sciarpa|Un orologio",3,"Ho ricevuto un bellissimo orologio per il compleanno."),
        ("Cosa fai domani?","Vado in ufficio|Faccio sport|Riposo|Studio",0,"Domani vado in ufficio come sempre."),
        ("Che penna preferisci?","Blu|Nera|Rossa|Verde",0,"Preferisco la penna blu per scrivere meglio."),
        ("Dove hai messo le chiavi?","Sul tavolo|In borsa|In tasca|Appese",0,"Le chiavi sono sul tavolo della cucina."),
        ("Quanto zucchero vuoi?","Un cucchiaino|Due cucchiaini|Niente|Poco",0,"Un cucchiaino di zucchero grazie."),
        ("Cosa guardi in TV?","Telegiornale|Film|Sport|Documentario",0,"Guardo il telegiornale delle 20."),
        ("Che scarpe hai comprato?","Da ginnastica|Da sera|Da lavoro|Da trekking",0,"Ho comprato scarpe da ginnastica nuove."),
        ("Dove hai messo il libro?","Nella libreria|Nello zaino|Sulla scrivania|Nel cassetto",2,"Il libro e sulla scrivania dello studio."),
    ],
    "B1": [
        ("Quali dati diffonde Istat?","Occupazione|Inflazione|PIL|Natalità",0,"Istat diffonde dati positivi occupazione in crescita."),
        ("Nuova scoperta archeologica?","Foro romano|Domus aurea|Terme caracalla|Colosseo",1,"Scoperta nuova sala Domus Aurea con affreschi intatti."),
        ("Borse europee?","In rialzo|In calo|Stabili|Miste",0,"Borse europee in rialzo dopo accordo commerciale."),
        ("Sciopero mezzi?","Treni|Aerei|Autobus|Traghetti",0,"Sciopero treni previsto per sabato 15 ore."),
        ("Partita di calcio?","Vinta|Pareggiata|Perse|Rinviata",0,"Squadra italiana vinta partita 2-0."),
        ("Nuovo record?","Velocità|Altezza|Lunghezza|Tempo",0,"Atleta italiano stabilito nuovo record mondiale."),
        ("Maltempo dove?","Nord|Centro|Sud|Isole",1,"Maltempo centro Italia allerta arancione per pioggia."),
        ("Cosa annuncia premier?","Misure lavoro|Misure fisco|Misure sanità|Misure istruzione",0,"Premier annuncia nuove misure per il lavoro."),
        ("Iniziativa sociale?","Banco alimentare|Caritas|Casa famiglia|Centro accoglienza",0,"Banco alimentare distribuisce cibo a 500 famiglie."),
        ("Celebrazione?","Festa nazionale|Ricorrenza|Anniversario|Cerimonia",0,"Celebrazioni per Anniversario della Repubblica."),
    ],
    "B2": [
        ("Cosa analizza Moody's?","Rating Italia|Rating banche|Rating regioni|Rating imprese",0,"Moody s conferma rating Italia outlook stabile."),
        ("Olimpiadi preparazione?","Impianti sportivi|Villaggio olimpico|Trasporti|Sicurezza",0,"Preparazione olimpiadi nuovi impianti quasi pronti."),
        ("Operazione antimafia?","Sequestri beni|Arresti|Confische|Intercettazioni",1,"Operazione antimafia arresti 25 persone."),
        ("Trovato quadro rubato?","Caravaggio|Leonardo|Raffaello|Tiziano",0,"Trovato Caravaggio rubato museo di Palermo."),
        ("Innovazione start up?","Intelligenza artificiale|Robot|Droni|App",0,"Startup italiana sviluppa AI per diagnosi tumori."),
        ("Scienziati avvertono?","Riscaldamento globale|Buco ozono|Siccita|Alluvioni",0,"Scienziati avvertono riscaldamento globale accelerato."),
        ("Movimento artistico?","Arte povera|Transavanguardia|Futurismo|Metafisica",0,"Arte povera italiani all asta di New York."),
        ("Crisi automobile?","Vendite calo|Produzione ferma|Esportazioni giù|Licenziamenti",0,"Crisi auto vendite calate del 15% in Europa."),
        ("Nuova legge?","Cyberbullismo|Revenge porn|Privacy|Copyright",0,"Nuova legge contro il cyberbullismo nelle scuole."),
        ("Esposizione mondiale?","Expo 2030|Olimpiadi|Mondiali|Conferenza",0,"Expo 2030 Roma presentato progetto ufficiale."),
    ],
    "C1": [
        ("Conferenza filosofia?","Filosofia analitica|Continentalismo|Hermeneutica|Decostruzione",0,"Filosofia analitica mente e significato Frege e Russell."),
        ("Saggio politico?","Democrazia radicale|Post-democrazia|Contro-democrazia|Iper-democrazia",1,"Post-democrazia Crouch democrazia senza cittadini."),
        ("Critica economia?","Neoliberismo|Keynesismo|Monetarismo|Supply-side",0,"Critica neoliberismo Stiglitz disuguaglianza crescente."),
        ("Antropologia culturale?","Relativismo|Universalismo|Particolarismo|Essenzialismo",0,"Relativismo culturale differenze valori tra società."),
        ("Geopolitica?","Grande gioco|Nuova via seta|Indo-pacifico|Transatlantico",1,"Nuova via della seta cinese influenza eurasiatica."),
        ("Filosofia scienza?","Kuhn|Popper|Feyerabend|Lakatos",0,"Kuhn paradigmi scientifici rivoluzioni e cambiamento."),
        ("Genere letterario?","Autofiction|Biografia|Memoir|Saggio",0,"Autofiction genere ibrido tra autobiografia e romanzo."),
        ("Critica sociologia?","Classi sociali|Ceti medi|Elite|Masse",0,"Trasformazione classi sociali società post-industriale."),
        ("Etica applicata?","Animali AI|Robot diritti|Post-umanesimo|Trans-umanesimo",0,"Etica animali e intelligenza artificiale diritti robot."),
        ("Nuovo pensiero?","Accelerazionismo|Post-operaismo|Cognitariato|Precariato",0,"Accelerazionismo sinistra superare capitalismo tecnologia."),
    ],
    "C2": [
        ("Ermeneutica?","Ricoeur|Gadamer|Schleiermacher|Dilthey",0,"Ricoeur ermeneutica testo azione e narrazione identità."),
        ("Saggio sociologia?","Modernità radicalizzata|Seconda modernità|Modernità riflessiva|Tarda modernità",2,"Modernità riflessiva Beck individualizzazione e rischio."),
        ("Critica psicoanalisi?","Inconscio politico|Desiderio|Godimento|Sintomo",0,"Inconscio politico Jameson testi come allegoria sociale."),
        ("Nuovo materialismo?","Ontologia piatta|Vitalismo|Agentività|Assemblaggio",0,"Nuovo materialismo Barad agentività della materia."),
        ("Filosofia differenza?","Deleuze|Bergson|Nietzsche|Heidegger",0,"Deleuze differenza ripetizione ontologia del molteplice."),
        ("Studi culturali?","Subculture|Controculture|Tribù urbane|Scene musicali",0,"Subculture Hebdige stili giovanili resistenza simbolica."),
        ("Saggio mediologia?","Ecologia media|Ambiente mediale|Rimediazione|Immediatezza",0,"Ecologia dei media Fuller ambiente mediale interconnesso."),
        ("Diritto filosofia?","Nomadismo giuridico|Pluralismo|Monismo|Cosmopolitismo",0,"Nomadismo giuridico Braidotti migrazioni identità fluide."),
        ("Teoria cinema?","Dispositivo|Sguardo|Identificazione|Spettatore",0,"Dispositivo cinematografico Baudry soggetto trascendentale."),
        ("Critica tecnologia?","Fenomenologia tecnologia|Post-fenomenologia|Media-ecologia|Cyber-cultura",0,"Post-fenomenologia Ihde tecnologia media percezione mondo."),
    ],
}

def add_extra():
    """Add extra items to levels that have less than 25"""
    for lv, items in EXTRA_CILS.items():
        cils_data.CILS[lv]["ascolto"].extend(items)
    for lv, items in EXTRA_CELI.items():
        celi_data.CELI[lv]["ascolto"].extend(items)
    print("Extra ascolto items added")

# ── Reuse CSS/JS from gen_independent ──
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
#resultTable td{padding:8px 12px;border-bottom:1px solid #F0EAE4}
.score-grade{padding:8px 12px;border-radius:6px;font-weight:500;display:inline-block}"""

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
else if(tp==='grammar'){var inp=q.querySelector('input[type="text"]'),ut=inp?inp.value.trim():'',kwlist=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w});var ans=q.getAttribute('data-answer')||kwlist[0]||'';var sc=kws(ut,kwlist);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Corretto':'Parziale')+' ('+sc+'/'+pt+')<br><span style="font-size:12px;color:#009246;">Risposta corretta: '+ans+'</span>'}
else if(tp==='scrittura'||tp==='orale'){var ta=q.querySelector('textarea'),ut=ta?ta.value.trim():'',kwlist=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ref=q.getAttribute('data-reference')||'';var base=kws(ut,kwlist),bonus=Math.min(5,Math.floor(wc(ut)/10)),sc=Math.min(pt,base+bonus);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Buono':'Da migliorare')+' ('+sc+'/'+pt+')'+(ref?'<br><span style="font-size:12px;color:#0077b6;">Risposta di riferimento: '+ref+'</span>':'')}});D.push({name:s.querySelector('h2').textContent.replace(/<span.*/,'').trim(),score:t,max:m})});
var p=Math.round((T/M)*100);document.getElementById('totalScore').textContent=T+'/'+M;var msg=document.getElementById('scoreMessage');
if(p>=85)msg.innerHTML='<span class="score-grade" style="background:#E8F5E9;color:#009246;">Eccellente!</span>';else if(p>=70)msg.innerHTML='<span class="score-grade" style="background:#E3F2FD;color:#1565C0;">Buono!</span>';else if(p>=55)msg.innerHTML='<span class="score-grade" style="background:#FFF8E1;color:#B8860B;">Discreto</span>';else if(p>=40)msg.innerHTML='<span class="score-grade" style="background:#FBE9E7;color:#E65100;">Insufficiente</span>';else msg.innerHTML='<span class="score-grade" style="background:#FFEBEE;color:#CE2B37;">Grave</span>';
var rf=document.getElementById('answerReference');if(rf){rf.style.display='block';var tb=document.getElementById('resultBody');if(tb){tb.innerHTML='';D.forEach(function(d){tb.innerHTML+='<tr><td>'+d.name+'</td><td>'+d.score+'</td><td>'+d.max+'</td></tr>'})}}window.scrollTo({top:0,behavior:'smooth'})}
function reset(){document.querySelectorAll('input[type="radio"]').forEach(function(r){r.checked=false});document.querySelectorAll('input[type="text"]').forEach(function(t){t.value=''});document.querySelectorAll('textarea').forEach(function(t){t.value=''});document.querySelectorAll('.feedback').forEach(function(f){f.className='feedback';f.innerHTML=''});document.querySelectorAll('.script-text').forEach(function(s){s.style.display='none'});document.querySelectorAll('.script-btn').forEach(function(b){b.textContent='Testo'});document.getElementById('totalScore').textContent='0/100';document.getElementById('scoreMessage').innerHTML='';var rf=document.getElementById('answerReference');if(rf)rf.style.display='none';window.scrollTo({top:0,behavior:'smooth'})}"""

LV_NAMES = {"A1":"Base","A2":"Elementare","B1":"Intermedio","B2":"Intermedio-Avanzato","C1":"Avanzato","C2":"Padronanza"}

REFERENCES = {
    "CILS": {
        "scrittura": {"A1":["Mi chiamo Marco, ho 22 anni e vengo dall'Italia. Studio lingue all'universit\u00e0. Mi piace leggere e viaggiare.","La mia giornata tipica: mi sveglio alle 7, faccio colazione con cappuccino e cornetto, poi vado all'universit\u00e0. Pranzo alle 13 e studio al pomeriggio. La sera ceno e guardo la TV.","Ieri sono andato al cinema con gli amici. Abbiamo visto un film divertente e poi siamo andati a cena in pizzeria. \u00c8 stata una bella giornata.","La mia famiglia \u00e8 composta da 4 persone: mio padre, mia madre, mio fratello e io. Abitiamo in una casa con giardino in periferia.","La mia citt\u00e0 \u00e8 Roma, una citt\u00e0 bellissima piena di storia. Ci sono molti musei e monumenti famosi come il Colosseo. Mi piace molto passeggiare per il centro."],"A2":["Sabato sono andato al mare con gli amici. Abbiamo fatto il bagno e preso il sole. La domenica sono rimasto a casa a riposare. \u00c8 stato un bel fine settimana.","L'anno scorso sono andato a Parigi con la mia famiglia. Abbiamo visitato la Tour Eiffel, il Louvre e Montmartre. \u00c8 stato un viaggio bellissimo, ho visto tantissime cose interessanti.","Quest'anno ho studiato molto all'universit\u00e0. Ho dato 5 esami e li ho passati tutti. I professori sono stati bravi e ho imparato molte cose nuove.","Ciao amico mio, sabato prossimo far\u00f2 una festa a casa mia. Inizier\u00e0 alle 20. Porta qualcosa da mangiare o da bere. Ti aspetto!","Recentemente ho visto il film 'La vita \u00e8 bella'. \u00c8 un film italiano molto commovente. La storia parla di un padre che protegge suo figlio durante la guerra. Mi \u00e8 piaciuto molto."],"B1":["Gentile Responsabile, mi candido per la posizione di assistente amministrativo. Ho esperienza nel settore e buone competenze informatiche. Sono disponibile per un colloquio. Cordiali saluti.","Imparare le lingue \u00e8 molto importante perch\u00e9 offre opportunit\u00e0 di lavoro all'estero e permette di conoscere nuove culture. Personalmente, studiare l'italiano mi ha aperto molte porte.","Il mio viaggio pi\u00f9 bello \u00e8 stato in Giappone. Ho visitato Tokyo e Kyoto, ho incontrato persone meravigliose e ho assaggiato cibi deliziosi. \u00c8 stata un'esperienza indimenticabile.","Ho cenato al Ristorante Da Mario. Il servizio \u00e8 stato eccellente e la qualit\u00e0 dei piatti ottima. Consiglio vivamente la pasta alla carbonara. Il rapporto qualit\u00e0-prezzo \u00e8 buono.","Tra dieci anni mi vedo con un buon lavoro, una famiglia e una casa mia. Spero di aver viaggiato molto e di essere realizzato professionalmente e personalmente."],"B2":["Il cambiamento climatico \u00e8 una delle sfide pi\u00f9 urgenti del nostro tempo. \u00c8 necessario agire subito per ridurre le emissioni e proteggere l'ambiente. Ogni individuo ha la responsabilit\u00e0 di fare la propria parte per un futuro sostenibile.","La globalizzazione ha portato benefici economici e opportunit\u00e0 culturali, ma ha anche creato disuguaglianze e omologazione. \u00c8 importante trovare un equilibrio tra apertura internazionale e tutela delle identit\u00e0 locali.","La settimana scorsa ho partecipato a una mostra d'arte contemporanea molto interessante. Le opere esposte erano innovative e stimolanti. L'evento era ben organizzato e il pubblico numeroso.","L'intelligenza artificiale sta rivoluzionando il mondo del lavoro. Alcuni lavori scompariranno ma ne nasceranno di nuovi. \u00c8 fondamentale investire nella formazione per prepararsi a questo cambiamento.","Egregio Sindaco, le scrivo per segnalare il problema del traffico nel mio quartiere. Chiedo l'installazione di dossi rallentatori e pi\u00f9 controlli. Una soluzione potrebbe essere la creazione di zone pedonali."],"C1":["Il rapporto tra etica e tecnologia \u00e8 complesso: l'innovazione tecnologica offre possibilit\u00e0 straordinarie ma solleva anche questioni etiche profonde. \u00c8 necessario stabilire limiti chiari per garantire che la tecnologia serva l'umanit\u00e0 e non la danneggi.","La post-verit\u00e0 rappresenta una sfida per la comunicazione contemporanea. Nell'era dei social media, l'informazione \u00e8 spesso manipolata e la verit\u00e0 diventa relativa. I media hanno la responsabilit\u00e0 di garantire informazioni accurate.","I cambiamenti climatici richiedono politiche ambientali coraggiose a livello globale. Il futuro del pianeta dipende dalle nostre scelte di oggi. \u00c8 urgente ridurre le emissioni e investire nelle energie rinnovabili.","La cultura nell'era globale deve bilanciare identit\u00e0 locale e dialogo interculturale. La diversit\u00e0 culturale \u00e8 una ricchezza che va preservata, mentre il dialogo tra culture diverse promuove comprensione e pace.","Il rapporto tra individuo e collettivit\u00e0 \u00e8 in continua evoluzione. La societ\u00e0 contemporanea oscilla tra la valorizzazione dell'individuo e la necessit\u00e0 di solidariet\u00e0 collettiva. Trovare un equilibrio \u00e8 fondamentale."],"C2":["Il concetto di verit\u00e0 nell'era della post-verit\u00e0 \u00e8 problematico. La conoscenza \u00e8 frammentata e l'interpretazione dei fatti \u00e8 spesso influenzata da interessi particolari. \u00c8 necessario recuperare un'etica della verit\u00e0 basata sul dialogo e sulla trasparenza.","Il potere e il sapere sono strettamente intrecciati nella societ\u00e0 contemporanea. Foucault ha mostrato come le istituzioni disciplinari producono conoscenza che a sua volta rafforza il potere. Oggi questo rapporto si manifesta nelle tecnologie di sorveglianza.","La crisi della rappresentanza politica \u00e8 evidente nel calo della partecipazione elettorale e nella sfiducia dei cittadini verso le istituzioni. La democrazia ha bisogno di nuovi spazi di partecipazione e di un rinnovamento delle elite politiche.","L'arte nella societ\u00e0 dello spettacolo rischia di diventare puro intrattenimento. Tuttavia, l'arte contemporanea conserva una funzione critica fondamentale, capace di interrogare la realt\u00e0 e proporre nuove prospettive di senso.","Il populismo \u00e8 un fenomeno complesso che va analizzato storicamente e politicamente. Nasce dalla crisi della rappresentanza e dalla disillusione verso le elite tradizionali, ma rischia di minare le istituzioni democratiche."]},
        "orale": {"A1":["Mi chiamo Luca, ho 25 anni e vengo dalla Sicilia. Vivo a Bologna dove studio ingegneria. Mi piace la musica italiana.","La mia routine: mi alzo alle 7, faccio colazione, vado all'universit\u00e0 o al lavoro. La sera ceno e guardo film.","La mia casa ha tre stanze: un salotto, una camera da letto e una cucina. \u00c8 piccola ma accogliente. C'\u00e8 anche un balcone.","Nel tempo libero mi piace leggere libri, andare al cinema e fare sport. Ogni settimana gioco a calcio con gli amici.","Sabato sono uscito con gli amici. Siamo andati al ristorante e poi al cinema. Ho visto un film molto divertente."],"A2":["Recentemente ho visitato Firenze con la mia ragazza. Abbiamo visto il Duomo e Ponte Vecchio. \u00c8 stata un'esperienza molto interessante e romantica.","La mia citt\u00e0 preferita \u00e8 Venezia perch\u00e9 \u00e8 unica al mondo. I canali, le gondole e Piazza San Marco la rendono speciale. Ogni visita \u00e8 magica.","Il mio progetto per il futuro \u00e8 trovare un buon lavoro e magari trasferirmi all'estero per qualche anno. Spero di realizzare questo sogno presto.","La persona pi\u00f9 importante per me \u00e8 mia madre. Mi ha sempre sostenuto e aiutato in ogni momento. \u00c8 una persona forte e generosa.","Di solito nel fine settimana mi rilasso: dormo fino a tardi, esco con gli amici, vado al cinema o faccio sport. La domenica ceno con la famiglia."],"B1":["Vivere in una grande citt\u00e0 offre molti vantaggi come trasporti efficienti, offerta culturale e opportunit\u00e0 di lavoro. Tuttavia, ci sono anche svantaggi come il costo della vita elevato, l'inquinamento e lo stress quotidiano.","I social media hanno rivoluzionato la comunicazione, permettendo di restare in contatto con persone lontane. Tuttavia, un uso eccessivo pu\u00f2 causare dipendenza e isolamento sociale. \u00c8 importante usarli con moderazione.","Il libro che mi ha colpito di pi\u00f9 \u00e8 'Il nome della rosa' di Umberto Eco. La trama \u00e8 avvincente, i personaggi sono ben sviluppati e lo stile \u00e8 affascinante. Lo consiglio a tutti gli amanti della letteratura.","La tutela dell'ambiente \u00e8 fondamentale per il nostro futuro. Dobbiamo ridurre l'inquinamento, riciclare i rifiuti e proteggere la biodiversit\u00e0. Ogni piccolo gesto quotidiano pu\u00f2 fare la differenza.","L'immigrazione in Italia \u00e8 un fenomeno complesso. Da un lato, l'integrazione \u00e8 necessaria per una societ\u00e0 multiculturale; dall'altro, ci sono sfide legate al lavoro e all'accoglienza. Serve equilibrio."],"B2":["I social media influenzano la democrazia in modi contraddittori: da un lato facilitano la partecipazione e la diffusione delle informazioni, dall'altro favoriscono la disinformazione e la polarizzazione. \u00c8 fondamentale educare all'uso critico dei media.","La tecnologia sta trasformando il mercato del lavoro. L'automazione elimina alcuni lavori ma ne crea di nuovi. La formazione continua \u00e8 essenziale per adattarsi a questi cambiamenti e acquisire nuove competenze.","Il turismo di massa ha effetti negativi sull'ambiente e sulle comunit\u00e0 locali. L'overtourism danneggia gli ecosistemi e la qualit\u00e0 della vita. Serve un turismo sostenibile che rispetti i territori e le culture.","L'integrazione europea ha portato pace e prosperit\u00e0, ma oggi affronta sfide come la crisi migratoria e il ritorno dei sovranismi. La solidariet\u00e0 tra stati membri \u00e8 essenziale per superare queste difficolt\u00e0.","L'universit\u00e0 ha un ruolo fondamentale nella societ\u00e0: forma i professionisti di domani, promuove la ricerca e il pensiero critico. Investire nell'istruzione superiore \u00e8 investire nel futuro del paese."],"C1":["La libert\u00e0 nella filosofia politica contemporanea \u00e8 un concetto complesso che spazia dalla libert\u00e0 negativa come non-interferenza alla libert\u00e0 positiva come autodeterminazione. L'autonomia individuale va bilanciata con la responsabilit\u00e0 sociale per una convivenza democratica.","L'intellettuale oggi ha il compito di interpretare criticamente la realt\u00e0, smascherare le ideologie e promuovere un pensiero indipendente. In un'epoca di disinformazione, il ruolo critico dell'intellettuale \u00e8 pi\u00f9 importante che mai.","Il modello di sviluppo attuale basato sulla crescita illimitata non \u00e8 sostenibile. L'economia deve rispettare i limiti del pianeta. La transizione ecologica richiede un cambiamento radicale del nostro modo di produrre e consumare.","La memoria storica \u00e8 fondamentale per costruire l'identit\u00e0 nazionale. Ricordare il passato, anche nelle sue pagine pi\u00f9 oscure, aiuta a comprendere il presente e a progettare un futuro migliore, senza ripetere gli errori.","L'intelligenza artificiale sta ridefinendo i confini della creativit\u00e0 umana. Mentre l'AI pu\u00f2 generare arte e musica, la vera creativit\u00e0 rimane un tratto distintamente umano. La tecnologia deve essere uno strumento, non un sostituto."],"C2":["Il riconoscimento nella filosofia politica contemporanea \u00e8 un tema centrale. Honneth e Taylor sostengono che il riconoscimento dell'identit\u00e0 e delle differenze \u00e8 fondamentale per la giustizia sociale. Senza riconoscimento non c'\u00e8 vera uguaglianza.","Il concetto di progresso va criticato: non tutto ci\u00f2 che \u00e8 nuovo \u00e8 meglio. La modernit\u00e0 ha promesso liberazione ma ha prodotto nuove forme di dominio. Serve una riflessione critica sul significato stesso del progresso.","Nel capitalismo contemporaneo, l'etica sembra subordinata all'economia. La ricerca del profitto a ogni costo genera disuguaglianze e crisi. Un nuovo modello economico deve mettere al centro la giustizia sociale e il bene comune.","La memoria collettiva costruisce l'identit\u00e0 nazionale attraverso la narrazione condivisa del passato. Tuttavia, questa memoria \u00e8 spesso selettiva e strumentalizzata politicamente. \u00c8 necessario un confronto aperto e critico con la storia.","La tensione tra universalismo e particolarismo \u00e8 al centro del dibattito culturale contemporaneo. I diritti universali devono essere conciliati con il rispetto delle differenze culturali in una societ\u00e0 sempre pi\u00f9 globalizzata."]}
    },
    "CELI": {
        "scrittura": {"A1":["Caro amico, mi presento: sono Sara, ho 23 anni e vivo a Milano. Studio architettura e mi piace viaggiare. In questo momento sto imparando l'italiano. Ciao!","La mia stanza \u00e8 color crema con una scrivania vicino alla finestra. C'\u00e8 un letto comodo, una libreria piena di libri e un armadio. Mi piace molto la mia stanza perch\u00e9 \u00e8 luminosa.","Il mio cibo preferito \u00e8 la pizza margherita. \u00c8 buonissima con il formaggio filante e il pomodoro fresco. Di solito la mangio al ristorante con gli amici il sabato sera.","La domenica mi alzo tardi, faccio una bella colazione e poi esco a passeggiare. Pranzo con la famiglia e il pomeriggio leggo o guardo un film. La sera ceno presto.","Il mio migliore amico si chiama Marco. \u00c8 alto, simpatico e gentile. Ci conosciamo da quando avevamo 5 anni. Insieme andiamo spesso al cinema e facciamo sport."],"A2":["Cari mamma e pap\u00e0, sto visitando Firenze e mi sto divertendo moltissimo. La citt\u00e0 \u00e8 bellissima, ho visto il Duomo e Ponte Vecchio. Il tempo \u00e8 bello. Un abbraccio, Maria.","Ieri sera sono andato al ristorante con la mia famiglia. Ho mangiato gli spaghetti alle vongole come primo e una grigliata mista come secondo. Per dolce ho preso un tiramis\u00f9. Ottimo!","Per il mio ultimo compleanno ho ricevuto un bel regalo dai miei amici: una chitarra acustica. Sono stato molto contento perch\u00e9 suonare la chitarra \u00e8 il mio hobby preferito.","Ciao Luca, andiamo al cinema sabato sera? Vorrei vedere il nuovo film di animazione. Ci troviamo alle 20 davanti al cinema. Fammi sapere se puoi. A presto!","L'estate scorsa sono andata in vacanza al mare in Sardegna. L'acqua era limpida e la spiaggia bellissima. Mi sono divertita tantissimo e ho fatto nuove amicizie."],"B1":["Fare volontariato \u00e8 stata un'esperienza meravigliosa. Ho aiutato persone bisognose e ho dedicato il mio tempo agli altri. Mi ha insegnato l'importanza della solidariet\u00e0 e mi ha fatto crescere come persona.","La dieta mediterranea \u00e8 un patrimonio culturale italiano. \u00c8 basata su cibi sani come olio d'oliva, pesce, frutta e verdura. Fa bene alla salute ed \u00e8 riconosciuta come modello alimentare equilibrato.","Una festa tradizionale italiana che conosco \u00e8 il Carnevale di Venezia. Si celebra con maschere e costumi meravigliosi. Le persone si riuniscono in piazza San Marco per festeggiare.","Gentile Professore, voglio ringraziarla per avermi insegnato tanto quest'anno. Le sue lezioni sono state stimolanti e mi hanno fatto crescere culturalmente. La ringrazio per la sua passione e dedizione.","Ho soggiornato al B&B 'Il Girasole' ed \u00e8 stato piacevole. La posizione \u00e8 centrale, la camera pulita e la colazione abbondante. Lo consiglio per un soggiorno economico ma di qualit\u00e0."],"B2":["Lo smart working offre flessibilit\u00e0 e autonomia, permettendo di conciliare lavoro e vita privata. Tuttavia, comporta anche isolamento sociale e difficolt\u00e0 di concentrazione. Un modello ibrido sarebbe la soluzione ideale.","Il patrimonio culturale italiano \u00e8 unico al mondo e va valorizzato attraverso la conservazione dei monumenti, la promozione dell'arte e l'educazione delle nuove generazioni. La cultura \u00e8 la nostra pi\u00f9 grande risorsa.","L'energia nucleare \u00e8 un tema controverso. Da un lato, produce energia pulita senza emissioni di CO2; dall'altro, comporta rischi di incidenti e la gestione delle scorie. La decisione richiede un dibattito informato.","Ho assistito a una conferenza TED sulla creativit\u00e0 molto stimolante. Il relatore ha parlato di come l'innovazione nasca dalla combinazione di idee diverse. L'intervento mi ha ispirato profondamente.","Gentile Direttore, le scrivo per segnalare il problema del rumore nel mio quartiere. Propongo l'installazione di barriere acustiche e maggiori controlli notturni. Una soluzione possibile \u00e8 la creazione di zone silenziose."],"C1":["I social media hanno un impatto profondo sulla democrazia: da un lato facilitano la partecipazione politica e la circolazione delle idee, dall'altro favoriscono la disinformazione e la polarizzazione del dibattito pubblico. \u00c8 necessaria un'educazione critica ai media.","Il turismo sostenibile \u00e8 essenziale per preservare l'ambiente e le comunit\u00e0 locali. Un turismo responsabile riduce l'impatto ecologico, rispetta le culture locali e promuove uno sviluppo economico equilibrato del territorio.","L'universit\u00e0 ha il compito di formare non solo professionisti competenti ma anche cittadini critici. La formazione superiore deve promuovere il pensiero autonomo, la ricerca libera e la consapevolezza sociale per preparare al futuro.","Il patrimonio culturale italiano \u00e8 fondamentale per l'identit\u00e0 nazionale. Preservare e valorizzare questo patrimonio significa proteggere la memoria storica e la tradizione, ma anche innovare per trasmetterlo alle nuove generazioni.","L'innovazione tecnologica sta trasformando il mondo del lavoro, creando nuove professioni e rendendone obsolete altre. La formazione continua e l'adattabilit\u00e0 sono le chiavi per affrontare con successo questa trasformazione."],"C2":["Il concetto di identit\u00e0 nell'era globale \u00e8 caratterizzato dal meticciato culturale. Le identit\u00e0 non sono pi\u00f9 fisse ma ibride, influenzate da flussi migratori e comunicazione globale. Il dialogo tra culture diverse arricchisce e trasforma.","Abbiamo una responsabilit\u00e0 etica verso le generazioni future: le nostre scelte di oggi determineranno il mondo di domani. La sostenibilit\u00e0 ambientale e la giustizia sociale sono imperativi morali per un futuro vivibile.","La crisi della democrazia contemporanea si manifesta nella sfiducia verso le istituzioni e nella caduta della partecipazione. Per rinnovare la democrazia servono nuovi spazi di partecipazione e una maggiore trasparenza decisionale.","La filosofia nella societ\u00e0 tecnologica ha il compito di interrogare il senso dell'umano in un'epoca di macchine intelligenti. L'umanesimo critico pu\u00f2 guidare lo sviluppo tecnologico senza perdere di vista i valori fondamentali.","La memoria storica e la riconciliazione sono processi complementari: ricordare le ingiustizie del passato \u00e8 necessario per costruire un futuro di pace. Senza verit\u00e0 e giustizia non pu\u00f2 esserci vera riconciliazione."]},
        "orale": {"A1":["La mia giornata tipo: mi sveglio alle 7, vado a scuola o al lavoro, pranzo alle 13, studio al pomeriggio e la sera mi rilasso guardando la TV.","La mia famiglia \u00e8 composta da tre persone: mia madre insegnante, mio padre ingegnere e io. Abbiamo un cane di nome Bal\u00f9.","Nel tempo libero mi piace ascoltare musica, fare sport e uscire con gli amici. Il mio sport preferito \u00e8 il nuoto.","Il mio paese \u00e8 piccolo ma accogliente. C'\u00e8 una piazza centrale con una chiesa antica e diversi negozi. La comunit\u00e0 \u00e8 molto unita.","La mia scuola \u00e8 grande e moderna. I professori sono bravi e i compagni simpatici. Studio lingue straniere e informatica."],"A2":["La mia casa ideale sarebbe in campagna con un grande giardino, una cucina spaziosa e tante stanze luminose. Vicino alla natura, silenziosa e tranquilla.","Il mio piatto preferito \u00e8 la pasta alla carbonara. Si prepara con uova, guanciale, pecorino e pepe. \u00c8 semplice ma deliziosa. La cucino spesso per i miei amici.","Quando ero piccolo andavo sempre al mare con i miei genitori. Giocavo sulla spiaggia e facevo castelli di sabbia. \u00c8 un ricordo bellissimo.","La settimana scorsa sono andato in gita al lago. \u00c8 stata una bellissima giornata di sole. Abbiamo fatto un picnic e una passeggiata nel bosco.","Il mio sport preferito \u00e8 il calcio. Gioco in una squadra locale e mi alleno due volte a settimana. La partita la domenica \u00e8 il momento pi\u00f9 bello."],"B1":["Il volontariato \u00e8 importante nella societ\u00e0 perch\u00e9 aiuta le persone in difficolt\u00e0 e crea comunit\u00e0 pi\u00f9 solidali. Dedicare tempo agli altri arricchisce anche chi aiuta.","Conosco diverse tradizioni italiane: il Carnevale con le maschere, la Pasqua con la colomba, il Natale con il presepe. Ogni regione ha le sue usanze particolari.","Il sistema scolastico italiano prevede 5 anni di elementari, 3 di medie e 5 di superiori. Poi c'\u00e8 l'universit\u00e0. Gli esami di maturit\u00e0 sono molto importanti.","Il turismo sostenibile rispetta l'ambiente e le comunit\u00e0 locali. Preferisco viaggiare in modo responsabile, evitando il turismo di massa e scegliendo strutture ecologiche.","Il nord Italia \u00e8 pi\u00f9 industrializzato e ricco, mentre il sud ha un costo della vita pi\u00f9 basso ma meno opportunit\u00e0. Le differenze culturali sono affascinanti."],"B2":["L'intelligenza artificiale sta trasformando la societ\u00e0 in modo profondo. Da un lato offre strumenti potenti per la medicina e la ricerca, dall'altro solleva questioni etiche sul controllo e la privacy. \u00c8 necessario un approccio equilibrato.","Lo sviluppo sostenibile integra crescita economica e rispetto ambientale. La green economy crea nuovi posti di lavoro e promuove l'innovazione. \u00c8 la strada giusta per il futuro del pianeta.","Le migrazioni sono un fenomeno complesso che richiede politiche di accoglienza e integrazione efficaci. L'integrazione passa attraverso il lavoro, l'istruzione e la partecipazione sociale dei migranti.","La donna nella societ\u00e0 contemporanea ha conquistato molti diritti ma persiste una disparit\u00e0 salariale e una sotto-rappresentazione nei ruoli di potere. La parit\u00e0 di genere \u00e8 ancora un obiettivo da raggiungere.","La crisi climatica richiede azioni urgenti a livello globale. Governi, imprese e cittadini devono collaborare per ridurre le emissioni e adottare stili di vita sostenibili. Il tempo per agire \u00e8 ora."],"C1":["La globalizzazione culturale crea un dialogo tra culture diverse ma rischia anche di omologare le identit\u00e0 particolari. Preservare la diversit\u00e0 culturale \u00e8 fondamentale per arricchire l'esperienza umana e promuovere la comprensione reciproca.","Il rapporto tra scienza e politica \u00e8 complesso: la scienza fornisce evidenze, ma la politica deve prendere decisioni considerando anche fattori sociali ed economici. Durante la pandemia, questo rapporto \u00e8 stato messo alla prova.","I diritti umani e l'immigrazione sono temi intrecciati. Ogni persona ha diritto a cercare una vita migliore. L'accoglienza e l'integrazione sono doveri morali oltre che obblighi giuridici internazionali.","L'educazione nell'era digitale deve preparare gli studenti a un mondo in continuo cambiamento. La tecnologia \u00e8 uno strumento potente, ma non deve sostituire il pensiero critico e la relazione educativa.","La sostenibilit\u00e0 e la giustizia sociale sono due facce della stessa medaglia. Non pu\u00f2 esserci vera sostenibilit\u00e0 ambientale senza equit\u00e0 sociale. Le politiche verdi devono tenere conto delle disuguaglianze."],"C2":["L'antropocentrismo va superato per un'etica ambientale che riconosca il valore intrinseco della natura. La crisi ecologica richiede un nuovo paradigma che superi la separazione tra umano e natura.","Il concetto di verit\u00e0 nell'epistemologia contemporanea \u00e8 problematico. Tra realismo scientifico e costruttivismo sociale, la verit\u00e0 appare come un orizzonte regolativo pi\u00f9 che come una corrispondenza oggettiva.","La giustizia distributiva deve affrontare le disuguaglianze globali in modo strutturale. La distribuzione ineguale delle risorse non \u00e8 solo ingiusta ma anche inefficiente per lo sviluppo umano globale.","Il rapporto tra tecnica e destino umano \u00e8 stato analizzato da Heidegger: la tecnica non \u00e8 solo uno strumento ma un modo di disvelamento che pu\u00f2 diventare pericolo se riduce l'essere a pura disponibilit\u00e0.","Il pluralismo culturale e l'universalit\u00e0 dei diritti sono in tensione. I diritti umani devono essere universali ma anche rispettosi delle differenze culturali, in un equilibrio delicato ma necessario."]}
    }
}

def sections_from_data(data, cert, lv, set_n):
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
                q, kws = item[0], item[1]
                ans_val = kws[0] if isinstance(kws, list) and kws else ""
                lines.append(f'  <div class="question" data-type="grammar" data-keywords="{kws}" data-answer="{ans_val}" data-points="{pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <input type="text" placeholder="Scrivi..." autocomplete="off">')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "scrittura":
                q, kws = item[0], item[1]
                refs = REFERENCES.get(cert, {}).get("scrittura", {}).get(lv, [])
                ref = refs[set_n - 1] if refs and (set_n - 1) < len(refs) else ""
                ref_esc = ref.replace("'", "&#39;")
                lines.append(f'  <div class="question" data-type="scrittura" data-keywords="{kws}" data-reference="{ref_esc}" data-points="{max_pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <textarea rows="4" placeholder="Scrivi qui..." autocomplete="off"></textarea>')
                lines.append(f'    <div class="feedback"></div></div>')
            
            elif sec_id == "orale":
                q, kws = item[0], item[1]
                refs = REFERENCES.get(cert, {}).get("orale", {}).get(lv, [])
                ref = refs[set_n - 1] if refs and (set_n - 1) < len(refs) else ""
                ref_esc = ref.replace("'", "&#39;")
                lines.append(f'  <div class="question" data-type="orale" data-keywords="{kws}" data-reference="{ref_esc}" data-points="{max_pts}">')
                lines.append(f'    <div class="question-text">{q}</div>')
                lines.append(f'    <textarea rows="4" placeholder="Rispondi qui..." autocomplete="off"></textarea>')
                lines.append(f'    <div class="feedback"></div></div>')
        
        lines.append('</div>')
    
    return "\n".join(lines)

def gen_html():
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
                count += 1
    print(f"HTML done: {count} pages")

async def gen_audio():
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
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(script + "\n")
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

def gen_nav():
    html = '<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Italiano Esami - Simulazioni CILS e CELI</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:"Lato",sans-serif;background:#FDF8F3;color:#2C1810}.top-band{height:4px;background:linear-gradient(90deg,#009246,#009246 33%,#FFF 33%,#FFF 66%,#CE2B37 66%,#CE2B37 100%)}h1{text-align:center;font-family:Georgia,serif;font-size:28px;margin:20px 0 8px;color:#2C1810}.subtitle{text-align:center;color:#666;font-size:14px;margin-bottom:30px}.cert-row{display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:1100px;margin:0 auto}.cert-box{border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08)}.cert-header{padding:18px 22px;color:#FFF;font-family:Georgia,serif;font-size:17px;font-weight:600}.cert-header.cils{background:linear-gradient(135deg,#003D7A,#0055B3)}.cert-header.celi{background:linear-gradient(135deg,#7A0000,#B3002D)}.cert-body{padding:16px;background:#FFF}.level-card{margin-bottom:10px}.lv-header{font-weight:600;font-size:14px;color:#2C1810;padding:6px 0;border-bottom:1px solid #F0EAE4}.lv-body{display:flex;flex-wrap:wrap;gap:4px}.set-btn{display:inline-block;padding:4px 12px;border-radius:14px;font-size:12px;text-decoration:none;color:#FFF}.cert-header.cils~.cert-body .set-btn{background:#0055B3}.cert-header.celi~.cert-body .set-btn{background:#B3002D}.set-btn:hover{opacity:0.8}@media(max-width:700px){.cert-row{grid-template-columns:1fr}}</style></head><body><div class="top-band"></div><h1>Italiano Esami</h1><p class="subtitle">60 simulazioni complete &middot; A1 &rarr; C2 &middot; 5 set per livello</p><div class="cert-row">'
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

def push_all():
    files = ["index.html"]
    for cert in ["CILS", "CELI"]:
        for lv in LEVELS:
            for s in range(1, 6):
                files.append(f"{cert}/{lv}/Set_{s}/{cert}_{lv}_Set_{s}.html")
            ad = os.path.join(REPO, cert, lv, "audio")
            if os.path.exists(ad):
                for f in sorted(os.listdir(ad)):
                    fp = os.path.join(ad, f)
                    sz = os.path.getsize(fp)
                    if sz < 100 and f.endswith(".txt"): continue
                    if sz < 5000 and f.endswith(".js"): continue
                    files.append(f"{cert}/{lv}/audio/{f}")
    pushed = 0
    for rel in files:
        fp = os.path.join(REPO, *rel.split("/"))
        if not os.path.exists(fp): continue
        url = f"https://api.github.com/repos/realrentao/italiano-esami/contents/{rel}"
        for attempt in range(3):
            sha = None
            try:
                r = urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json"})
                sha = json.loads(urllib.request.urlopen(r, timeout=10).read())["sha"]
            except: pass
            with open(fp, "rb") as f:
                content = base64.b64encode(f.read()).decode()
            data = {"message": "Fix duplicate sets - 25 items per level", "content": content, "branch": "master"}
            if sha: data["sha"] = sha
            r2 = urllib.request.Request(url, method="PUT", data=json.dumps(data).encode(), headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
            try:
                json.loads(urllib.request.urlopen(r2, timeout=30).read())
                pushed += 1
                break
            except urllib.error.HTTPError as e:
                if e.code == 409 and attempt < 2:
                    time.sleep(1); continue
                break
        time.sleep(0.15)
    print(f"Pushed: {pushed}/{len(files)}")

if __name__ == "__main__":
    add_extra()
    gen_nav()
    gen_html()
    print("Generating audio...")
    asyncio.run(gen_audio())
    print("Pushing to GitHub...")
    push_all()
    print("ALL DONE")
