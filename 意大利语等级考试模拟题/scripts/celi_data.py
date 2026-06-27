#!/usr/bin/env python3
"""CELI independent question data - 6 levels x 5 sets, each with unique questions.
CELI official: Univ. di Perugia - reading-heavy, text comprehension, text analysis
Different emphasis from CILS: more reading, different grammar, less dialogue"""

CELI = {}
LEVELS = ["A1","A2","B1","B2","C1","C2"]
for lv in LEVELS:
    CELI[lv] = {"ascolto":[],"lettura":[],"grammatica":[],"scrittura":[],"orale":[]}

# ═══════════════ A1 ═══════════════
CELI["A1"]["ascolto"] = [
    ("Cosa viene annunciato?","Apertura negozio|Chiusura scuola|Festa paese|Concerto",0,"Attenzione in via Roma ha aperto un nuovo supermercato."),
    ("Chi parla?","Professore|Poliziotto|Medico|Giornalista",3,"Oggi parliamo del bel tempo che accompagnera il weekend."),
    ("Numero di telefono?","329-4567|328-4567|327-4567|326-4567",1,"Il numero e 328-4567 chiamare dopo le 17."),
    ("Dove si trova il mercato?","In piazza|In via Cavour|In centro|Vicino stazione",2,"Mercato si trova in centro vicino alla fontana."),
    ("A che ora chiude farmacia?","19:00|19:30|20:00|20:30",2,"Farmacia chiude alle 20 giovedi fino alle 22."),
    ("Cosa comprare al mercato?","Frutta|Vestiti|Libri|Giocattoli",0,"Frutta e verdura fresca ogni mattina."),
    ("Quanto costa biglietto museo?","5|8|10|12",2,"Biglietto 10 euro gratuito sotto 18 anni."),
    ("Dove ufficio postale?","Piazza Garibaldi|Via Torino|Corso Italia|Viale Roma",0,"Ufficio postale in piazza Garibaldi accanto al bar."),
    ("Cosa si festeggia sabato?","Carnevale|Natale|Pasqua|Festa Repubblica",0,"Sfilata di Carnevale per le vie del centro."),
    ("Che tempo domani?","Sole|Pioggia|Neve|Nuvoloso",1,"Previsa pioggia su tutto il territorio regionale."),
    ("Dove andate stasera?","Al cinema|A teatro|Al ristorante|Al concerto",2,"Andiamo al ristorante per compleanno Laura."),
    ("Cosa ordinate?","Pizza|Pasta|Insalata|Bistecca",0,"Pizza margherita e acqua naturale."),
    ("Cosa fa Luca domenica?","Gioca calcio|Va al mare|Studia|Lavora",0,"Luca gioca a calcio con amici al parco."),
    ("Dove biblioteca?","Via Dante|Viale Roma|In piazza|Corso Umberto",0,"Biblioteca comunale via Dante 25."),
    ("Cosa vuole Anna?","Gelato|Caffe|Te|Birra",1,"Anna vuole un caffe senza zucchero."),
]
CELI["A1"]["lettura"] = [
    ("Dove supermercato?","Via Mazzini|Corso Italia|Piazza del Popolo|Viale Roma",0,"Nuovo Conad via Mazzini angolo piazza Repubblica."),
    ("Orari apertura?","7:30-21|8-20:30|8-21|7:30-20:30",0,"Aperto 7:30-21 dal lunedi al sabato."),
    ("Menu ristorante?","Fisso 15 euro|Degustazione|Pizza|Buffet",0,"Menu fisso 15 euro primo secondo contorno dolce."),
    ("Cosa include menu?","Primo secondo|Primo secondo dolce|Primo secondo contorno dolce|Antipasto primo secondo",2,"Primo secondo contorno e dolce."),
    ("Annuncio descrive?","Casa vendita|Casa affitto|Ufficio|Negozio",0,"Vendesi bilocale ristrutturato San Giovanni 70 mq."),
    ("Metri quadri?","50|60|70|80",2,"70 metri quadri."),
    ("Corso scuola?","Inglese|Italiano|Francese|Spagnolo",1,"Corsi italiano per principianti assoluti."),
    ("Ore settimana?","2|3|4|5",1,"Tre ore a settimana lunedi e mercoledi."),
    ("Concerto dove?","Teatro|Parco|Piazza|Palazzetto",2,"Concerto banda cittadina in piazza del Comune."),
    ("A che ora?","20|20:30|21|21:30",3,"Inizio 21:30 ingresso gratuito."),
    ("Negozio abbigliamento?","Sconto 20%|30%|40%|50%",3,"Sconto 50% tutta collezione autunno inverno."),
    ("Offerta fino a?","Sabato|Domenica|Lunedi|Martedi",0,"Fino a sabato 15 marzo."),
    ("Cosa fare al parco?","Correre|Giocare|Picnic|Bici",2,"Aree picnic e percorsi pedonali."),
    ("Parco aperto?","6-20|7-21|8-22|6-22",0,"6:00-20:00 in inverno."),
    ("Per iscrizione palestra?","Documento|Tessera|Certificato medico|Foto",2,"Certificato medico idoneita sportiva."),
]
CELI["A1"]["grammatica"] = [
    ("Marco _____ (lavorare) in un ufficio.","lavora"),
    ("Noi _____ (parlare) italiano.","parliamo"),
    ("Loro _____ (vivere) a Milano.","vivono"),
    ("Io _____ (volere) un caffe.","voglio"),
    ("Tu _____ (venire) con noi?","vieni"),
    ("Voi _____ (avere) fame?","avete"),
    ("Lei _____ (chiamarsi) Anna.","si chiama"),
    ("Noi non _____ (capire) questa frase.","capiamo"),
    ("Loro _____ (preferire) la pizza.","preferiscono"),
    ("Io _____ (studiare) medicina.","studio"),
    ("Tu _____ (dovere) studiare.","devi"),
    ("Lui _____ (sapere) parlare inglese.","sa"),
    ("Noi _____ (andare) al mare d estate.","andiamo"),
    ("Voi _____ (bere) il caffe?","bevete"),
    ("Io _____ (leggere) molti libri.","leggo"),
]
CELI["A1"]["scrittura"] = [
    ("Email presentazione a nuovo amico penna 40-50.","caro|amico|mi chiamo|italiano|ciao"),
    ("Descrivi la tua stanza 40-50 parole.","stanza|letto|scrivania|finestra|colore"),
    ("Parla del tuo cibo preferito 40-50.","cibo|preferito|buono|mangio|ristorante"),
    ("Cosa fai di solito la domenica 40-50.","domenica|alzarsi|colazione|pranzo|sera"),
    ("Descrivi il tuo amico del cuore 40-50.","amico|simpatico|gentile|insieme|alto"),
]
CELI["A1"]["orale"] = [
    ("Giornata tipo lunedi venerdi.","sveglia|studiare|pranzo|casa|sera"),
    ("La tua famiglia quanti siete.","famiglia|madre|padre|fratello|sorella"),
    ("Cosa ti piace tempo libero.","piace|tempo|libero|sport|amici"),
    ("Parla del tuo paese com e.","paese|citta|centro|piazza|bello"),
    ("Descrivi la tua scuola lavoro.","scuola|lavoro|ufficio|colleghi|lezioni"),
]

