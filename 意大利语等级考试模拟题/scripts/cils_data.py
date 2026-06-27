#!/usr/bin/env python3
"""CILS independent question data - 6 levels x 5 sets, each with unique questions.
Format: {level: {section: [(q, opts|kw, ans, script), ...]}}
Sections: ascolto(5), lettura(2-3), grammatica(3-4), scrittura(1), orale(1)
CILS official: Univ. di Siena - situational dialogues, grammar-focused, practical texts"""

CILS = {}
LEVELS = ["A1","A2","B1","B2","C1","C2"]

for lv in LEVELS:
    CILS[lv] = {"ascolto":[],"lettura":[],"grammatica":[],"scrittura":[],"orale":[]}

# ═══════════════ A1 ═══════════════
CILS["A1"]["ascolto"] = [
    ("Di dove sei?","Italia|Francia|Spagna|Germania",0,"Ciao mi chiamo Marco e vengo da Roma in Italia."),
    ("Quanti anni hai?","18|20|22|25",2,"Ho ventidue anni e studio lingue all universita."),
    ("Che lavoro fai?","Studente|Insegnante|Medico|Avvocato",0,"Sono studente di medicina all Universita di Bologna."),
    ("Dove abiti?","Milano|Roma|Firenze|Napoli",1,"Abito a Roma in via Cavour vicino al Colosseo."),
    ("Che ora e?","8:00|9:00|10:00|11:00",2,"Sono le dieci del mattino. E presto per la pausa pranzo."),
    ("Di che colore e la macchina?","Rosso|Blu|Verde|Giallo",0,"La macchina di Luca e rossa una Fiat 500 nuova."),
    ("Quanto costa il biglietto?","2 euro|3 euro|5 euro|10 euro",1,"Il biglietto dell autobus costa tre euro."),
    ("Dove vai in vacanza?","Mare|Montagna|Citta|Campagna",2,"Quest anno vado in vacanza a Roma per visitare i musei."),
    ("Cosa mangi a colazione?","Cornetto|Pizza|Pasta|Insalata",0,"La mattina mangio un cornetto con il cappuccino."),
    ("Preferisci il te o il caffe?","Te|Caffe|Latte|Succo",1,"Preferisco il caffe lo bevo sempre dopo pranzo."),
    ("Quanti fratelli hai?","Uno|Due|Tre|Nessuno",3,"Sono figlia unica non ho fratelli ne sorelle."),
    ("Che tempo fa oggi?","Sole|Pioggia|Neve|Nuvolo",0,"Oggi c e il sole e fa molto caldo quasi trenta gradi."),
    ("Cosa studi?","Italiano|Inglese|Francese|Tedesco",0,"Studio italiano perche voglio vivere a Milano."),
    ("A che ora inizia la lezione?","8:00|9:00|10:00|14:00",1,"La lezione di italiano inizia alle nove in punto."),
    ("Dove e la stazione?","A destra|A sinistra|Sempre dritto|Dietro",0,"La stazione e a destra dopo il semaforo."),
    ("Cosa prendi al bar?","Cappuccino|Acqua|Birra|Vino",0,"Al bar prendo sempre un cappuccino con il cornetto."),
    ("Che giorno e oggi?","Lunedi|Martedi|Mercoledi|Giovedi",2,"Oggi e mercoledi siamo a meta settimana."),
    ("Dove compri il pane?","Panetteria|Supermercato|Mercato|Forno",0,"Compro il pane fresco alla panetteria sotto casa."),
    ("Quanto studi italiano?","Un mese|Sei mesi|Un anno|Due anni",2,"Studio italiano da un anno e ora so parlare."),
    ("Ti piace la pizza?","Si molto|No poco|Non mi piace|Non so",0,"La pizza mi piace tantissimo la margherita."),
    ("Dove e il bagno?","In fondo|A sinistra|Al primo piano|Di fianco",0,"Il bagno e in fondo al corridoio a destra."),
    ("Che libro leggi?","Romanzo|Saggio|Fumetto|Poesia",0,"Sto leggendo un bel romanzo giallo italiano."),
    ("Quando torni a casa?","Oggi|Domani|Sabato|Lunedi",2,"Torno a casa sabato dopo gli esami."),
    ("Dove lavori?","Ufficio|Ospedale|Scuola|Banca",2,"Lavoro in una scuola come insegnante di italiano."),
    ("Cosa fai nel tempo libero?","Leggo|Cucino|Gioco|Dormo",0,"Nel tempo libero leggo libri e vado al cinema."),
]
CILS["A1"]["lettura"] = [
    ("Cosa dice il testo?","Maria studia e lavora|Maria e studentessa|Non studia|Lavora in banca",1,"Maria ha 22 anni. Studia lingue all Universita di Venezia."),
    ("Dove vive Maria?","Roma|Milano|Venezia|Napoli",2,"Maria abita a Venezia una bellissima citta sul mare."),
    ("Di cosa parla il testo?","Una festa|Una scuola|Un viaggio|Un lavoro",0,"Sabato sera c e una festa da Marco. Portate da mangiare."),
    ("Cosa devono portare?","Da mangiare|Da bere|La musica|Regali",0,"Portate qualcosa da mangiare e da bere."),
    ("Orario del negozio?","8-13 e 15-19|9-13 e 14-18|8-12 e 14-20|9-18",0,"Panetteria aperta 8-13 e 15-19. Chiuso domenica."),
    ("Quando e chiuso?","Sabato|Domenica|Lunedi|Martedi",1,"Chiuso la domenica."),
    ("Cosa offre il ristorante?","Cucina italiana|Cucina cinese|Cucina giapponese|Messicana",0,"Ristorante Da Gigi offre cucina italiana tradizionale."),
    ("Quanto costa il menu fisso?","20|25|30|35",1,"Menu fisso a 25 euro vino incluso."),
    ("Cosa cerca Sara?","Lavoro|Casa|Corso|Amico",0,"Sara cerca lavoro come cameriera."),
    ("Che lingue parla?","Inglese e francese|Inglese e spagnolo|Francese|Tedesco",1,"Parla inglese e spagnolo."),
    ("Dove e l appartamento?","In centro|In periferia|Vicino stazione|In campagna",0,"Appartamento in centro tre locali."),
    ("Quante stanze ha?","2|3|4|5",1,"Tre locali piu cucina abitabile."),
    ("A che ora parte il treno?","14:30|15:00|15:30|16:00",0,"Treno per Firenze alle 14:30 binario 3."),
    ("Da che binario?","1|2|3|4",2,"Binario 3."),
    ("Quanto costa l abbonamento?","30|40|50|60",2,"Abbonamento palestra mensile 50 euro."),
]
CILS["A1"]["grammatica"] = [
    ("Io _____ (essere) italiano.","sono"),("Tu _____ (avere) vent anni.","hai"),
    ("Loro _____ (abitare) a Roma.","abitano"),("Noi _____ (studiare) italiano.","studiamo"),
    ("Lei _____ (chiamarsi) Maria.","si chiama"),("Voi _____ (venire) da Milano?","venite"),
    ("Io non _____ (sapere) la risposta.","so"),("Lui _____ (fare) il medico.","fa"),
    ("Noi _____ (andare) al cinema.","andiamo"),("Cosa _____ (tu dire)?","dici"),
    ("Io _____ (leggere) un libro.","leggo"),("Loro _____ (preferire) la pizza.","preferiscono"),
    ("Tu _____ (dovere) studiare.","devi"),("Noi _____ (volere) un caffe.","vogliamo"),
    ("Io _____ (potere) venire domani.","posso"),
]
CILS["A1"]["scrittura"] = [
    ("Presentati 40-50 parole: nome eta provenienza studio hobby.","mi chiamo|anni|vengo|studio|mi piace"),
    ("Descrivi la tua giornata tipo 40-50 parole.","mi sveglio|colazione|pranzo|cena|vado"),
    ("Cosa hai fatto ieri 40-50 parole.","ieri|mattina|pomeriggio|sera|andato"),
    ("Descrivi la tua famiglia 40-50 parole.","madre|padre|fratello|sorella|casa"),
    ("Parla della tua citta 40-50 parole.","citta|centro|musei|piace|bella"),
]
CILS["A1"]["orale"] = [
    ("Presentati e parla del tuo paese.","mi chiamo|vengo|vivo|studio|italia"),
    ("Parla della tua routine quotidiana.","sveglia|colazione|lezione|pranzo|dormo"),
    ("Descrivi la tua casa.","casa|stanze|cucina|salotto|camera"),
    ("Parla dei tuoi hobby.","tempo|libero|leggere|cinema|sport"),
    ("Racconta il tuo weekend.","sabato|domenica|amici|uscito|fatto"),
]

# ═══════════════ A2 ═══════════════
CILS["A2"]["ascolto"] = [
    ("Cosa hai fatto ieri?","Sono andato al mare|Ho studiato|Stato a casa|Ho lavorato",1,"Ieri ho studiato tutto il giorno per l esame."),
    ("Dove sei stato in vacanza?","Al mare|In montagna|In citta|All estero",3,"Sono stato in Spagna a Barcellona."),
    ("Cosa hai mangiato ieri?","Pasta|Pizza|Insalata|Pesce",0,"Ho mangiato pasta al pomodoro e insalata."),
    ("Che film hai visto?","Commedia|Dramma|Azione|Thriller",0,"Ho visto una commedia italiana divertente."),
    ("Con chi sei uscito?","Amici|Famiglia|Colleghi|Da solo",0,"Sono uscito con gli amici a cena."),
    ("Cosa hai comprato?","Un libro|Un vestito|Un telefono|Un regalo",0,"Ho comprato un libro di narrativa italiana."),
    ("Dove hai parcheggiato?","In strada|Nel parcheggio|In garage|In divieto",1,"Ho parcheggiato nel parcheggio sotterraneo."),
    ("Che tempo faceva?","Bello ma freddo|Caldo|Piovoso|Neve",0,"Faceva bello ma freddo circa 10 gradi."),
    ("Quando parti?","Questa settimana|Prossima|Mese prossimo|Non so",1,"Parto la prossima settimana con la famiglia."),
    ("Quanto hai speso?","20|50|100|200",2,"Ho speso cento euro per la spesa."),
    ("Cosa fai la sera?","Leggo|Guardo TV|Esco|Gioco",2,"Mi piace uscire con gli amici."),
    ("Che sport fai?","Nuoto|Calcio|Tennis|Palestra",3,"Vado in palestra tre volte a settimana."),
    ("Dove conosciuto il tuo amico?","A scuola|Al lavoro|In vacanza|Online",0,"Conosciuto Marco a scuola a 10 anni."),
    ("Cosa hai studiato?","Matematica|Storia|Italiano|Scienze",2,"Oggi studiato italiano 3 ore verbi."),
    ("Come ti senti?","Bene|Stanco|Male|Felice",1,"Stanco ho dormito solo 5 ore."),
]
CILS["A2"]["lettura"] = [
    ("Cosa racconta l email?","Viaggio|Lavoro|Studio|Festa",0,"Tornata da Roma fantastico visitato Colosseo e Fontana di Trevi."),
    ("Dove e andata?","Milano|Roma|Firenze|Napoli",1,"Andata a Roma una settimana."),
    ("Annuncio parla di?","Vendita|Lavoro|Affitto|Corso",2,"Affitto bilocale zona Prati 700 euro."),
    ("Quanto costa?","500|600|700|800",2,"700 euro al mese."),
    ("Cosa offre il corso?","Inglese|Italiano|Francese|Spagnolo",1,"Corso italiano per stranieri 3 livelli."),
    ("Lezioni quando?","Mattina|Pomeriggio|Sera|Weekend",2,"Lezioni serali 18-20."),
    ("Articolo parla di?","Cultura|Sport|Economia|Politica",0,"Museo Egizio Torino nuova sezione."),
    ("Dove si trova il museo?","Milano|Roma|Torino|Firenze",2,"Museo Egizio di Torino."),
    ("Cosa propone la ricetta?","Pasta|Dolce|Insalata|Zuppa",1,"Tiramisu fatto in casa."),
    ("Ingrediente principale?","Panna|Mascarpone|Cioccolato|Caffe",1,"Mascarpone ingrediente principale."),
    ("Evento dove?","Teatro|Cinema|Piazza|Museo",0,"Teatro Argentina La Traviata stasera."),
    ("Opera in scena?","Carmen|Traviata|Boheme|Tosca",1,"La Traviata di Verdi."),
    ("Il negozio vende?","Abbigliamento|Scarpe|Accessori|Libri",0,"Sconto 30% collezione autunno inverno."),
    ("Sconto quanto?","20%|30%|40%|50%",1,"Sconto trenta per cento."),
    ("La biblioteca offre?","Libri|Film|Musica|WiFi",3,"WiFi gratuito e postazioni studio."),
]
CILS["A2"]["grammatica"] = [
    ("Ieri _____ (io andare) al cinema.","sono andato|sono andata"),
    ("Da bambino _____ (giocare) sempre.","giocavo"),
    ("Quando _____ (tu arrivare) a Roma?","sei arrivato|sei arrivata"),
    ("Mentre _____ (io mangiare) suono il telefono.","mangiavo"),
    ("_____ (noi vedere) un bel film ieri.","abbiamo visto"),
    ("Da piccolo _____ (io volere) fare il pilota.","volevo"),
    ("Voi _____ (partire) per le vacanze?","siete partiti|siete partite"),
    ("Mentre loro _____ (passeggiare) ha piovuto.","passeggiavano"),
    ("Ieri non _____ (io potere) venire.","ho potuto"),
    ("Da giovane _____ (tu abitare) in campagna?","abitavi"),
    ("_____ (voi leggere) questo libro?","avete letto"),
    ("Mentre noi _____ (dormire) arrivo corriere.","dormivamo"),
    ("Loro _____ (sposarsi) l anno scorso.","si sono sposati|si sono sposate"),
    ("Quando _____ (io essere) piccolo avevo un cane.","ero"),
    ("Loro _____ (finire) i compiti ieri.","hanno finito"),
]
CILS["A2"]["scrittura"] = [
    ("Racconta il tuo weekend 60-80 parole.","sabato|domenica|amici|andato|visto"),
    ("Descrivi un viaggio 60-80 parole.","viaggio|visitato|visto|bello|andato"),
    ("Parla del tuo ultimo anno di studi.","anno|studiato|esami|imparato|professori"),
    ("Email a un amico per invitarlo a una festa.","festa|sabato|casa|invitare|portare"),
    ("Descrivi un film visto recentemente 60-80 parole.","film|visto|storia|attori|piaciuto"),
]
CILS["A2"]["orale"] = [
    ("Racconta un esperienza interessante recente.","fatto|esperienza|interessante|andato|vissuto"),
    ("Descrivi la tua citta preferita perche.","citta|preferita|perche|bella|visitare"),
    ("Parla dei tuoi progetti futuri.","futuro|progetti|voglio|spero|anno"),
    ("Descrivi una persona importante per te.","persona|importante|conosciuto|simpatico|aiutato"),
    ("Cosa fai di solito nel fine settimana?","fine|settimana|sabato|domenica|sempre"),
]