# ═══════════════ A2 ═══════════════
CELI["A2"]["ascolto"] = [
    ("Signora chiede?","Indicazioni|Orari treni|Numeri|Prezzi",0,"Scusi sa dov e la stazione per Firenze?"),
    ("Deve andare dove?","Roma|Firenze|Bologna|Milano",1,"Devo prendere il treno per Firenze."),
    ("Marco ha perso?","Portafoglio|Chiavi|Telefono|Borsa",0,"Marco attenzione portafoglio caduto per terra."),
    ("Dov e caduto?","Per terra|Sedia|Tavolo|Macchina",0,"Portafoglio caduto per terra."),
    ("Bambina mangia?","Pasta|Pizza|Patatine|Gelato",2,"Mamma posso prendere le patatine fritte?"),
    ("Mamma risponde?","Si|No|Dopo|Forse",1,"No cara non vanno bene prima di cena."),
    ("Uomo cerca?","Regalo|Libro|Vestito|Giocattolo",0,"Cerco regalo per ragazza compie anni domani."),
    ("Cosa compra?","Profumo|Fiori|Borsa|Sciarpa",1,"Decido per un bel mazzo di fiori."),
    ("Appuntamento dove?","Ristorante|Cinema|Parco|Bar",0,"Ci vediamo stasera 20:30 al ristorante Da Gigi."),
    ("A che ora?","19:30|20|20:30|21",2,"Alle 20:30."),
    ("Paolo cosa ha?","Mal di testa|Mal di pancia|Schiena|Dente",0,"Paolo ha mal di testa sta a casa."),
    ("Perche non viene?","Stanco|Mal di testa|Lavora|Studia",1,"Ha mal di testa."),
    ("Previsione tempo?","Bel tempo stabile|Pioggia|Neve|Temporali",3,"Domani temporali su tutto il nord."),
    ("Dove temporali?","Nord|Centro|Sud|Tutta Italia",0,"Nord Italia."),
    ("Farmacia turno?","Via Nazionale|Corso Umberto|Piazza San Carlo|Viale Giardini",2,"Farmacia piazza San Carlo."),
]
CELI["A2"]["lettura"] = [
    ("Lucia email?","Racconta vacanze|Chiede favore|Annuncia|Invita",3,"Ti invito alla mia festa di compleanno sabato."),
    ("Quando festa?","Giovedi|Venerdi|Sabato|Domenica",2,"Sabato prossimo."),
    ("Promozione offre?","Sconto secondo acquisto|Omaggio|Due prezzo uno|Spedizione gratis",0,"Seconda notte hotel a meta prezzo."),
    ("Vale in?","Tutti hotel|4 stelle|Solo Italia|Solo estate",0,"Tutti gli hotel della catena."),
    ("Blog viaggio?","Roma|Firenze|Venezia|Napoli",2,"Venezia meravigliosa gondola e San Marco."),
    ("Visto cosa?","Colosseo|Piazza San Marco|Ponte Vecchio|Piazza Plebiscito",1,"Piazza San Marco e Ponte Rialto."),
    ("Avviso dice?","Lavori strada|Chiusura ufficio|Sciopero mezzi|Ritardi treni",2,"Venerdi 25 sciopero mezzi pubblici."),
    ("Venerdi 25?","Festa nazionale|Sciopero|Giorno festivo|Chiusura",1,"Sciopero mezzi pubblici."),
    ("Annuncio lavoro?","Cameriere tempo pieno|Cuoco|Barista|Commesso",0,"Cameriere ristorante full time esperienza."),
    ("Richiesto?","Esperienza|Laurea|Patente|Macchina",0,"Esperienza nel settore."),
    ("Carta fedelta?","Punti sconto|Regali|Omaggi|Voucher",0,"Accumuli punti per sconti."),
    ("Cosa ottenere?","Sconti|Prodotti gratis|Buoni|Omaggi",0,"Punti trasformati in sconti."),
    ("Corso cucina dove?","Via Dante|Via Garibaldi|Piazza Navona|Corso Vittorio",1,"In via Garibaldi 45."),
    ("Durata corso?","Un mese|Due|Tre|Quattro",2,"Tre mesi martedi e giovedi."),
    ("Cosa si impara?","Pasta fresca|Pizza|Dolci|Antipasti",0,"Preparare pasta fresca fatta in casa."),
]
CELI["A2"]["grammatica"] = [
    ("Ieri sera noi _____ (andare) al ristorante.","siamo andati|siamo andate"),
    ("Da bambina io _____ (vivere) in campagna.","vivevo"),
    ("_____ (tu vedere) il film di ieri?","hai visto"),
    ("Mentre loro _____ (mangiare) suono campanello.","mangiavano"),
    ("L anno scorso noi _____ (visitare) Parigi.","abbiamo visitato"),
    ("Da piccolo io _____ (avere) un cane bianco.","avevo"),
    ("Voi _____ (finire) i compiti?","avete finito"),
    ("Mentre io _____ (fare) doccia squillato telefono.","facevo"),
    ("Ieri loro _____ (arrivare) tardi a casa.","sono arrivati|sono arrivate"),
    ("Quando tu _____ (essere) piccolo avevi paura?","eri"),
    ("_____ (noi comprare) macchina nuova.","abbiamo comprato"),
    ("Da giovani loro _____ (giocare) tennis.","giocavano"),
    ("_____ (io perdere) portafoglio ieri.","ho perso"),
    ("Mentre noi _____ (passeggiare) incontrato Maria.","passeggiavamo"),
    ("Loro _____ (sposarsi) nel 2023.","si sono sposati|si sono sposate"),
]
CELI["A2"]["scrittura"] = [
    ("Cartolina da citta italiana visitando 60-80.","cartolina|visito|citta|bello|arrivederci"),
    ("Cosa hai mangiato ieri ristorante 60-80.","ieri|ristorante|mangiato|primo|dolce"),
    ("Ultimo regalo compleanno 60-80.","compleanno|regalo|amici|bello|contento"),
    ("Messaggio amico organizzare uscita 60-80.","uscita|sabato|cinema|appuntamento|amici"),
    ("Ultima vacanza 60-80 parole.","vacanza|estate|andato|mare|divertito"),
]
CELI["A2"]["orale"] = [
    ("Casa ideale come la immagini.","casa|ideale|stanze|giardino|cucina"),
    ("Piatto preferito come si prepara.","piatto|preferito|ingredienti|preparare|cucina"),
    ("Ricordo d infanzia.","ricordo|infanzia|piccolo|gioco|quando"),
    ("Gita fuori citta.","gita|fuori|citta|campagna|giornata"),
    ("Sport preferito perche.","sport|preferito|gioco|squadra|settimana"),
]