# ═══════════════ B1 ═══════════════
CILS["B1"]["ascolto"] = [
    ("Cosa e successo secondo il telegiornale?","Terremoto|Alluvione|Incendio|Frana",0,"Terremoto magnitudo 4.5 registrato questa mattina in Umbria."),
    ("Cosa dice l intervistato?","Favorevole|Contrario|Indeciso|Non risponde",1,"Contrario alla riforma perche penalizza i lavoratori."),
    ("Cosa ha deciso il comune?","Pista ciclabile|Parcheggio|Parco|Mercato",0,"Approvato progetto per nuova pista ciclabile in centro."),
    ("Cosa propone l associazione?","Ridurre rifiuti|Piantare alberi|Risparmiare acqua|Riciclare",1,"Proposta piantare mille nuovi alberi in periferia."),
    ("Quale servizio attivato?","Trasporto disabili|Sportello immigrati|Numero verde|App",2,"Numero verde per segnalazioni emergenza sociale."),
    ("Cosa dichiara il sindaco?","Nuova scuola|Nuovo ospedale|Nuovo teatro|Nuovo stadio",0,"Annunciata costruzione nuova scuola elementare."),
    ("Cosa pensano i cittadini?","A favore ZTL|Contro ZTL|Indifferenti|Non sanno",0,"65% favorevoli alla zona traffico limitato."),
    ("Iniziativa culturale?","Festival cinema|Fiera del libro|Mostra|Concerto",1,"Fiera del libro di Torino centinaia stand."),
    ("Cosa dice il dottore?","Fare sport|Riposare|Mangiare sano|Medicine",0,"Attivita fisica regolare 3 volte a settimana."),
    ("Cosa organizza l ufficio turistico?","Visite|Degustazioni|Escursioni|Laboratori",2,"Escursioni nei dintorni ogni weekend."),
    ("Legge approvata?","Sul lavoro|Sulla scuola|Sanita|Ambiente",0,"Nuova legge sul lavoro 280 voti."),
    ("Cosa preoccupa economisti?","Inflazione|Disoccupazione|Crescita|Debito",1,"Preoccupati aumento disoccupazione giovanile."),
    ("Tecnologia presentata?","AI|Robot|Droni|Pannelli solari",3,"Nuovi pannelli solari ad alta efficienza."),
    ("Cosa chiedono studenti?","Borse studio|Meno tasse|Piu aule|Piu docenti",0,"Piu borse di studio per merito."),
    ("Evento sportivo?","Olimpiadi|Mondiali|Europei|Campionati",1,"Mondiali calcio in Italia tra un mese."),
]
CILS["B1"]["lettura"] = [
    ("Tesi articolo?","Lavoro remoto positivo|Lavoro remoto negativo|Moda|Impossibile",0,"Studio: lavoro da remoto aumenta produttivita 20%."),
    ("Cosa consiglia l articolo?","Andare in ufficio|Lavorare da casa|Modello misto|Cambiare lavoro",2,"Ideale modello misto 3 giorni ufficio 2 casa."),
    ("Di cosa parla il testo?","Cambiamenti climatici|Inquinamento|Energia rinnovabile|Riciclo",2,"Italia superato 30% energia da fonti rinnovabili."),
    ("Obiettivo raggiunto?","20%|25%|30%|35%",2,"30% energia da rinnovabili."),
    ("Cosa descrive il brano?","Dipinto|Scultura|Monumento|Citta",0,"La Gioconda di Leonardo da Vinci."),
    ("Dove si trova?","Parigi|Roma|Firenze|Milano",0,"Museo del Louvre di Parigi."),
    ("Effetti del fenomeno?","Economici e sociali|Politici|Scientifici|Ambientali",0,"Invecchiamento popolazione effetti su economia e societa."),
    ("Soluzione proposta?","Piu immigrazione|Piu nascite|Riforma pensioni|Automazione",1,"Incentivi alla natalita."),
    ("Dallo studio scientifico?","Sonno fondamentale|Alimentazione|Sport|Socialita",0,"Dormire meno 6 ore aumenta rischi cardiovascolari."),
    ("Quante ore dormire?","Almeno 6|Almeno 7|Almeno 8|Almeno 9",1,"Raccomandate 7 ore di sonno."),
    ("Report economico analizza?","PIL|Inflazione|Occupazione|Esportazioni",2,"Tasso occupazione Italia salito al 62%."),
    ("Dato piu alto?","58%|60%|62%|65%",2,"Raggiunto 62%."),
    ("Autore del saggio propone?","Riforma scuola|Giustizia|Fiscale|Sanitaria",0,"Scuola ha bisogno di riforma profonda."),
    ("Problema segnalato?","Edifici vecchi|Docenti pochi|Programmi obsoleti|Studenti pochi",2,"Programmi obsoleti non preparano al lavoro."),
    ("Conclusione dibattito?","Necessario cambiamento|Mantenere status quo|Piu fondi|Aspettare",0,"Cambiamento necessario e urgente."),
]
CILS["B1"]["grammatica"] = [
    ("Spero che tu _____ (venire) alla festa.","venga"),
    ("Se _____ (io avere) piu tempo studierei cinese.","avessi"),
    ("Credo che loro _____ (arrivare) domani.","arrivino"),
    ("Benche _____ (essere) stanco e uscito.","fosse"),
    ("Vorrei che tu mi _____ (aiutare).","aiutassi"),
    ("Penso che loro _____ (avere) ragione.","abbiano"),
    ("Se noi _____ (sapere) prima saremmo venuti.","avessimo saputo"),
    ("Nonostante _____ (piovere) siamo andati al mare.","piovesse"),
    ("E importante che voi _____ (studiare) ogni giorno.","studiate"),
    ("Temo che lui non _____ (capire) la situazione.","capisca"),
    ("Se tu _____ (potere) mi aiuteresti?","potessi"),
    ("Benche _____ (avere) fretta si e fermato.","avesse"),
    ("Dubito che loro _____ (venire) alla riunione.","vengano"),
    ("Mi dispiace che voi non _____ (essere) contenti.","siate"),
    ("Se lui _____ (fare) attenzione non avrebbe sbagliato.","avesse fatto"),
]
CILS["B1"]["scrittura"] = [
    ("Email formale candidatura lavoro 80-100 parole.","candidatura|esperienza|competenze|disponibile|colloquio"),
    ("Opinione sull importanza delle lingue 80-100.","lingue|importante|opportunita|lavoro|cultura"),
    ("Esperienza di viaggio all estero 80-100.","viaggio|estero|esperienza|visitato|incontrato"),
    ("Recensione ristorante o film 80-100.","recensione|qualita|servizio|consiglio|voto"),
    ("Come immagini la vita tra 10 anni 80-100.","dieci|anni|lavoro|famiglia|spero"),
]
CILS["B1"]["orale"] = [
    ("Vantaggi e svantaggi vivere in grande citta.","vantaggi|svantaggi|citta|trasporti|costo"),
    ("Opinione sull uso dei social media.","social|media|comunicazione|opinione|tempo"),
    ("Libro o film che ti ha colpito.","libro|film|colpito|storia|personaggi"),
    ("Importanza della tutela dell ambiente.","ambiente|tutela|inquinamento|futuro|importante"),
    ("Fenomeno immigrazione in Italia.","immigrazione|italia|integrazione|lavoro|societa"),
]

# ═══════════════ B2 ═══════════════
CILS["B2"]["ascolto"] = [
    ("Conseguenze economiche decisione?","Aumento prezzi|Crescita occupazione|Riduzione tasse|Crisi mercato",0,"Decisione banca centrale ha causato aumento prezzi."),
    ("Cosa sostiene l economista?","Politica espansiva|Austerita fiscale|Investimenti|Liberalizzazioni",1,"Austerita necessaria per ridurre debito pubblico."),
    ("Riforma discussa in parlamento?","Sanita|Scuola|Giustizia|Fiscale",2,"Riforma giustizia per tempi piu rapidi processi."),
    ("Rapporto ONU evidenzia?","Aumento poverta|Miglioramento clima|Crescita demografica|Riduzione conflitti",0,"Preoccupante aumento poverta paesi in via sviluppo."),
    ("Innovazione tecnologica?","Processore|Batteria quantistica|Chip neuromorfico|Computer ottico",1,"Batteria quantistica si ricarica in secondi."),
    ("Ministro istruzione dichiara?","Piu fondi ricerca|Assunzione docenti|Nuovi programmi|Edilizia",0,"Aumento fondi destinati ricerca universitaria."),
    ("Tendenza demografica?","Invecchiamento|Calo natalita|Immigrazione|Urbanizzazione",1,"Istat calo nascite 1.2 figli per donna."),
    ("Preoccupa ambientalisti?","Deforestazione|Inquinamento aria|Scioglimento ghiacciai|Biodiversita",2,"Ghiacciai alpini si sciolgono doppio rispetto 10 anni fa."),
    ("Accordo commerciale?","UE-USA|UE-Cina|UE-Giappone|UE-Mercosur",3,"Ue firmato accordo commerciale con Mercosur."),
    ("Inchiesta rivela?","Corruzione|Evasione|Spionaggio|Riciclaggio",0,"Sistema corruzione coinvolge politici e imprenditori."),
    ("Scoperta archeologica?","Citta sommersa|Tomba etrusca|Tempio greco|Anfiteatro romano",1,"Scoperta tomba etrusca intatta VII secolo a.C."),
    ("Piano energetico?","Piu nucleare|Piu rinnovabili|Piu gas|Piu carbone",1,"Raggiungere 70% rinnovabili entro 2030."),
    ("Problema sociale denunciato?","Disuguaglianza|Razzismo|Poverta minorile|Violenza genere",0,"Crescente disuguaglianza nord-sud."),
    ("Nuovo piano urbanistico?","Piu parchi|Piu parcheggi|Trasporto pubblico|Piste ciclabili",2,"Potenziamento trasporto pubblico locale."),
    ("Iniziativa diplomatica?","Vertice pace|Missione ONU|Trattato|Conferenza",0,"Vertice di pace tra le parti in conflitto."),
]
CILS["B2"]["lettura"] = [
    ("Argomento centrale saggio?","Giustizia distributiva|Liberta|Uguaglianza|Diritti",0,"Saggio analizza giustizia distributiva nella filosofia politica."),
    ("Posizione criticata?","Liberalismo|Conservatorismo|Socialismo|Populismo",1,"Critica posizione conservatrice status quo."),
    ("Articolo scientifico sostiene?","Benefici meditazione|Inquinamento|Cancro|Terapie",0,"Mindfulness riduce stress migliora funzioni cognitive."),
    ("Evidenze presentate?","Studi clinici|Dati statistici|Testimonianze|Casi studio",0,"Studio clinico 500 pazienti mostra miglioramenti."),
    ("Inchiesta analizza?","Evasione|Criminalita organizzata|Corruzione|Concussione",1,"DDA analizza criminalita organizzata in Europa."),
    ("Dati mostrano?","Aumento sequestri|Riduzione reati|Collaborazioni|Meno denunce",0,"Aumento 40% sequestri beni mafia."),
    ("Volume tratta di?","Risorgimento|Unificazione|Figure storiche|Battaglie",0,"Analisi Risorgimento con nuova documentazione."),
    ("Figura rivalutata?","Garibaldi|Mazzini|Cavour|Vittorio Emanuele",2,"Cavour nel processo unificazione nazionale."),
    ("Editoriale propone?","Riforma elettorale|Cambio costituzionale|Decentramento|Federalismo",3,"Autonomia regionale modello federalista."),
    ("Modello citato?","Tedesco|Svizzero|Americano|Spagnolo",0,"Modello federalista tedesco."),
    ("Report sanita descrive?","Carenza personale|Innovazione|Efficienza|Qualita",0,"Carenza personale infermieristico negli ospedali."),
    ("Soluzione proposta?","Assunzioni|Formazione|Robotizzazione|Privatizzazione",0,"Assunzione 50.000 nuovi infermieri."),
    ("Documento UE analizza?","Politica agricola|Industriale|Energetica|Migratoria",2,"Politica energetica verso neutralita carbonica."),
    ("Obiettivo fissato?","2040|2050|2060|2070",1,"Neutralita carbonica entro 2050."),
    ("Filosofo sostiene?","Etica responsabilita|Individualismo|Collettivismo|Relativismo",0,"Etica responsabilita generazioni future."),
]
CILS["B2"]["grammatica"] = [
    ("Temono che governo non _____ (riuscire) a risolvere.","riesca"),
    ("Sebbene _____ (esserci) accordo non tutti soddisfatti.","ci fosse"),
    ("Nonostante noi _____ (insistere) non ha cambiato.","insistessimo|avessimo insistito"),
    ("Qualunque cosa tu _____ (dire) non gli fara cambiare.","dica"),
    ("Per quanto lui _____ (sforzarsi) non riesce.","si sforzi"),
    ("Nel caso in cui loro _____ (arrivare) tardi iniziamo.","arrivassero|arrivino"),
    ("Purché noi _____ (ricevere) il visto partiro.","riceviamo|abbiamo ricevuto"),
    ("Benche lui _____ (prepararsi) bene esame difficilissimo.","si fosse preparato"),
    ("E probabile che loro _____ (gia partire).","siano gia partiti|siano gia partite"),
    ("Temo che _____ (esserci) stato un malinteso.","ci sia"),
    ("A condizione che tutti _____ (essere) d accordo.","siano"),
    ("Malgrado noi _____ (avvertire) i colleghi non hanno risposto.","avessimo avvertito"),
    ("Qualunque _____ (essere) decisione la rispettero.","sia"),
    ("Incredibile che lui _____ (fare) cosa del genere.","abbia fatto"),
    ("Affinche il progetto _____ (riuscire) servono fondi.","riesca"),
]
CILS["B2"]["scrittura"] = [
    ("Articolo opinione cambiamento climatico 100-120.","cambiamento|climatico|ambiente|responsabilita|futuro"),
    ("Pro e contro della globalizzazione 100-120.","globalizzazione|economia|cultura|opportunita|criticita"),
    ("Relazione su evento culturale 100-120.","evento|culturale|partecipato|mostra|interessante"),
    ("Posizione su intelligenza artificiale 100-120.","intelligenza|artificiale|tecnologia|lavoro|futuro"),
    ("Lettera formale al sindaco problema citta 100-120.","sindaco|problema|citta|richiesta|soluzione"),
]
CILS["B2"]["orale"] = [
    ("Impatto social media sulla democrazia.","social|democrazia|informazione|disinformazione|media"),
    ("Rapporto tecnologia e mercato lavoro.","tecnologia|lavoro|automazione|competenze|formazione"),
    ("Opinione sul turismo di massa.","turismo|massa|overtourism|impatto|sostenibile"),
    ("Opinione sull integrazione europea.","europa|integrazione|unione|sovranita|solidarieta"),
    ("Ruolo universita nella societa contemporanea.","universita|formazione|ricerca|societa|futuro"),
]