# ═══════════════ B1 ═══════════════
CELI["B1"]["ascolto"] = [
    ("Notizia principale?","Sciopero trasporti|Nuovo Museo|Riforma sanitaria|Alluvione",0,"Sciopero nazionale trasporti venerdi 15 dalle 9 alle 17."),
    ("Durata sciopero?","4 ore|8 ore|12 ore|24 ore",1,"Dalle 9 alle 17 otto ore."),
    ("Cosa presenta la mostra?","Futurismo|Rinascimento|Barocco|Contemporaneo",0,"Mostra sul Futurismo italiano a Palazzo Reale."),
    ("Durata mostra?","Fino dicembre|Fino gennaio|Fino febbraio|Fino marzo",2,"Aperta fino al 28 febbraio 2026."),
    ("Cosa annuncia assessore?","Nuovo parco|Nuovo teatro|Nuova piscina|Nuovo stadio",0,"Nuovo parco urbano con zona cani e pista jogging."),
    ("Dove verra realizzato?","Zona nord|Periferia ovest|Centro|Sud",1,"Nell area dismessa della ex fabbrica in periferia ovest."),
    ("Nuova legge cosa introduce?","Congedo parentale|Tredicesima|Quattordicesima|Bonus bebè",0,"Congedo parentale retribuito al 60% per entrambi genitori."),
    ("Quanto retribuito?","50%|60%|70%|80%",1,"Retribuito al 60%."),
    ("Rapporto FAO?","Aumento fame|Riduzione povertà|Siccita|Alluvioni",0,"Aumento fame nel mondo 150 milioni persone."),
    ("Quante persone?","100 milioni|150 milioni|200 milioni|250 milioni",1,"150 milioni di persone in piu."),
    ("Conferenza sanita?","Screening gratuiti|Farmaci gratis|Vaccini obbligatori|Ospedali nuovi",0,"Campagna screening gratuiti per prevenzione tumori."),
    ("Quanti esami?","2|3|4|5",2,"Quattro esami gratuiti per over 50."),
    ("Iniziativa scuola?","Tutoraggio|Borse studio|Scambi culturali|Mensa gratis",2,"Programma scambi culturali con scuole europee."),
    ("Paesi coinvolti?","3|4|5|6",3,"6 paesi coinvolti Francia Spagna Germania."),
    ("Crisi economica?","Calo PIL|Inflazione|Disoccupazione|Debito",0,"Pil italiano calato dello 0.3% ultimo trimestre."),
]
CELI["B1"]["lettura"] = [
    ("Articolo parla di?","Riforma fiscale|Riforma pensioni|Riforma scuola|Sanita",0,"Nuova riforma fiscale introduce aliquota unica 25%."),
    ("Aliquota unica?","20%|25%|30%|33%",1,"Aliquota unica al 25% per semplificare sistema."),
    ("Testo descrive?","Nuova legge|Nuovo regolamento|Nuovo servizio|Nuova tassa",0,"Nuovo regolamento per affitti brevi obbligo registrazione."),
    ("Obbligo per?","Proprietari|Turisti|Agenzie|Vicini",0,"Proprietari devono registrare contratti."),
    ("Cosa analizza l inchiesta?","Spesa pubblica|Spesa sanitaria|Spesa militare|Spesa istruzione",0,"Analisi spesa pubblica italiana 50% spesa sociale."),
    ("Percentuale spesa sociale?","40%|45%|50%|55%",2,"50% della spesa pubblica destinata a sociale."),
    ("Nuova tecnologia?","Pompa calore|Pannelli solari|Turbina eolica|Batteria",0,"Pompa di calore geotermica riduce consumi 60%."),
    ("Riduzione consumi?","40%|50%|60%|70%",2,"Riduzione 60%."),
    ("Rapporto Istat?","Invecchiamento|Natalita|Immigrazione|Occupazione",0,"Indice invecchiamento sale a 193 over 65 ogni 100 giovani."),
    ("Indice invecchiamento?","170|180|190|193",3,"193 over 65 ogni 100 giovani."),
    ("Intervista esperto?","Transizione digitale|Automazione|AI|Robot",0,"Transizione digitale creera 2 milioni posti lavoro."),
    ("Posti creati?","1 milione|2 milioni|3 milioni|4 milioni",1,"2 milioni nuovi posti entro 2030."),
    ("Ricerca universitaria?","Nuovo farmaco|Nuovo vaccino|Nuova terapia|Nuovo test",0,"Nuovo farmaco per Alzheimer rallenta degenerazione."),
    ("Rallentamento?","20%|30%|40%|50%",1,"Rallenta degenerazione del 30%."),
    ("Editoriale cosa critica?","Burocrazia|Corruzione|Evasione|Clientelismo",0,"Critica burocrazia eccessiva ostacola investimenti."),
]
CELI["B1"]["grammatica"] = [
    ("Penso che loro _____ (arrivare) domani.","arrivino"),
    ("Se _____ (io sapere) risposta te lo direi.","sapessi"),
    ("E meglio che tu _____ (andare) via.","vada"),
    ("Benche _____ (lui essere) ricco non e felice.","sia"),
    ("Vorrei che voi _____ (partecipare) alla riunione.","partecipaste"),
    ("Non credo che _____ (loro avere) tempo.","abbiano"),
    ("Se _____ (noi potere) vi aiuteremmo.","potessimo"),
    ("Nonostante _____ (io dire) la verita non ha creduto.","dicessi"),
    ("Spero che voi _____ (divertirsi) alla festa.","vi divertiate"),
    ("Dubito che lui _____ (capire) l italiano.","capisca"),
    ("Se _____ (lei sapere) prima sarebbe venuta.","avesse saputo"),
    ("Benche _____ (piovere) siamo usciti.","piovesse"),
    ("Credevo che loro _____ (partire) gia.","fossero gia partiti|fossero gia partite"),
    ("Permetto che lui _____ (usare) il mio computer.","usi"),
    ("Se _____ (voi vedere) Marco salutatemelo.","vedete"),
]
CELI["B1"]["scrittura"] = [
    ("Racconta esperienza volontariato 80-100 parole.","volontariato|esperienza|aiutare|tempo|persone"),
    ("Opinione su dieta mediterranea 80-100.","dieta|mediterranea|cibo|salute|tradizione"),
    ("Descrivi festa tradizionale italiana 80-100.","festa|tradizionale|italiana|celebrare|usanza"),
    ("Lettera ringraziamento a professore 80-100.","ringraziamento|professore|insegnato|crescita|corso"),
    ("Recensione hotel o B&B 80-100 parole.","hotel|soggiorno|servizio|posizione|consiglio"),
]
CELI["B1"]["orale"] = [
    ("Importanza volontariato nella societa.","volontariato|societa|aiuto|solidarieta|comunita"),
    ("Tradizioni italiane che conosci.","tradizioni|italia|feste|cucina|usanze"),
    ("Parla del sistema scolastico italiano.","scuola|italia|universita|studio|esami"),
    ("Cosa pensi del turismo sostenibile?","turismo|sostenibile|ambiente|viaggi|rispetto"),
    ("Differenze tra nord e sud Italia.","nord|sud|italia|differenze|cultura"),
]