# ═══════════════ C1 ═══════════════
CILS["C1"]["ascolto"] = [
    ("Posizione filosofica relatore?","Neopositivismo|Esistenzialismo|Fenomenologia|Strutturalismo",1,"Posizione esistenzialista enfatizza liberta e responsabilita."),
    ("Cosa critica il professore?","Riduzionismo scientifico|Determinismo|Relativismo|Scetticismo",0,"Critica riduzionismo scientifico che riduce complessita umana a dati."),
    ("Tesi dibattito accademico?","Linguaggio plasma pensiero|Pensiero precede|Indipendenti|Solo comunicazione",0,"Linguaggio non descrive realta ma la costruisce."),
    ("Ricerca sociologica evidenzia?","Nuova classe media|Declino operaia|Ascesa precariato|Frammentazione",2,"Ascesa del precariato come nuova classe sociale."),
    ("Paradigma epistemologico?","Realismo critico|Costruttivismo sociale|Empirismo logico|Razionalismo",1,"Costruttivismo sociale conoscenza costruita socialmente."),
    ("Conferenza bioetica analizza?","Eutanasia|Fecondazione|Ingegneria genetica|Staminali",2,"Implicazioni etiche ingegneria genetica embrioni."),
    ("Teoria politica presentata?","Liberalismo|Comunitarismo|Repubblicanesimo|Teoria critica",2,"Teoria repubblicana liberta come non-dominazione."),
    ("Economista eterodosso sostiene?","Decrescita|Neoliberismo|Keynesismo|Monetarismo",0,"Teoria della decrescita alternativa sviluppo illimitato."),
    ("Dibattito storiografico?","Revisionismo|Negazionismo|Storia sociale|Microstoria",0,"Revisionismo del Risorgimento."),
    ("Studio neuroscientifico rivela?","Neuroplasticita|Mappe cerebrali|Neuroni specchio|Sinapsi",2,"Neuroni specchio apprendimento per imitazione."),
    ("Questione giuridica?","Diritto autore|Privacy digitale|Brevetti|Liberta espressione",1,"Privacy digitale era big data."),
    ("Saggio estetica analizza?","Arte contemporanea|Estetica brutto|Bello ideale|Kitsch",0,"Rapporto arte contemporanea mercato globale."),
    ("Critica letteraria?","Decostruzione|New Historicism|Postcolonialismo|Gender",2,"Critica postcoloniale letteratura italiana contemporanea."),
    ("Dibattito scuola?","Meritocrazia|Uguaglianza|Valutazione|Autonomia",0,"Necessita selezione meritocratica scuola."),
    ("Scenario geopolitico?","Multipolarismo|Unipolarismo|Bipolarismo|Apolarita",0,"Emergere sistema multipolare."),
]
CILS["C1"]["lettura"] = [
    ("Autore argomenta?","Crisi democrazia rappresentativa|Trionfo liberale|Fine storia|Scontro civilta",0,"Democrazia rappresentativa in crisi disaffezione cittadini."),
    ("Soluzione proposta?","Democrazia deliberativa|Diretta|Governo tecnico|Populismo",0,"Modello democrazia deliberativa coinvolgere cittadini."),
    ("Testo su globalizzazione?","Aumentato disuguaglianze|Ridotto poverta|Uniformato culture|Frammentato economia",0,"Globalizzazione aumentato disuguaglianze tra paesi e interni."),
    ("Meccanismo criticato?","Mercato finanziario|Libero scambio|Mobilita capitale|Deregulation",2,"Mobilita capitali erode sovranita fiscale."),
    ("Societa digitale analizza?","Sorveglianza massa|Capitalismo digitale|Algoritmi|Piattaforme",1,"Capitalismo digitale basato su estrazione dati."),
    ("Concetto introdotto?","Plusvalore digitale|Lavoro immateriale|Sfruttamento cognitivo|Capitalismo sorveglianza",3,"Capitalismo sorveglianza Shoshana Zuboff."),
    ("Saggio linguaggio?","Istituzione sociale|Sistema formale|Abilita innata|Prodotto culturale",0,"Natura istituzionale del linguaggio fatto sociale."),
    ("Teoria confutata?","Grammatica universale|Sapir-Whorf|Atti linguistici|Pragmatica",0,"Confutata grammatica universale chomskiana neuroscienze."),
    ("Documento storico analizza?","Cause prima guerra mondiale|Trattato Versailles|Ascesa totalitarismi|Crisi democrazie",2,"Condizioni ascesa totalitarismi Europa."),
    ("Lezione storica?","Fragilita democrazie|Forza autoritarismi|Ruolo elite|Potere masse",0,"Fragilita istituzioni democratiche crisi economiche."),
    ("Articolo economia propone?","Reddito universale|Salario minimo|Sussidio|Lavoro garantito",0,"Reddito universale risposta automazione."),
    ("Obiezione discussa?","Costo eccessivo|Disincentivo lavoro|Inflazione|Dipendenza",0,"Principale obiezione costo finanze pubbliche."),
    ("Ricerca psicologica analizza?","Bias cognitivo|Euristica|Illusioni|Dissonanza",0,"Bias cognitivi processo decisionale."),
    ("Esperimento citato?","Milgram|Stanford|Hawthorne|Asch",0,"Esperimento Milgram obbedienza autorita."),
    ("Autore conclude?","Natura sociale uomo|Individualismo|Altruismo innato|Competizione",0,"Cooperazione tratto fondamentale natura umana."),
]
CILS["C1"]["grammatica"] = [
    ("Ove non _____ (esserci) soluzione si vota.","ci fosse"),
    ("Per quanto lui _____ (cercare) di nascondere si vede.","cerchi"),
    ("Laddove _____ (mancare) presupposti la proposta decade.","mancassero"),
    ("Qualora si _____ (rendere) necessario convocheremo.","rendesse"),
    ("Non che io _____ (opporsi) ma preferirei altro.","mi opponga"),
    ("A patto che _____ (finire) compiti entro stasera.","tu finisca|abbia finito"),
    ("Malgrado noi _____ (dirgli) verita non ha creduto.","gli avessimo detto"),
    ("Come se non _____ (bastare) le difficolta ora anche questo.","bastassero"),
    ("E ora che tu _____ (mettersi) a studiare.","ti metta"),
    ("Avrei preferito che loro _____ (arrivare) prima.","fossero arrivati|fossero arrivate"),
    ("Fosse anche _____ (essere) vero non cambierebbe.","stato"),
    ("Non e che io _____ (voler) criticare ma non concordo.","voglia"),
    ("Purché non _____ (loro fare) tardi possiamo aspettare.","facciano"),
    ("Ammesso che tutto _____ (andare) bene finiamo tra un mese.","vada"),
    ("Senza che nessuno _____ (accorgersene) e uscito.","se ne accorgesse"),
]
CILS["C1"]["scrittura"] = [
    ("Saggio breve etica e tecnologia 120-150 parole.","etica|tecnologia|responsabilita|innovazione|limiti"),
    ("Analisi post-verita comunicazione contemporanea 120-150.","post-verita|comunicazione|informazione|verita|media"),
    ("Posizione su cambiamenti climatici 120-150.","cambiamento|climatico|ambiente|politiche|futuro"),
    ("Ruolo cultura nell era globale 120-150.","cultura|globale|identita|diversita|dialogo"),
    ("Individuo e collettivita societa contemporanea 120-150.","individuo|collettivita|societa|liberta|responsabilita"),
]
CILS["C1"]["orale"] = [
    ("Liberta nella filosofia politica contemporanea.","liberta|filosofia|politica|autonomia|responsabilita"),
    ("Ruolo intellettuale nella societa di oggi.","intellettuale|societa|critica|cultura|impegno"),
    ("Sostenibilita modello sviluppo attuale.","sostenibilita|sviluppo|economia|ambiente|limiti"),
    ("Memoria storica e identita nazionale.","memoria|storica|identita|nazionale|passato"),
    ("Impatto AI sulla creativita umana.","intelligenza|artificiale|creativita|umano|arte"),
]