# ═══════════════ B2 ═══════════════
CELI["B2"]["ascolto"] = [
    ("Intervista economista?","Crisi energetica|Inflazione|crescita|Debito",0,"Crisi energetica colpisce produzione industriale."),
    ("Settore piu colpito?","Automotive|Siderurgico|Tessile|Alimentare",1,"Siderurgico produzione calata 15%."),
    ("Nuova normativa UE?","Digital tax|Privacy|Copyright|Antitrust",0,"Nuova digital tax grandi piattaforme 3% fatturato."),
    ("Aliquota digital tax?","1%|2%|3%|4%",2,"3% fatturato per aziende sopra 750 milioni."),
    ("Inchiesta sanita?","Liste attesa|Carenza medici|Privatizzazione|Ticket",0,"Liste attesa esami specialistici oltre 6 mesi."),
    ("Tempo attesa medio?","2 mesi|4 mesi|6 mesi|8 mesi",2,"Oltre 6 mesi per visita specialistica."),
    ("Convegno neuroscienze?","Memoria|Apprendimento|Emozioni|Linguaggio",0,"Nuove scoperte sulla memoria procedurale."),
    ("Parte cervello?","Ippocampo|Corteccia|Cervelletto|Amigdala",2,"Memoria procedurale localizzata nel cervelletto."),
    ("Rapporto banca d Italia?","Credito imprese|Mutui famiglie|Risparmio|Investimenti",0,"Crisi credito imprese calo 12% prestiti."),
    ("Crollo prestiti?","8%|10%|12%|15%",2,"Prestiti calati del 12%."),
    ("Conferenza clima?","Zero emissioni|Riduzione CO2|Energia pulita|Rinnovabili",0,"Obiettivo zero emissioni nette entro 2045."),
    ("Entro quando?","2035|2040|2045|2050",2,"Obiettivo zero emissioni nette 2045."),
    ("Statistiche immigrazione?","Ingressi regolari|Richiedenti asilo|Ricongiungimenti|Studenti",1,"Aumento richiedenti asilo del 35%."),
    ("Aumento quanto?","15%|25%|35%|45%",2,"Richiedenti asilo aumentati 35%."),
    ("Evento culturale?","Biennale Venezia|Salone del libro|Festival Sanremo|Maggio Fiorentino",0,"Aperta Biennale Arte di Venezia tema straniamento."),
]
CELI["B2"]["lettura"] = [
    ("Saggio sociologia?","Società liquida|Modernità solida|Tradizione|Post-modernità",0,"Bauman societa liquida relazioni umane diventano fluide."),
    ("Concetto chiave?","Liquidita|Solidita|Gas|Vapore",0,"La liquidita come metafora della contemporaneita."),
    ("Editoriale economia?","Inflazione strutturale|Stagflazione|Deflazione|Ristagno",0,"Inflazione strutturale causata da scarsita materie prime."),
    ("Causa inflazione?","Domanda eccessiva|Scarsita materie prime|Speculazione|Moneta",1,"Scarsita materie prime causa principale."),
    ("Saggio letteratura?","Romanzo storico|Neorealismo|Postmoderno|Decadentismo",2,"Analisi romanzo postmoderno Calvino Eco."),
    ("Autori analizzati?","Calvino e Eco|Moravia e Pavese|Svevo e Pirandello|Manzoni e Verga",0,"Calvino e Eco esponenti postmoderno."),
    ("Inchiesta giustizia?","Processi lunghi|Carceri sovraffollate|Recidiva|Riforma",0,"Durata media processi 4 anni prima sentenza."),
    ("Durata media?","2 anni|3 anni|4 anni|5 anni",2,"4 anni per processi civili."),
    ("Ricerca genetica?","DNA|Genoma|Editing genetico|Terapia genica",2,"Crispr editing genetico apre nuove frontiere."),
    ("Cosa modifica?","DNA|RNA|Proteine|Cellule",0,"Modifica DNA con precisione mai vista."),
    ("Analisi geopolitica?","Nuovo ordine|Guerra fredda|Bipolarismo|Decolonizzazione",0,"Nuovo ordine mondiale multipolare."),
    ("Attori emergenti?","BRICS|G7|NATO|ONU",0,"Brics paesi emergenti ridefiniscono equilibri."),
    ("Critica architettura?","Sostenibile|Brutalista|Futurista|Minimalista",0,"Architettura sostenibile nuovi materiali e basso impatto."),
    ("Obiettivo?","Impatto zero|Risparmio energetico|Riciclo materiali|Bioedilizia",0,"Costruzioni a impatto zero."),
    ("Rapporto educazione?","Competenze digitali|Soft skills|STEM|Umanistiche",0,"Competenze digitali fondamentali mercato lavoro."),
]
CELI["B2"]["grammatica"] = [
    ("Nonostante _____ (lui provare) non e riuscito.","provasse|avesse provato"),
    ("Se _____ (loro arrivare) in tempo vedrebbero spettacolo.","arrivassero"),
    ("E giusto che _____ (tu dire) la verita.","tu dica"),
    ("Temo che _____ (noi fare) tardi.","facciamo|abbiamo fatto"),
    ("Per quanto _____ (lui impegnarsi) non basta.","si impegni"),
    ("Benche _____ (noi avere) ragione abbiamo taciuto.","avessimo"),
    ("A condizione che tutti _____ (partecipare) all incontro.","partecipino"),
    ("Senza che nessuno _____ (accorgersi) e sparito.","si accorgesse"),
    ("Dubito che _____ (essere) la soluzione giusta.","sia"),
    ("Malgrado _____ (loro insistere) non abbiamo cambiato.","insistessero|avessero insistito"),
    ("Credevo che _____ (tu sapere) tutto.","sapessi"),
    ("Qualunque _____ (essere) il motivo non giustifica.","sia"),
    ("Nel caso in cui _____ (lui rifiutare) chiamatemi.","rifiuti|rifiutasse"),
    ("Se solo _____ (io potere) tornare indietro.","potessi"),
    ("Non e che _____ (noi preferire) aspettare.","preferiamo|preferissimo"),
]
CELI["B2"]["scrittura"] = [
    ("Analisi fenomeno smart working pro contro 100-120.","smart|working|flessibilita|produttivita|isolamento"),
    ("Articolo valorizzazione patrimonio culturale 100-120.","patrimonio|culturale|arte|storia|conservazione"),
    ("Posizione su energia nucleare 100-120.","nucleare|energia|sicurezza|futuro|ambiente"),
    ("Relazione su conferenza TED assistita 100-120.","conferenza|TED|intervento|idee|ispirato"),
    ("Lettera direttore su problema quartiere 100-120.","direttore|quartiere|problema|proposta|soluzione"),
]
CELI["B2"]["orale"] = [
    ("Impatto intelligenza artificiale sulla societa.","intelligenza|artificiale|societa|lavoro|etica"),
    ("Sviluppo sostenibile e green economy.","sostenibile|green|economia|ambiente|futuro"),
    ("Migrazioni e integrazione.","migrazioni|integrazione|accoglienza|societa|cultura"),
    ("Ruolo della donna nella societa contemporanea.","donna|societa|parita|lavoro|diritti"),
    ("Crisi climatica e azioni necessarie.","clima|crisi|azione|governo|futuro"),
]

# ═══════════════ C1 ═══════════════
CELI["C1"]["ascolto"] = [
    ("Tavola rotonda su?","Etica ricerca|Bioetica|Deontologia|Filosofia",0,"Etica della ricerca scientifica limiti manipolazione genetica."),
    ("Posizione relatore?","Favorevole manipolazione|Contrario totale|Condizionato|Indifferente",2,"Favorevole con limiti etici molto stringenti."),
    ("Conferenza linguistica?","Lingue in via estinzione|Dialetti|Multilinguismo|Traduzione",0,"Lingue a rischio estinzione una muore ogni due settimane."),
    ("Quante lingue?","3000|5000|7000|9000",2,"7000 lingue nel mondo meta a rischio."),
    ("Dibattito economia?","Economia circolare|Decrescita|Sviluppo|Liberalizzazione",0,"Economia circolare supera modello usa e getta."),
    ("Percentuale riciclo UE?","30%|40%|50%|60%",3,"UE ricicla 60% rifiuti imballaggio."),
    ("Seminario neuroscienze?","Coscienza|Percezione|Attenzione|Memoria",0,"Studio coscienza approccio integrato cervello-mente."),
    ("Metodo usato?","fMRI|EEG|PET|TMS",0,"fMRI per mappare aree cerebrali coscienza."),
    ("Forum politiche sociali?","Reddito cittadinanza|Salario minimo|Pensioni|Sanita",1,"Salario minimo 9 euro ora divide maggioranza."),
    ("Importo proposto?","8|9|10|11",1,"Nove euro l ora."),
    ("Convegno diritto?","Diritto privacy|Dati personali|Brevetti|Antitrust",0,"Nuovo regolamento privacy europeo revisione."),
    ("Novita regolamento?","Piu tutele|Meno burocrazia|Sanzioni|Esenzioni",0,"Piu tutele per cittadini trattamento dati."),
    ("Premio letterario?","Strega|Campiello|Bancarella|Viareggio",0,"Premio Strega 2026 vinto da esordiente 28 anni."),
    ("Vincitore eta?","24|26|28|30",2,"28 anni piu giovane vincitore storia premio."),
    ("Analisi sociologica?","Nuove poverta|Working poor|Precariato|Esclusione",0,"Nuove poverta emergono classe media impoverita."),
]
CELI["C1"]["lettura"] = [
    ("Saggio filosofia?","Ermeneutica|Fenomenologia|Esistenzialismo|Ontologia",0,"Gadamer ermeneutica fusione orizzonti interpretazione testi."),
    ("Concetto principale?","Fusione orizzonti|Circolo ermeneutico|Precomprensione|Tradizione",0,"Fusione orizzonti tra interprete e testo."),
    ("Analisi economia?","Capitalismo stakeholder|Capitalismo shareholder|Capitalismo di stato|Capitalismo popolare",0,"Capitalismo stakeholder supera shareholder value."),
    ("Differenza?","Tutti stakeholder|Solo azionisti|Stato controlla|Popolo azionista",0,"Coinvolge lavoratori ambiente e comunita."),
    ("Critica letteraria?","Nuovo romanzo|Transavanguardia|Ipermoderno|Realismo",0,"Nuovo realismo letteratura italiana contemporanea."),
    ("Caratteristica?","Impegno civile|Sperimentalismo|Lirismo|Satira",0,"Impegno civile tematiche sociali."),
    ("Documento storico?","Archivi Vaticani|Processi inquisizione|Lettere diplomatiche|Manoscritti",0,"Archivi Vaticani rivelano retroscena Concilio Vaticano II."),
    ("Periodo storico?","Concilio Vaticano II|Rinascimento|Controriforma|Risorgimento",0,"Concilio Vaticano II anni '60."),
    ("Saggio psicologia?","Intelligenze multiple|EQ|Quoziente intellettivo|Creativita",0,"Gardner intelligenze multiple oltre QI."),
    ("Quante intelligenze?","5|6|7|8",3,"8 tipi intelligenza linguistica logica musicale."),
    ("Ricerca genetica?","Epigenetica|DNA|RNA|Proteine",0,"Epigenetica ambiente modifica espressione geni."),
    ("Fattori ambientali?","Dieta stress|Clima sostanze|Esercizio|Sociale",0,"Dieta e stress modificano epigenoma."),
    ("Saggio sociologia?","Societa rete|Network society|Connettivismo|Tribu digitali",0,"Castells societa rete potere flussi informazione."),
    ("Struttura sociale?","Rete|Gerarchia|Mercato|Comunita",0,"Societa organizzata in reti orizzontali."),
    ("Analisi urbanistica?","Citta smart|Citta creativa|Citta inclusiva|Citta globale",0,"Citta smart tecnologia migliora vita urbana."),
]
CELI["C1"]["grammatica"] = [
    ("Per quanto _____ (lui sforzarsi) non raggiunge obiettivo.","si sforzi"),
    ("Ove _____ (essere) necessario consulteremo esperto.","fosse"),
    ("Laddove _____ (mancare) alternative si proceda.","mancassero"),
    ("Non che _____ (io credere) ma prendiamo in considerazione.","creda"),
    ("Qualora _____ (lei decidere) di accettare ci faccia sapere.","decidesse"),
    ("A patto che tutti _____ (rispettare) le regole.","rispettino|abbiano rispettato"),
    ("Benche _____ (noi informare) per tempo non hanno agito.","li avessimo informati"),
    ("Come se _____ (bastare) quanto gia fatto ora pure questo.","bastasse"),
    ("E fondamentale che tu _____ (comprendere) il problema.","comprenda"),
    ("Avrei voluto che loro _____ (comportarsi) diversamente.","si fossero comportati"),
    ("Pur _____ (sapere) la verita ha taciuto.","sapendo"),
    ("Non e che _____ (noi opporsi) alla proposta ma...","ci opponiamo|ci opponessimo"),
    ("Fino a che non _____ (loro arrivare) non iniziamo.","arrivino|arrivano"),
    ("Anche se _____ (essere) tardi possiamo provare.","fosse"),
    ("Tale da _____ (lasciare) tutti senza parole.","lasciare"),
]
CELI["C1"]["scrittura"] = [
    ("Saggio impatto social media democrazia 120-150.","social|media|democrazia|informazione|disinformazione"),
    ("Analisi turismo sostenibile impatto ambientale 120-150.","turismo|sostenibile|impatto|ambiente|territorio"),
    ("Ruolo universita formazione critica 120-150.","universita|formazione|critica|sapere|futuro"),
    ("Patrimonio culturale identita nazionale 120-150.","patrimonio|culturale|identita|nazionale|tradizione"),
    ("Innovazione tecnologica e lavoro 120-150.","innovazione|tecnologica|lavoro|futuro|competenze"),
]
CELI["C1"]["orale"] = [
    ("Globalizzazione culturale identita.","globalizzazione|cultura|identita|diversita|tradizione"),
    ("Ruolo scienza decisioni politiche.","scienza|politica|decisioni|ricerca|evidenze"),
    ("Diritti umani e immigrazione.","diritti|umani|immigrazione|accoglienza|integrazione"),
    ("Educazione nell era digitale.","educazione|digitale|scuola|tecnologia|apprendimento"),
    ("Sostenibilita e giustizia sociale.","sostenibilita|giustizia|sociale|ambiente|equita"),
]