# ═══════════════ C2 ═══════════════
CILS["C2"]["ascolto"] = [
    ("Antinomia filosofo?","Liberta e responsabilita|Giustizia e uguaglianza|Individuo collettivita|Tradizione modernita",0,"Antinomia liberta individuale e responsabilita sociale."),
    ("Postmodernita afferma?","Fine meta-narrazioni|Nuovo illuminismo|Ritorno metafisica|Superamento",0,"Fine grandi narrazioni ideologiche."),
    ("Paradigma criticato?","Positivismo logico|Costruttivismo|Fenomenologia|Strutturalismo",0,"Positivismo logico insufficiente complessita sociale."),
    ("Concetto analizzato?","Biopolitica|Biopotere|Governamentalita|Dispositivo",0,"Biopolitica foucaultiana governo della vita."),
    ("Transizione ecologica conseguenze?","Antropologiche sociali|Economiche politiche|Culturali tecnologiche|Geopolitiche",0,"Profonde conseguenze antropologiche e sociali."),
    ("Critico letterario sostiene?","Fine letteratura|Rinascita romanzo|Decadenza poesia|Trionfo saggistica",1,"Rinascita romanzo contemporaneo."),
    ("Dibattito filosofico?","Etica virtu vs deontologia|Utilitarismo vs liberalismo|Contrattualismo vs comunitarismo|Realismo vs idealismo",0,"Etica della virtu e deontologia kantiana."),
    ("Studio coscienza rivela?","Correlati neurali|Natura fenomenica|Origine evolutiva|Funzione adattiva",0,"Correlati neurali della coscienza."),
    ("Teoria economica demolita?","Mercati efficienti|Moltiplicatore keynesiano|Curva Phillips|Parita potere",0,"Teoria mercati efficienti fallacie empiriche."),
    ("Saggio potere analizza?","Microfisica potere|Potere disciplinare|Biopotere|Sovranita",0,"Microfisica del potere istituzioni totali."),
    ("Questione etica dibattuta?","Miglioramento umano|Eutanasia|Aborto|Clonazione",0,"Miglioramento umano tecnologia genetica."),
    ("Analisi globalizzazione?","Nuova gerarchia globale|Decentramento|Rete orizzontale|Impero diffuso",0,"Nuova gerarchia globale post-occidentale."),
    ("Visione storia?","Progresso|Ciclo|Catastrofe|Caso",1,"Visione ciclica storia modello vichiano."),
    ("Linguista sostiene?","Relativita linguistica|Universalita grammaticale|Determinismo|Innativismo",0,"Relativita linguistica moderata."),
    ("Critica sociale?","Societa performance|Societa consumo|Societa disciplinare|Societa spettacolo",0,"Critica societa performance ossessione successo."),
]
CILS["C2"]["lettura"] = [
    ("Tesi brano Vattimo?","Fine realta forte interpretazione plurale|Nuova realta|Negazione interpretazione|Ritorno realismo",0,"Vattimo fine concezioni forti della realta."),
    ("Concetto introdotto?","Pensiero debole|Ontologia ermeneutica|Nichilismo attivo|Verita evento",0,"Pensiero debole come ermeneutica finitezza."),
    ("Filosofia politica?","Giustizia equita|Bene comune|Riconoscimento|Capacita umane",2,"Giustizia basata su riconoscimento differenze."),
    ("Critica liberismo?","Individualismo possessivo|Atomismo sociale|Mercificazione|Homo oeconomicus",0,"Individualismo possessivo fondamento liberismo."),
    ("Estetica analizza?","Bello simbolo bene|Arte verita|Giudizio estetico|Genio artistico",2,"Giudizio estetico ponte natura liberta."),
    ("Teoria difesa?","Realismo morale|Soggettivismo etico|Relativismo|Scetticismo",0,"Realismo morale fatti naturali oggettivi."),
    ("Testo letterario emerge?","Polisemia interpretativa|Univocita semantica|Intenzione autoriale|Ricezione",0,"Polisemia interpretativa del testo."),
    ("Metodologia proposta?","Decostruzione|Strutturale|Critica genetica|Stilistica",0,"Decostruzione metodo analisi testuale."),
    ("Autore linguaggio?","E un abisso|Tradisce pensiero|Crea realta|Trasparente",2,"Linguaggio crea realta sociale."),
    ("Teoria conoscenza difesa?","Realismo scientifico|Empirismo costruttivo|Strumentalismo|Relativismo",0,"Realismo scientifico obiezioni costruttivismo."),
    ("Saggio tempo?","Durata|Istante|Ciclo|Eternita",0,"Tempo bergsoniano come durata creativa."),
    ("Critica illuminismo?","Ragione strumentale|Dominio tecnico|Totalitarismo logico|Colonialismo",0,"Critica adorniana ragione strumentale dominio."),
    ("Identita?","Narrazione|Sostanza|Ruolo|Essenza",0,"Concezione narrativa identita personale."),
    ("Tecnica?","Destino|Strumento|Liberazione|Pericolo",3,"Heidegger tecnica pericolo e salvezza."),
    ("Conclusione testo?","Uomo liberta|Uomo natura|Uomo cultura|Uomo storia",0,"Tesi sartriana uomo condannato liberta."),
]
CILS["C2"]["grammatica"] = [
    ("Ove mai lui _____ (accorgersi) inganno reagirebbe.","si accorgesse"),
    ("Per quanto si _____ (sforzarsi) non ricordava.","sforzasse"),
    ("Laddove noi _____ (trovarsi) in disaccordo si vota.","ci trovassimo"),
    ("Come se non _____ (esserci) gia abbastanza.","ci fossero"),
    ("Quand anche lui _____ (avere) ragione non ammettera.","avesse"),
    ("Non e che noi _____ (dubitare) capacita ma...","dubitiamo|dubitassimo"),
    ("Fosse _____ (loro andare) via prima non avremmo problema.","andati|andate"),
    ("Trattandosi di emergenza _____ (noi dover) intervenire.","dobbiamo"),
    ("Pur _____ (essere) informato ha fatto finta.","essendo stato"),
    ("Al punto che nessuno _____ (sapere) piu cosa fare.","sa|sapeva"),
    ("Tale da non _____ (poter) credere ai propri occhi.","potere"),
    ("Affinche tutti _____ (poter) comprendere.","potessero|possano"),
    ("Tanto _____ (loro insistere) che abbiamo ceduto.","hanno insistito"),
    ("Per il fatto che _____ (tu non rispondere) abbiamo concluso.","non hai risposto"),
    ("Non gia che io _____ (opporsi) ma trovo inopportuno.","mi opponga"),
]
CILS["C2"]["scrittura"] = [
    ("Saggio critico verita era post-verita 150-180.","verita|post-verita|informazione|conoscenza|interpretazione"),
    ("Potere e sapere societa contemporanea 150-180.","potere|sapere|societa|conoscenza|disciplina"),
    ("Crisi rappresentanza politica 150-180.","crisi|rappresentanza|politica|democrazia|partecipazione"),
    ("Ruolo arte societa spettacolo 150-180.","arte|spettacolo|societa|cultura|consumo"),
    ("Populismo chiave storico-politica 150-180.","populismo|politica|democrazia|popolo|leadership"),
]
CILS["C2"]["orale"] = [
    ("Riconoscimento filosofia politica contemporanea.","riconoscimento|filosofia|politica|identita|differenza"),
    ("Riflessione critica sul concetto di progresso.","progresso|critica|storia|modernita|societa"),
    ("Etica ed economia capitalismo contemporaneo.","etica|economia|capitalismo|giustizia|mercato"),
    ("Memoria collettiva identita nazionale.","memoria|collettiva|identita|nazionale|storia"),
    ("Universalismo e particolarismo cultura globalizzata.","universalismo|particolarismo|cultura|globale|diversita"),
]

print(f"CILS data loaded: {sum(len(CILS[lv]['ascolto'])+len(CILS[lv]['lettura'])+len(CILS[lv]['grammatica'])+len(CILS[lv]['scrittura'])+len(CILS[lv]['orale']) for lv in LEVELS)} questions")