# ═══════════════ C2 ═══════════════
CELI["C2"]["ascolto"] = [
    ("Lezione filosofia?","Fenomenologia Husserl|Esistenzialismo|Strutturalismo|Post-strutturalismo",0,"Husserl fenomenologia come scienza rigorosa coscienza."),
    ("Concetto introdotto?","Intenzionalita|Noema Noesi|Epoché|Mondo vita",0,"Intenzionalita coscienza sempre diretta a oggetto."),
    ("Conferenza geopolitica?","Fine egemonia USA|Ascesa Cina|Nuovo bipolarismo|Multipolarismo",0,"Fine egemonia americana transizione multipolare."),
    ("Ordine mondiale?","Unipolare|Bipolare|Multipolare|Apolare",2,"Ordine multipolare con centri potere diversi."),
    ("Seminario bioetica?","Post-umano|Trans-umano|Cyborg|Miglioramento genetico",0,"Post-umano superamento limiti biologici."),
    ("Questione centrale?","Identita umana|Etica potenziamento|Dignita|Natura",0,"Cosa significa essere umani dopo potenziamento."),
    ("Dibattito storiografico?","Microstoria|Storia globale|Storia concettuale|Storia culturale",1,"Storia globale supera approccio eurocentrico."),
    ("Approccio criticato?","Eurocentrismo|Nazionalismo|Occidentalismo|Imperialismo",0,"Eurocentrismo nella narrazione storica."),
    ("Convegno linguistica?","Pragmatica|Semantica|Sintassi|Fonetica",0,"Pragmatica linguaggio atti linguistici indiretti."),
    ("Teorico?","Austin|Searle|Grice|Habermas",2,"Grice massime conversazionali implicature."),
    ("Economia politica?","Decrescita felice|Post-crescita|Stato stazionario|Nuovo paradigma",0,"Decrescita felice Latouche alternativa sviluppo."),
    ("Teorico riferimento?","Latouche|Jackson|Piketty|Stiglitz",0,"Latouche decrescita serena."),
    ("Analisi sociologica?","Società rischio|Modernità riflessiva|Individualizzazione|Globalizzazione",0,"Beck societa del rischio incertezza globale."),
    ("Concetto chiave?","Rischio globale|Incertezza|Modernizzazione|Riflessivita",0,"Rischio globale caratterizza modernita avanzata."),
    ("Critica arte?","Arte concettuale|Arte relazionale|Estetica relazionale|Post-arte",0,"Arte concettuale idea prevale oggetto realizzazione."),
]
CELI["C2"]["lettura"] = [
    ("Saggio Adorno?","Industria culturale|Dialettica illuminismo|Ragione strumentale|Minima moralia",0,"Industria culturale merce cultura standardizzata intrattenimento."),
    ("Concetto critico?","Standardizzazione|Mercefazione|Passivita|Consumo",0,"Cultura diventa merce standardizzata per masse."),
    ("Filosofia Arendt?","Banalita male|Vita activa|Totalitarismo|Spazio pubblico",0,"Banalita del male Eichmann uomo comune burocrate."),
    ("Concetto male?","Burocrazia|Ideologia|Obbedienza|Conformismo",0,"Male commesso per conformismo non malvagita."),
    ("Saggio Bourdieu?","Capitale culturale|Capitale sociale|Habitus|Campo",0,"Capitale culturale riproduce disuguaglianze sociali scuola."),
    ("Riproduzione?","Scuola|Famiglia|Lavoro|Media",0,"Scuola riproduce capitale culturale classi dominanti."),
    ("Testo Haraway?","Cyborg manifesto|Conoscenza situata|Ecologia saperi|Femminismo",0,"Cyborg identita ibrida supera binarismi natura cultura."),
    ("Metafora cyborg?","Superamento|Ibridazione|Resistenza|Utopia",1,"Metafora per superare dualismi occidentali."),
    ("Analisi Derrida?","Decostruzione|Différance|Traccia|Supplimento",0,"Decostruzione metafisica presenza significazione infinita."),
    ("Concetto differance?","Differire|Differenza|Assenza|Traccia",0,"Différance differire senso mai pienamente presente."),
    ("Saggio Foucault?","Dispositivo sessualita|Biopotere|Governamentalita|Cura di se",0,"Dispositivo sessualita sapere potere controllo corpi."),
    ("Tecnica potere?","Controllo|Sorveglianza|Disciplina|Confessione",3,"Confessione tecnica produzione verita sessualita."),
    ("Etica Levinas?","Altro|Volto|Responsabilita|Infinito",0,"Etica come filosofia prima responsabilita per l Altro."),
    ("Concetto volto?","Relazione|Appello|Responsabilita|Esposizione",2,"Volto dell Altro chiama a responsabilita infinita."),
    ("Saggio Cacciari?","Europa|Nomos|Krisis|Metafisica",0,"Europa tramonto idea politica nichilismo compiuto."),
]
CELI["C2"]["grammatica"] = [
    ("Non che _____ (noi sottovalutare) il problema ma...","sottovalutiamo|sottovalutassimo"),
    ("Ove mai si _____ (presentare) occasione coglietela.","presentasse"),
    ("Per quanto si _____ (cercare) non si trova soluzione.","cerchi|cercasse"),
    ("Laddove _____ (noi trovarci) in difficolta chiediamo aiuto.","ci trovassimo"),
    ("Quand anche _____ (lui negare) le prove sono evidenti.","neghi"),
    ("Come se non _____ (bastare) i guai passati.","bastassero"),
    ("Fosse _____ (loro andare) via prima non succedeva.","andati|andate"),
    ("Pur _____ (avere) prove schiaccianti non ha convinto.","avendo"),
    ("Trattandosi di questione delicata _____ (noi procedere) con cautela.","procediamo"),
    ("Al punto che nessuno _____ (poter) piu distinguere vero da falso.","puo|potrebbe"),
    ("In modo che tutti _____ (comprendere) la complessita.","comprendano|comprendessero"),
    ("Tale da _____ (mettere) in discussione tutto sistema.","mettere"),
    ("Per il solo fatto che _____ (tu opporsi) hanno deciso diversamente.","ti opponi|ti sia opposto"),
    ("Se non che _____ (lui rivelare) la verita all improvviso.","ha rivelato"),
    ("Non gia che _____ (io dubitare) della buona fede.","dubiti|dubitassi"),
]
CELI["C2"]["scrittura"] = [
    ("Saggio critico su concetto identita nell era globale 150-180.","identita|globale|cultura|meticciato|dialogo"),
    ("Etica e responsabilita generazioni future 150-180.","etica|responsabilita|generazioni|futuro|sostenibilita"),
    ("Crisi della democrazia contemporanea 150-180.","crisi|democrazia|partecipazione|rappresentanza|sovranita"),
    ("Ruolo filosofia nella societa tecnologica 150-180.","filosofia|tecnologia|societa|pensiero|umanesimo"),
    ("Memoria storia e riconciliazione 150-180.","memoria|storia|riconciliazione|passato|futuro"),
]
CELI["C2"]["orale"] = [
    ("Superamento antropocentrismo etica ambientale.","antropocentrismo|etica|ambiente|natura|specismo"),
    ("Concetto verita nell epistemologia contemporanea.","verita|epistemologia|conoscenza|scienza|interpretazione"),
    ("Giustizia distributiva e disuguaglianze globali.","giustizia|distributiva|disuguaglianza|globale|equita"),
    ("Rapporto tecnica e destino umano.","tecnica|destino|umano|heidegger|liberta"),
    ("Pluralismo culturale e universale dei diritti.","pluralismo|culturale|universale|diritti|differenza"),
]

print(f"CELI data loaded: {sum(len(CELI[lv]['ascolto'])+len(CELI[lv]['lettura'])+len(CELI[lv]['grammatica'])+len(CELI[lv]['scrittura'])+len(CELI[lv]['orale']) for lv in LEVELS)} questions")
