#!/usr/bin/env python3

"""Generate interactive CILS/CELI exam HTML pages with base64 audio"""

import os, json, re
import base64



REPO_DIR = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"



# ═══════════════════════════════════════════════════════════════

# EXAMS DATA — define all 36 exam records (6 sets × 6 levels)

# Each record: exam_type, level, set, sections[], items[]

# ═══════════════════════════════════════════════════════════════

EXAMS = {}

EXAMS["CELI1_A1"] = {
  "title": "CELI CELI1 Impatto (A1)",
  "exam_type": "CELI",
  "set": "CELI1",
  "level": "A1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa fa il signor Rossi nel weekend?",
          "opts": [
            "Gioca a calcio",
            "Va a pesca",
            "Va al cinema"
          ],
          "ans": 1,
          "script": "Il sabato il signor Rossi va sempre a pesca con suo figlio. La domenica invece legge il giornale e si prende cura del suo giardino."
        },
        {
          "type": "listen_choice",
          "q": "Dov'è la biblioteca?",
          "opts": [
            "In piazza centrale",
            "In via Garibaldi",
            "All'università"
          ],
          "ans": 1,
          "script": "La biblioteca comunale è in via Garibaldi, di fronte al parco. È aperta dal lunedì al venerdì dalle nove alle diciannove."
        },
        {
          "type": "listen_choice",
          "q": "Cosa mangia a pranzo?",
          "opts": [
            "Pasta",
            "Un'insalata con pollo",
            "Pizza"
          ],
          "ans": 1,
          "script": "Di solito a pranzo mangio un'insalata con pollo e pomodori. Qualche volta prendo anche un gelato per dessert."
        },
        {
          "type": "listen_choice",
          "q": "Perché Luca è triste?",
          "opts": [
            "Ha perso il lavoro",
            "Il suo cane è malato",
            "Ha litigato"
          ],
          "ans": 1,
          "script": "Luca è triste perché il suo cane è malato. Domani lo porterà dal veterinario per una visita approfondita."
        },
        {
          "type": "listen_choice",
          "q": "Che tempo farà?",
          "opts": [
            "Pioverà",
            "Farà bello",
            "Nevicherà"
          ],
          "ans": 1,
          "script": "Le previsioni dicono che domani farà bello con temperature intorno ai venticinque gradi. Una giornata perfetta per una gita."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Dove abita Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli con la mia famiglia. Studio medicina all'università e nel tempo libero suono la chitarra. Mi piace molto la pizza e il mare.",
          "opts": [
            "A Napoli",
            "A Roma",
            "A Milano"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa studia Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina all'università e nel tempo libero suono la chitarra.",
          "opts": [
            "Medicina",
            "Ingegneria",
            "Economia"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa piace a Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina e nel tempo libero suono la chitarra. Mi piace molto la pizza.",
          "opts": [
            "La pizza",
            "La pasta",
            "Il pesce"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Io ___ (essere) italiano.",
          "hint": "presente",
          "ans": "sono"
        },
        {
          "type": "fill",
          "q": "Loro ___ (avere) due cani.",
          "hint": "presente",
          "ans": "hanno"
        },
        {
          "type": "fill",
          "q": "Tu ___ (andare) a scuola in autobus.",
          "hint": "presente",
          "ans": "vai"
        },
        {
          "type": "fill",
          "q": "Noi ___ (parlare) italiano.",
          "hint": "presente",
          "ans": "parliamo"
        },
        {
          "type": "fill",
          "q": "Maria ___ (leggere) un libro.",
          "hint": "presente",
          "ans": "legge"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una breve email per presentarti a un nuovo amico italiano. Parla del tuo nome, della tua età, della tua città e dei tuoi hobby. (50-80 parole)",
          "keywords": [
            "mi chiamo",
            "anni",
            "abito",
            "mi piace",
            "hobby"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla della tua giornata tipica. Descrivi cosa fai dalla mattina alla sera (sveglia, colazione, lavoro/studio, pranzo, tempo libero, cena).",
          "keywords": [
            "sveglia",
            "colazione",
            "lavoro",
            "studio",
            "pranzo",
            "cena"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI1_A2"] = {
  "title": "CELI CELI1 1 (A2)",
  "exam_type": "CELI",
  "set": "CELI1",
  "level": "A2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Perché Maria non è venuta?",
          "opts": [
            "Era stanca",
            "Ha lavorato fino a tardi",
            "Era malata"
          ],
          "ans": 1,
          "script": "Maria non è venuta alla festa perché ha dovuto lavorare fino a tardi. Stava finendo un progetto importante per un cliente internazionale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa hanno visitato a Roma?",
          "opts": [
            "Solo il Colosseo",
            "Musei e monumenti",
            "Negozi"
          ],
          "ans": 1,
          "script": "Durante il viaggio a Roma hanno visitato il Colosseo, i Musei Vaticani e la Fontana di Trevi. Sono stati tre giorni molto intensi."
        },
        {
          "type": "listen_choice",
          "q": "Dove ha studiato italiano?",
          "opts": [
            "A Siena",
            "A Roma",
            "A Milano"
          ],
          "ans": 0,
          "script": "Ho studiato italiano all'università per due anni. Poi ho frequentato un corso intensivo a Siena per un mese durante l'estate."
        },
        {
          "type": "listen_choice",
          "q": "Cosa regala a Natale?",
          "opts": [
            "Un viaggio a Parigi",
            "Un libro",
            "Un profumo"
          ],
          "ans": 0,
          "script": "Quest'anno per Natale regalo ai miei genitori un viaggio a Parigi. L'anno scorso avevo regalato una cena in un ristorante stellato."
        },
        {
          "type": "listen_choice",
          "q": "Com'era l'appartamento?",
          "opts": [
            "Grande e scuro",
            "Piccolo ma luminoso",
            "Vecchio e rumoroso"
          ],
          "ans": 1,
          "script": "L'appartamento che ho visitato era piccolo ma luminoso. Aveva due camere da letto, un soggiorno spazioso e una cucina moderna."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tempo fa al nord?",
          "text": "Le previsioni del tempo per domani: al nord nuvoloso con possibili piogge, temperature tra 8 e 15 gradi. Al centro sereno con qualche nuvola, 12-20 gradi. Al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "Nuvoloso",
            "Sereno",
            "Soleggiato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti gradi al sud?",
          "text": "Le previsioni del tempo per domani: al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "18-28",
            "12-20",
            "8-15"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Dov'è sereno?",
          "text": "Le previsioni del tempo per domani: al centro sereno con qualche nuvola, 12-20 gradi.",
          "opts": [
            "Al centro",
            "Al nord",
            "Al sud"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Ieri io ___ (andare) al mare.",
          "hint": "passato prossimo",
          "ans": "sono andato"
        },
        {
          "type": "fill",
          "q": "Loro ___ (finire) il lavoro.",
          "hint": "passato prossimo",
          "ans": "hanno finito"
        },
        {
          "type": "fill",
          "q": "Noi ___ (vedere) un bel film.",
          "hint": "passato prossimo",
          "ans": "abbiamo visto"
        },
        {
          "type": "fill",
          "q": "Tu ___ (comprare) il pane?",
          "hint": "passato prossimo",
          "ans": "hai comprato"
        },
        {
          "type": "fill",
          "q": "Maria ___ (arrivare) ieri sera.",
          "hint": "passato prossimo",
          "ans": "è arrivata"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una email a un albergo per prenotare una camera doppia per tre notti. Chiedi informazioni sul prezzo, sulla colazione e sul parcheggio.",
          "keywords": [
            "prenotare",
            "camera",
            "notte",
            "prezzo",
            "colazione",
            "parcheggio"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Descrivi la tua casa o il tuo appartamento. Quante stanze ci sono? Com'è la tua camera? Cosa c'è nel soggiorno? Ti piace la tua casa? Perché?",
          "keywords": [
            "casa",
            "appartamento",
            "stanza",
            "camera",
            "soggiorno",
            "cucina",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI1_B1"] = {
  "title": "CELI CELI1 2 (B1)",
  "exam_type": "CELI",
  "set": "CELI1",
  "level": "B1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa ha proposto l'associazione?",
          "opts": [
            "Un mercato settimanale",
            "Una festa",
            "Un concorso"
          ],
          "ans": 0,
          "script": "Il presidente dell'associazione ha proposto di organizzare un mercato settimanale dei prodotti locali nella piazza principale del paese."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha assegnato la professoressa?",
          "opts": [
            "Un esame",
            "Una ricerca",
            "Un progetto"
          ],
          "ans": 1,
          "script": "La professoressa di storia ci ha assegnato una ricerca sulla Seconda Guerra Mondiale da consegnare entro la fine del mese prossimo."
        },
        {
          "type": "listen_choice",
          "q": "Cosa dice la recensione?",
          "opts": [
            "Il ristorante è buono",
            "Il ristorante è caro",
            "Il servizio è lento"
          ],
          "ans": 0,
          "script": "Il ristorante ha ricevuto una recensione positiva sul giornale locale per la qualità dei suoi piatti tipici della cucina toscana."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha inaugurato la palestra?",
          "opts": [
            "Una nuova area yoga",
            "Una piscina",
            "Un campo da tennis"
          ],
          "ans": 0,
          "script": "La palestra in centro ha inaugurato una nuova area dedicata allo yoga e al pilates con istruttori qualificati e attrezzature moderne."
        },
        {
          "type": "listen_choice",
          "q": "Cosa è successo ieri sera?",
          "opts": [
            "Un incendio",
            "Un furto",
            "Un incidente"
          ],
          "ans": 0,
          "script": "I vigili del fuoco sono intervenuti ieri sera per spegnere un incendio scoppiato in un appartamento al terzo piano di via Roma."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tipo di lavoro offre?",
          "text": "Cerchiamo un/una cameriere/a per il nostro ristorante in centro. Richiesta esperienza di almeno un anno, conoscenza base dell'inglese, disponibilità serale e nei weekend. Offriamo contratto a tempo determinato di 6 mesi con possibilità di rinnovo. Orario: 18:00-23:00. Inviare CV a lavoro@ristorante.it",
          "opts": [
            "Cameriere/a",
            "Cuoco/a",
            "Barista"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanto dura il contratto?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Richiesta esperienza di almeno un anno. Contratto 6 mesi rinnovabile.",
          "opts": [
            "6 mesi",
            "1 anno",
            "3 mesi"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Qual è l'orario di lavoro?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Offriamo contratto a tempo determinato con possibilità di rinnovo. Orario: 18:00-23:00.",
          "opts": [
            "18:00-23:00",
            "08:00-14:00",
            "12:00-18:00"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Se avessi soldi, ___ (comprare) una casa.",
          "hint": "condizionale",
          "ans": "comprerei"
        },
        {
          "type": "fill",
          "q": "Penso che lui ___ (arrivare) domani.",
          "hint": "congiuntivo presente",
          "ans": "arrivi"
        },
        {
          "type": "fill",
          "q": "Spero che voi ___ (potere) venire.",
          "hint": "congiuntivo presente",
          "ans": "possiate"
        },
        {
          "type": "fill",
          "q": "Prima di ___ (uscire), chiudi la porta.",
          "hint": "infinito",
          "ans": "uscire"
        },
        {
          "type": "fill",
          "q": "Mentre ___ (mangiare), guardava la TV.",
          "hint": "imperfetto",
          "ans": "mangiava"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi un testo di circa 100 parole in cui descrivi la tua routine quotidiana. Parla del lavoro/studio, dei pasti, del tempo libero e dei tuoi hobby.",
          "keywords": [
            "ogni",
            "mattina",
            "lavoro",
            "studio",
            "pomeriggio",
            "sera",
            "tempo libero"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla del tuo lavoro o dei tuoi studi. Cosa fai esattamente? Da quanto tempo? Cosa ti piace di più del tuo lavoro/studio? Quali sono le difficoltà? Cosa vorresti fare in futuro?",
          "keywords": [
            "lavoro",
            "studio",
            "colleghi",
            "progetti",
            "futuro",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI1_B2"] = {
  "title": "CELI CELI1 3 (B2)",
  "exam_type": "CELI",
  "set": "CELI1",
  "level": "B2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Di cosa parla la mostra?",
          "opts": [
            "Fotografia contemporanea",
            "Pittura rinascimentale",
            "Scultura moderna"
          ],
          "ans": 0,
          "script": "La mostra internazionale di fotografia contemporanea ospiterà opere di artisti provenienti da quindici paesi diversi."
        },
        {
          "type": "listen_choice",
          "q": "Cosa prevede il progetto urbano?",
          "opts": [
            "Piste ciclabili e aree verdi",
            "Un nuovo stadio",
            "Un centro commerciale"
          ],
          "ans": 0,
          "script": "Il progetto di riqualificazione urbana prevede la creazione di nuove piste ciclabili, aree verdi e spazi pedonali nel centro della città."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha attivato l'università?",
          "opts": [
            "Un master in IA medica",
            "Un corso di cucina",
            "Un dottorato"
          ],
          "ans": 0,
          "script": "L'università ha attivato un nuovo master in Intelligenza Artificiale applicata alla medicina, con borse di studio per studenti meritevoli."
        },
        {
          "type": "listen_choice",
          "q": "Cosa organizza la fondazione?",
          "opts": [
            "Conferenze su etica e IA",
            "Un festival musicale",
            "Un premio letterario"
          ],
          "ans": 0,
          "script": "La fondazione culturale organizza un ciclo di conferenze sul rapporto tra etica e intelligenza artificiale con relatori internazionali."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha approvato il consiglio?",
          "opts": [
            "Il bilancio previsionale",
            "Un nuovo regolamento",
            "Una tassa"
          ],
          "ans": 0,
          "script": "Il consiglio comunale ha approvato all'unanimità il bilancio che destina il quaranta per cento delle risorse all'istruzione e ai servizi sociali."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Di quanto si ridurranno le emissioni?",
          "text": "Il Ministero dell'Ambiente ha annunciato un nuovo piano per la riduzione delle emissioni di CO2 del 55% entro il 2030. Il piano prevede incentivi per l'acquisto di auto elettriche, l'ampliamento delle zone a traffico limitato e investimenti nelle energie rinnovabili. Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "55%",
            "30%",
            "40%"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa NON prevede il piano?",
          "text": "Il piano prevede incentivi per auto elettriche, ampliamento zone a traffico limitato e investimenti in energie rinnovabili.",
          "opts": [
            "Nuove autostrade",
            "Auto elettriche",
            "Zone a traffico limitato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa pensano le associazioni?",
          "text": "Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "Positivo ma vogliono di più",
            "Negativo",
            "Indifferente"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Credo che loro ___ (partire) ieri.",
          "hint": "congiuntivo passato",
          "ans": "siano partiti"
        },
        {
          "type": "fill",
          "q": "Sebbene ___ (piovere), siamo usciti.",
          "hint": "congiuntivo presente",
          "ans": "piova"
        },
        {
          "type": "fill",
          "q": "Benché ___ (essere) stanco, ha finito il lavoro.",
          "hint": "congiuntivo presente",
          "ans": "sia"
        },
        {
          "type": "fill",
          "q": "È importante che tu ___ (studiare) ogni giorno.",
          "hint": "congiuntivo presente",
          "ans": "studi"
        },
        {
          "type": "fill",
          "q": "Temo che non mi ___ (capire).",
          "hint": "congiuntivo presente",
          "ans": "capisca"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una lettera formale al sindaco della tua città per esprimere la tua opinione sulla creazione di una zona a traffico limitato (ZTL) in centro. Argomenta le tue ragioni pro o contro con almeno due argomenti. (150 parole)",
          "keywords": [
            "sindaco",
            "traffico",
            "centro",
            "inquinamento",
            "opinione",
            "argomento"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla dell'importanza della sostenibilità ambientale nella vita quotidiana. Cosa fai concretamente per ridurre il tuo impatto ambientale? Quali cambiamenti vorresti vedere nella tua città?",
          "keywords": [
            "ambiente",
            "sostenibilità",
            "riciclo",
            "energia",
            "città",
            "futuro"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI1_C1"] = {
  "title": "CELI CELI1 4 (C1)",
  "exam_type": "CELI",
  "set": "CELI1",
  "level": "C1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dov'è l'Italia nella digitalizzazione?",
          "opts": [
            "Avanzata",
            "In ritardo",
            "Nella media"
          ],
          "ans": 1,
          "script": "Il rapporto evidenzia che l'Italia è ancora indietro nella digitalizzazione della PA rispetto alla media europea, nonostante i progressi recenti."
        },
        {
          "type": "listen_choice",
          "q": "Con chi collabora il museo?",
          "opts": [
            "Col Louvre",
            "Col British Museum",
            "Col Prado"
          ],
          "ans": 0,
          "script": "La direzione del museo ha annunciato una partnership con il Louvre per lo scambio di opere e la collaborazione su progetti di restauro."
        },
        {
          "type": "listen_choice",
          "q": "Cosa preferiscono i giovani?",
          "opts": [
            "Flessibilità lavorativa",
            "Alto stipendio",
            "Carriera veloce"
          ],
          "ans": 0,
          "script": "L'indagine rivela che oltre il sessanta per cento dei giovani intervistati considera la flessibilità lavorativa più importante dello stipendio."
        },
        {
          "type": "listen_choice",
          "q": "Dov'è il nuovo centro di ricerca?",
          "opts": [
            "A Frascati",
            "A Milano",
            "A Bologna"
          ],
          "ans": 0,
          "script": "Il nuovo centro di ricerca sulla fusione nucleare inaugurato oggi a Frascati rappresenta un passo avanti nella collaborazione scientifica internazionale."
        },
        {
          "type": "listen_choice",
          "q": "Quanto sport raccomanda l'OMS?",
          "opts": [
            "150 minuti a settimana",
            "30 minuti al giorno",
            "2 ore al giorno"
          ],
          "ans": 0,
          "script": "L'OMS raccomanda almeno centocinquanta minuti di attività fisica moderata a settimana per la prevenzione di malattie cardiovascolari."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa suggerisce lo studio?",
          "text": "Uno studio pubblicato sulla rivista Nature Neuroscience suggerisce che l'apprendimento di una seconda lingua in età adulta può rallentare il declino cognitivo legato all'invecchiamento. I ricercatori hanno seguito 853 partecipanti per oltre 40 anni, scoprendo che i bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui. Il fenomeno sarebbe legato alla maggiore plasticità neuronale indotta dal bilinguismo.",
          "opts": [
            "Il bilinguismo rallenta il declino cognitivo",
            "Il bilinguismo accelera l'invecchiamento",
            "Non c'è alcun effetto"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti partecipanti allo studio?",
          "text": "I ricercatori hanno seguito 853 partecipanti per oltre 40 anni.",
          "opts": [
            "853",
            "583",
            "385"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti anni di ritardo nella demenza?",
          "text": "I bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui.",
          "opts": [
            "4,5 anni",
            "2 anni",
            "10 anni"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Qualora ___ (arrivare) in ritardo, avvisateci.",
          "hint": "congiuntivo imperfetto",
          "ans": "arrivaste"
        },
        {
          "type": "fill",
          "q": "Se lo ___ (sapere), te lo avrei detto.",
          "hint": "congiuntivo trapassato",
          "ans": "avessi saputo"
        },
        {
          "type": "fill",
          "q": "Nonostante ___ (avere) ragione, ha taciuto.",
          "hint": "congiuntivo imperfetto",
          "ans": "avesse"
        },
        {
          "type": "fill",
          "q": "Pur ___ (essere) ricco, vive modestamente.",
          "hint": "gerundio",
          "ans": "essendo"
        },
        {
          "type": "fill",
          "q": "Il libro di cui ti ___ (parlare) è interessante.",
          "hint": "trapassato prossimo",
          "ans": "avevo parlato"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Il governo propone di aumentare l'età pensionabile a 67 anni per tutti i lavoratori. Scrivi un articolo di opinione di circa 200 parole esprimendo la tua posizione, analizzando sia i vantaggi che gli svantaggi della proposta.",
          "keywords": [
            "pensione",
            "lavoro",
            "governo",
            "riforma",
            "vantaggi",
            "svantaggi",
            "futuro"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Discuti il fenomeno della globalizzazione analizzandone vantaggi e svantaggi per l'economia e la cultura locale italiana. Fornisci esempi concreti e una tua opinione personale.",
          "keywords": [
            "globalizzazione",
            "economia",
            "cultura",
            "commercio",
            "identità",
            "tradizione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI1_C2"] = {
  "title": "CELI CELI1 5 (C2)",
  "exam_type": "CELI",
  "set": "CELI1",
  "level": "C2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Di cosa ha parlato il Nobel?",
          "opts": [
            "Meccanica quantistica e coscienza",
            "Buchi neri",
            "Energia nucleare"
          ],
          "ans": 0,
          "script": "Il premio Nobel per la fisica ha tenuto una lectio magistralis sul rapporto tra meccanica quantistica e coscienza, suscitando un vivace dibattito."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha stabilito la Corte?",
          "opts": [
            "Principi sulla privacy digitale",
            "Nuove leggi",
            "Divieti"
          ],
          "ans": 0,
          "script": "La Corte Costituzionale si è pronunciata sulla legittimità delle nuove norme in materia di privacy digitale, stabilendo principi importanti per la tutela dei dati."
        },
        {
          "type": "listen_choice",
          "q": "Dov'è l'Italia nella mobilità sociale?",
          "opts": [
            "Ultime posizioni",
            "Prime posizioni",
            "A metà classifica"
          ],
          "ans": 0,
          "script": "L'indagine dell'OCSE sulla mobilità sociale colloca l'Italia nelle ultime posizioni per equità di opportunità tra generazioni."
        },
        {
          "type": "listen_choice",
          "q": "Di cosa ha discusso il festival?",
          "opts": [
            "Etica dell'editing genetico",
            "Cambiamento climatico",
            "Intelligenza artificiale"
          ],
          "ans": 0,
          "script": "Il festival della scienza ha ospitato un dibattito sulle implicazioni etiche dell'editing genetico con biologi, filosofi e giuristi."
        },
        {
          "type": "listen_choice",
          "q": "Cosa analizza Foreign Affairs?",
          "opts": [
            "La transizione multipolare",
            "La crisi economica",
            "Il riscaldamento globale"
          ],
          "ans": 0,
          "script": "L'analisi geopolitica pubblicata su Foreign Affairs esamina le conseguenze della transizione multipolare sugli equilibri di potere globali."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa ha dichiarato la Corte?",
          "text": "La recente sentenza della Corte Costituzionale n. 152/2023 ha dichiarato l'illegittimità costituzionale di alcune norme del codice degli appalti, ritenute lesive del principio di libera concorrenza sancito dall'articolo 41 della Costituzione. La decisione avrà ripercussioni significative sul settore delle costruzioni, dove le gare d'appalto dovranno essere riformulate per garantire maggiore trasparenza e pari opportunità tra i concorrenti.",
          "opts": [
            "Illegittimità di norme sugli appalti",
            "Legittimità delle norme",
            "Rinvio della decisione"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quale settore è più colpito?",
          "text": "La decisione avrà ripercussioni sul settore delle costruzioni, dove le gare dovranno essere riformulate per garantire maggiore trasparenza.",
          "opts": [
            "Costruzioni",
            "Sanità",
            "Istruzione"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Lungi dal ___ (voler) offendere, mi scuso.",
          "hint": "infinito",
          "ans": "volere"
        },
        {
          "type": "fill",
          "q": "Per quanto ___ (sforzarsi), non ce la fa.",
          "hint": "congiuntivo presente",
          "ans": "si sforzi"
        },
        {
          "type": "fill",
          "q": "Ove mai ___ (esserci) dubbi, contattateci.",
          "hint": "congiuntivo presente",
          "ans": "ci siano"
        },
        {
          "type": "fill",
          "q": "Al fine di ___ (evitare) disguidi, confermate.",
          "hint": "infinito",
          "ans": "evitare"
        },
        {
          "type": "fill",
          "q": "Il candidato ___ (ritenere) idoneo sarà contattato.",
          "hint": "participio passato",
          "ans": "ritenuto"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Analizza criticamente l'impatto dell'intelligenza artificiale sul mercato del lavoro italiano, considerando gli aspetti etici, economici e sociali. Fornisci esempi concreti e una tua valutazione personale. (300 parole)",
          "keywords": [
            "intelligenza artificiale",
            "lavoro",
            "etica",
            "economia",
            "società"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Analizza le conseguenze della digitalizzazione della pubblica amministrazione in Italia. Quali sono i rischi e i benefici per i cittadini? Considera aspetti come l'accessibilità, la privacy e l'inclusione digitale.",
          "keywords": [
            "digitalizzazione",
            "pubblica amministrazione",
            "cittadini",
            "privacy",
            "accessibilità",
            "inclusione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI2_A1"] = {
  "title": "CELI CELI2 Impatto (A1)",
  "exam_type": "CELI",
  "set": "CELI2",
  "level": "A1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dove lavora Paolo?",
          "opts": [
            "In un ristorante",
            "In un'azienda informatica",
            "In un ospedale"
          ],
          "ans": 1,
          "script": "Paolo lavora in una grande azienda informatica a Torino. Si occupa di sviluppare software per banche e uffici postali."
        },
        {
          "type": "listen_choice",
          "q": "Cosa vuole la signora?",
          "opts": [
            "Frutta e latte",
            "Pane e vino",
            "Carne e formaggio"
          ],
          "ans": 0,
          "script": "Buongiorno, vorrei un chilo di mele e mezzo chilo di pere. Anche una busta di latte intero e due yogurt alla frutta, per favore."
        },
        {
          "type": "listen_choice",
          "q": "Che ora sono le lezioni?",
          "opts": [
            "8:30-11:00",
            "8:45-11:00",
            "9:00-11:00"
          ],
          "ans": 1,
          "script": "Le lezioni di italiano cominciano alle otto e tre quarti e finiscono alle undici. La pausa è dalle dieci e un quarto alle dieci e mezza."
        },
        {
          "type": "listen_choice",
          "q": "Perché Sara è contenta?",
          "opts": [
            "Ha trovato lavoro",
            "Ha vinto una borsa di studio",
            "Ha comprato casa"
          ],
          "ans": 1,
          "script": "Sara ha ricevuto una borsa di studio per studiare arte a Firenze per un anno intero. È felicissima perché è la sua città preferita."
        },
        {
          "type": "listen_choice",
          "q": "Cosa prenota il signore?",
          "opts": [
            "Un tavolo",
            "Una camera",
            "Un biglietto"
          ],
          "ans": 1,
          "script": "Buongiorno, vorrei prenotare una camera doppia per tre notti dal quindici al diciotto agosto con colazione inclusa, per favore."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Dove abita Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli con la mia famiglia. Studio medicina all'università e nel tempo libero suono la chitarra. Mi piace molto la pizza e il mare.",
          "opts": [
            "A Napoli",
            "A Roma",
            "A Milano"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa studia Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina all'università e nel tempo libero suono la chitarra.",
          "opts": [
            "Medicina",
            "Ingegneria",
            "Economia"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa piace a Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina e nel tempo libero suono la chitarra. Mi piace molto la pizza.",
          "opts": [
            "La pizza",
            "La pasta",
            "Il pesce"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Io ___ (essere) italiano.",
          "hint": "presente",
          "ans": "sono"
        },
        {
          "type": "fill",
          "q": "Loro ___ (avere) due cani.",
          "hint": "presente",
          "ans": "hanno"
        },
        {
          "type": "fill",
          "q": "Tu ___ (andare) a scuola in autobus.",
          "hint": "presente",
          "ans": "vai"
        },
        {
          "type": "fill",
          "q": "Noi ___ (parlare) italiano.",
          "hint": "presente",
          "ans": "parliamo"
        },
        {
          "type": "fill",
          "q": "Maria ___ (leggere) un libro.",
          "hint": "presente",
          "ans": "legge"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una breve email per presentarti a un nuovo amico italiano. Parla del tuo nome, della tua età, della tua città e dei tuoi hobby. (50-80 parole)",
          "keywords": [
            "mi chiamo",
            "anni",
            "abito",
            "mi piace",
            "hobby"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla della tua giornata tipica. Descrivi cosa fai dalla mattina alla sera (sveglia, colazione, lavoro/studio, pranzo, tempo libero, cena).",
          "keywords": [
            "sveglia",
            "colazione",
            "lavoro",
            "studio",
            "pranzo",
            "cena"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI2_A2"] = {
  "title": "CELI CELI2 1 (A2)",
  "exam_type": "CELI",
  "set": "CELI2",
  "level": "A2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dov'è andato Marco in vacanza?",
          "opts": [
            "In Sardegna",
            "In Sicilia",
            "In Puglia"
          ],
          "ans": 1,
          "script": "Marco è andato in vacanza in Sicilia con la sua ragazza. Sono stati una settimana a Taormina, un paese bellissimo sul mare, e hanno visitato anche l'Etna."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha perso la ragazza?",
          "opts": [
            "Il telefono",
            "Lo zaino",
            "La borsa"
          ],
          "ans": 1,
          "script": "Mi scusi, ho perso il mio zaino grigio. Dentro c'erano il computer portatile e i libri dell'università. L'ho lasciato al bar della stazione."
        },
        {
          "type": "listen_choice",
          "q": "Che lavoro fa il signor Moretti?",
          "opts": [
            "Insegnante",
            "Giornalista",
            "Avvocato"
          ],
          "ans": 1,
          "script": "Sono il signor Moretti, faccio il giornalista da più di vent'anni. Lavoro per un importante quotidiano nazionale e seguo la cronaca estera."
        },
        {
          "type": "listen_choice",
          "q": "Cosa serve per l'esame?",
          "opts": [
            "Libri e dizionario",
            "Documento e ricevuta",
            "Computer e calcolatrice"
          ],
          "ans": 1,
          "script": "Per l'esame di certificazione dovete portare un documento d'identità valido e la ricevuta del pagamento. Non sono ammessi telefoni cellulari durante la prova."
        },
        {
          "type": "listen_choice",
          "q": "A che ora parte l'ultimo treno?",
          "opts": [
            "22:30",
            "23:00",
            "23:30"
          ],
          "ans": 2,
          "script": "L'ultimo treno per Napoli parte alle ventitré e trenta dal binario sette. Il Regionale per Salerno parte ogni ora fino a mezzanotte."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tempo fa al nord?",
          "text": "Le previsioni del tempo per domani: al nord nuvoloso con possibili piogge, temperature tra 8 e 15 gradi. Al centro sereno con qualche nuvola, 12-20 gradi. Al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "Nuvoloso",
            "Sereno",
            "Soleggiato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti gradi al sud?",
          "text": "Le previsioni del tempo per domani: al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "18-28",
            "12-20",
            "8-15"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Dov'è sereno?",
          "text": "Le previsioni del tempo per domani: al centro sereno con qualche nuvola, 12-20 gradi.",
          "opts": [
            "Al centro",
            "Al nord",
            "Al sud"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Ieri io ___ (andare) al mare.",
          "hint": "passato prossimo",
          "ans": "sono andato"
        },
        {
          "type": "fill",
          "q": "Loro ___ (finire) il lavoro.",
          "hint": "passato prossimo",
          "ans": "hanno finito"
        },
        {
          "type": "fill",
          "q": "Noi ___ (vedere) un bel film.",
          "hint": "passato prossimo",
          "ans": "abbiamo visto"
        },
        {
          "type": "fill",
          "q": "Tu ___ (comprare) il pane?",
          "hint": "passato prossimo",
          "ans": "hai comprato"
        },
        {
          "type": "fill",
          "q": "Maria ___ (arrivare) ieri sera.",
          "hint": "passato prossimo",
          "ans": "è arrivata"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una email a un albergo per prenotare una camera doppia per tre notti. Chiedi informazioni sul prezzo, sulla colazione e sul parcheggio.",
          "keywords": [
            "prenotare",
            "camera",
            "notte",
            "prezzo",
            "colazione",
            "parcheggio"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Descrivi la tua casa o il tuo appartamento. Quante stanze ci sono? Com'è la tua camera? Cosa c'è nel soggiorno? Ti piace la tua casa? Perché?",
          "keywords": [
            "casa",
            "appartamento",
            "stanza",
            "camera",
            "soggiorno",
            "cucina",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI2_B1"] = {
  "title": "CELI CELI2 2 (B1)",
  "exam_type": "CELI",
  "set": "CELI2",
  "level": "B1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa propone il sindaco?",
          "opts": [
            "Nuovi parcheggi",
            "Nuovi alberi",
            "Nuove strade"
          ],
          "ans": 1,
          "script": "Il sindaco ha annunciato che entro la fine dell'anno verranno piantati cinquemila nuovi alberi nelle aree periferiche per migliorare la qualità dell'aria e creare nuove aree verdi."
        },
        {
          "type": "listen_choice",
          "q": "Perché Marta ha cambiato università?",
          "opts": [
            "Era troppo difficile",
            "Non le piaceva il corso",
            "Era troppo lontana"
          ],
          "ans": 1,
          "script": "Marta ha cambiato università perché il corso che frequentava non corrispondeva alle sue aspettative. Ora studia Mediazione Linguistica e si trova molto meglio."
        },
        {
          "type": "listen_choice",
          "q": "Cosa pensa il dottore della dieta?",
          "opts": [
            "Mangiare meno",
            "Dieta più equilibrata",
            "Più sport"
          ],
          "ans": 1,
          "script": "Il dottore mi ha detto di seguire una dieta più equilibrata: più verdura, meno grassi e attività fisica almeno tre volte a settimana per migliorare la salute."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre l'agenzia?",
          "opts": [
            "Vacanze studio all'estero",
            "Stage lavorativi",
            "Scambi culturali"
          ],
          "ans": 0,
          "script": "L'agenzia offre corsi di lingua all'estero per studenti dai sedici ai venticinque anni. Le destinazioni includono Inghilterra, Stati Uniti, Spagna e Francia."
        },
        {
          "type": "listen_choice",
          "q": "Qual è il problema del condominio?",
          "opts": [
            "Il riscaldamento",
            "L'umidità",
            "Il rumore"
          ],
          "ans": 1,
          "script": "Durante l'assemblea condominiale i residenti hanno discusso del problema dell'umidità che danneggia i muri degli appartamenti al primo piano."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tipo di lavoro offre?",
          "text": "Cerchiamo un/una cameriere/a per il nostro ristorante in centro. Richiesta esperienza di almeno un anno, conoscenza base dell'inglese, disponibilità serale e nei weekend. Offriamo contratto a tempo determinato di 6 mesi con possibilità di rinnovo. Orario: 18:00-23:00. Inviare CV a lavoro@ristorante.it",
          "opts": [
            "Cameriere/a",
            "Cuoco/a",
            "Barista"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanto dura il contratto?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Richiesta esperienza di almeno un anno. Contratto 6 mesi rinnovabile.",
          "opts": [
            "6 mesi",
            "1 anno",
            "3 mesi"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Qual è l'orario di lavoro?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Offriamo contratto a tempo determinato con possibilità di rinnovo. Orario: 18:00-23:00.",
          "opts": [
            "18:00-23:00",
            "08:00-14:00",
            "12:00-18:00"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Se avessi soldi, ___ (comprare) una casa.",
          "hint": "condizionale",
          "ans": "comprerei"
        },
        {
          "type": "fill",
          "q": "Penso che lui ___ (arrivare) domani.",
          "hint": "congiuntivo presente",
          "ans": "arrivi"
        },
        {
          "type": "fill",
          "q": "Spero che voi ___ (potere) venire.",
          "hint": "congiuntivo presente",
          "ans": "possiate"
        },
        {
          "type": "fill",
          "q": "Prima di ___ (uscire), chiudi la porta.",
          "hint": "infinito",
          "ans": "uscire"
        },
        {
          "type": "fill",
          "q": "Mentre ___ (mangiare), guardava la TV.",
          "hint": "imperfetto",
          "ans": "mangiava"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi un testo di circa 100 parole in cui descrivi la tua routine quotidiana. Parla del lavoro/studio, dei pasti, del tempo libero e dei tuoi hobby.",
          "keywords": [
            "ogni",
            "mattina",
            "lavoro",
            "studio",
            "pomeriggio",
            "sera",
            "tempo libero"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla del tuo lavoro o dei tuoi studi. Cosa fai esattamente? Da quanto tempo? Cosa ti piace di più del tuo lavoro/studio? Quali sono le difficoltà? Cosa vorresti fare in futuro?",
          "keywords": [
            "lavoro",
            "studio",
            "colleghi",
            "progetti",
            "futuro",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI2_B2"] = {
  "title": "CELI CELI2 3 (B2)",
  "exam_type": "CELI",
  "set": "CELI2",
  "level": "B2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Di cosa si occupa la conferenza?",
          "opts": [
            "Energia nucleare",
            "Sviluppo sostenibile",
            "Innovazione digitale"
          ],
          "ans": 1,
          "script": "Benvenuti alla conferenza annuale sullo sviluppo sostenibile. Quest'anno ci concentriamo sull'economia circolare e sulle strategie per ridurre i rifiuti plastici negli oceani."
        },
        {
          "type": "listen_choice",
          "q": "Quale critica viene fatta al sistema?",
          "opts": [
            "Prezzi troppo alti",
            "Mezzi non puntuali",
            "Stazioni sporche"
          ],
          "ans": 1,
          "script": "Molti cittadini lamentano che i mezzi pubblici non sono puntuali e che le corse serali sono troppo ridotte. Il comune ha promesso di potenziare il servizio."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha scoperto la ricerca?",
          "opts": [
            "Leggere fa bene",
            "Leggere è noioso",
            "I libri costano troppo"
          ],
          "ans": 0,
          "script": "Un recente studio ha scoperto che leggere almeno trenta minuti al giorno riduce lo stress del sessantotto per cento e migliora la memoria a lungo termine."
        },
        {
          "type": "listen_choice",
          "q": "Cosa propone l'associazione?",
          "opts": [
            "Visite guidate gratuite",
            "Corsi d'arte",
            "Mostre temporanee"
          ],
          "ans": 0,
          "script": "L'associazione culturale 'Arte per Tutti' organizza visite guidate gratuite ai musei della città ogni prima domenica del mese, senza necessità di prenotazione."
        },
        {
          "type": "listen_choice",
          "q": "Qual è il problema principale?",
          "opts": [
            "L'inquinamento",
            "Il traffico",
            "Il rumore"
          ],
          "ans": 1,
          "script": "Il problema principale della nostra città rimane il traffico nelle ore di punta. Il comune sta valutando l'introduzione di un pedaggio per l'accesso al centro storico."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Di quanto si ridurranno le emissioni?",
          "text": "Il Ministero dell'Ambiente ha annunciato un nuovo piano per la riduzione delle emissioni di CO2 del 55% entro il 2030. Il piano prevede incentivi per l'acquisto di auto elettriche, l'ampliamento delle zone a traffico limitato e investimenti nelle energie rinnovabili. Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "55%",
            "30%",
            "40%"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa NON prevede il piano?",
          "text": "Il piano prevede incentivi per auto elettriche, ampliamento zone a traffico limitato e investimenti in energie rinnovabili.",
          "opts": [
            "Nuove autostrade",
            "Auto elettriche",
            "Zone a traffico limitato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa pensano le associazioni?",
          "text": "Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "Positivo ma vogliono di più",
            "Negativo",
            "Indifferente"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Credo che loro ___ (partire) ieri.",
          "hint": "congiuntivo passato",
          "ans": "siano partiti"
        },
        {
          "type": "fill",
          "q": "Sebbene ___ (piovere), siamo usciti.",
          "hint": "congiuntivo presente",
          "ans": "piova"
        },
        {
          "type": "fill",
          "q": "Benché ___ (essere) stanco, ha finito il lavoro.",
          "hint": "congiuntivo presente",
          "ans": "sia"
        },
        {
          "type": "fill",
          "q": "È importante che tu ___ (studiare) ogni giorno.",
          "hint": "congiuntivo presente",
          "ans": "studi"
        },
        {
          "type": "fill",
          "q": "Temo che non mi ___ (capire).",
          "hint": "congiuntivo presente",
          "ans": "capisca"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una lettera formale al sindaco della tua città per esprimere la tua opinione sulla creazione di una zona a traffico limitato (ZTL) in centro. Argomenta le tue ragioni pro o contro con almeno due argomenti. (150 parole)",
          "keywords": [
            "sindaco",
            "traffico",
            "centro",
            "inquinamento",
            "opinione",
            "argomento"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla dell'importanza della sostenibilità ambientale nella vita quotidiana. Cosa fai concretamente per ridurre il tuo impatto ambientale? Quali cambiamenti vorresti vedere nella tua città?",
          "keywords": [
            "ambiente",
            "sostenibilità",
            "riciclo",
            "energia",
            "città",
            "futuro"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI2_C1"] = {
  "title": "CELI CELI2 4 (C1)",
  "exam_type": "CELI",
  "set": "CELI2",
  "level": "C1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Quale iniziativa viene discussa?",
          "opts": [
            "Nuova metropolitana",
            "Mobilità sostenibile",
            "Pedaggi autostradali"
          ],
          "ans": 1,
          "script": "La regione ha presentato il nuovo piano per la mobilità sostenibile che prevede l'estensione della rete ciclabile e l'introduzione di bus elettrici, con un investimento di 45 milioni di euro."
        },
        {
          "type": "listen_choice",
          "q": "Quale critica viene sollevata?",
          "opts": [
            "Disparità nord-sud",
            "Mancanza di medici",
            "Ospedali vecchi"
          ],
          "ans": 0,
          "script": "Nonostante i progressi, il rapporto segnala significative disparità tra nord e sud nell'accesso ai servizi sanitari. Le regioni meridionali registrano tempi d'attesa più lunghi."
        },
        {
          "type": "listen_choice",
          "q": "Cosa propone lo psicologo?",
          "opts": [
            "Meno ore di lavoro",
            "Pause obbligatorie",
            "Più ferie"
          ],
          "ans": 1,
          "script": "La psicologa del lavoro suggerisce pause obbligatorie di quindici minuti ogni due ore di lavoro al computer per prevenire affaticamento e aumentare la produttività."
        },
        {
          "type": "listen_choice",
          "q": "Perché l'artista è controverso?",
          "opts": [
            "Usa materiali costosi",
            "Opera provocatoria",
            "È troppo giovane"
          ],
          "ans": 1,
          "script": "Il giovane artista siciliano ha suscitato un acceso dibattito con la sua ultima opera che critica il consumismo attraverso l'utilizzo di rifiuti industriali."
        },
        {
          "type": "listen_choice",
          "q": "Cosa succederà dal prossimo anno?",
          "opts": [
            "Nuove tasse",
            "Nuovo sistema esami",
            "Più corsi online"
          ],
          "ans": 1,
          "script": "A partire dal prossimo anno accademico, l'università introdurrà un nuovo sistema di valutazione con esami scritti al computer e prove orali registrate."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa suggerisce lo studio?",
          "text": "Uno studio pubblicato sulla rivista Nature Neuroscience suggerisce che l'apprendimento di una seconda lingua in età adulta può rallentare il declino cognitivo legato all'invecchiamento. I ricercatori hanno seguito 853 partecipanti per oltre 40 anni, scoprendo che i bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui. Il fenomeno sarebbe legato alla maggiore plasticità neuronale indotta dal bilinguismo.",
          "opts": [
            "Il bilinguismo rallenta il declino cognitivo",
            "Il bilinguismo accelera l'invecchiamento",
            "Non c'è alcun effetto"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti partecipanti allo studio?",
          "text": "I ricercatori hanno seguito 853 partecipanti per oltre 40 anni.",
          "opts": [
            "853",
            "583",
            "385"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti anni di ritardo nella demenza?",
          "text": "I bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui.",
          "opts": [
            "4,5 anni",
            "2 anni",
            "10 anni"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Qualora ___ (arrivare) in ritardo, avvisateci.",
          "hint": "congiuntivo imperfetto",
          "ans": "arrivaste"
        },
        {
          "type": "fill",
          "q": "Se lo ___ (sapere), te lo avrei detto.",
          "hint": "congiuntivo trapassato",
          "ans": "avessi saputo"
        },
        {
          "type": "fill",
          "q": "Nonostante ___ (avere) ragione, ha taciuto.",
          "hint": "congiuntivo imperfetto",
          "ans": "avesse"
        },
        {
          "type": "fill",
          "q": "Pur ___ (essere) ricco, vive modestamente.",
          "hint": "gerundio",
          "ans": "essendo"
        },
        {
          "type": "fill",
          "q": "Il libro di cui ti ___ (parlare) è interessante.",
          "hint": "trapassato prossimo",
          "ans": "avevo parlato"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Il governo propone di aumentare l'età pensionabile a 67 anni per tutti i lavoratori. Scrivi un articolo di opinione di circa 200 parole esprimendo la tua posizione, analizzando sia i vantaggi che gli svantaggi della proposta.",
          "keywords": [
            "pensione",
            "lavoro",
            "governo",
            "riforma",
            "vantaggi",
            "svantaggi",
            "futuro"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Discuti il fenomeno della globalizzazione analizzandone vantaggi e svantaggi per l'economia e la cultura locale italiana. Fornisci esempi concreti e una tua opinione personale.",
          "keywords": [
            "globalizzazione",
            "economia",
            "cultura",
            "commercio",
            "identità",
            "tradizione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI2_C2"] = {
  "title": "CELI CELI2 5 (C2)",
  "exam_type": "CELI",
  "set": "CELI2",
  "level": "C2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Quale tesi sostiene il linguista?",
          "opts": [
            "L'italiano si impoverisce",
            "La lingua si evolve",
            "I dialetti scompaiono"
          ],
          "ans": 1,
          "script": "Il professor Marchesi sostiene che l'evoluzione dell'italiano contemporaneo non rappresenta un impoverimento ma una naturale trasformazione linguistica."
        },
        {
          "type": "listen_choice",
          "q": "Quale critica muove al sistema?",
          "opts": [
            "Mancanza di giudici",
            "Processi troppo lunghi",
            "Poche sentenze"
          ],
          "ans": 1,
          "script": "Il presidente della Corte Suprema ha denunciato la lentezza della giustizia italiana, definendola una piaga che mina la fiducia dei cittadini nello Stato."
        },
        {
          "type": "listen_choice",
          "q": "Cosa emerge dallo studio?",
          "opts": [
            "I giovani non vogliono lavorare",
            "Priorità alla qualità della vita",
            "Tutti vogliono carriera"
          ],
          "ans": 1,
          "script": "La ricerca rivela che il settanta per cento dei giovani tra diciotto e trent'anni privilegia la qualità della vita rispetto alla carriera."
        },
        {
          "type": "listen_choice",
          "q": "Cosa si propone per il turismo?",
          "opts": [
            "Più voli low-cost",
            "Destagionalizzazione",
            "Meno turisti"
          ],
          "ans": 1,
          "script": "Il nuovo piano strategico per il turismo punta sulla destagionalizzazione e sulla promozione dei borghi meno conosciuti."
        },
        {
          "type": "listen_choice",
          "q": "Qual è la posizione del filosofo?",
          "opts": [
            "L'IA va potenziata",
            "L'IA ha bisogno di etica",
            "L'IA va vietata"
          ],
          "ans": 1,
          "script": "Il filosofo ha espresso una posizione critica sull'intelligenza artificiale, avvertendo che lo sviluppo senza regolamentazione etica rischia di delegare il pensiero critico alle macchine."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa ha dichiarato la Corte?",
          "text": "La recente sentenza della Corte Costituzionale n. 152/2023 ha dichiarato l'illegittimità costituzionale di alcune norme del codice degli appalti, ritenute lesive del principio di libera concorrenza sancito dall'articolo 41 della Costituzione. La decisione avrà ripercussioni significative sul settore delle costruzioni, dove le gare d'appalto dovranno essere riformulate per garantire maggiore trasparenza e pari opportunità tra i concorrenti.",
          "opts": [
            "Illegittimità di norme sugli appalti",
            "Legittimità delle norme",
            "Rinvio della decisione"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quale settore è più colpito?",
          "text": "La decisione avrà ripercussioni sul settore delle costruzioni, dove le gare dovranno essere riformulate per garantire maggiore trasparenza.",
          "opts": [
            "Costruzioni",
            "Sanità",
            "Istruzione"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Lungi dal ___ (voler) offendere, mi scuso.",
          "hint": "infinito",
          "ans": "volere"
        },
        {
          "type": "fill",
          "q": "Per quanto ___ (sforzarsi), non ce la fa.",
          "hint": "congiuntivo presente",
          "ans": "si sforzi"
        },
        {
          "type": "fill",
          "q": "Ove mai ___ (esserci) dubbi, contattateci.",
          "hint": "congiuntivo presente",
          "ans": "ci siano"
        },
        {
          "type": "fill",
          "q": "Al fine di ___ (evitare) disguidi, confermate.",
          "hint": "infinito",
          "ans": "evitare"
        },
        {
          "type": "fill",
          "q": "Il candidato ___ (ritenere) idoneo sarà contattato.",
          "hint": "participio passato",
          "ans": "ritenuto"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Analizza criticamente l'impatto dell'intelligenza artificiale sul mercato del lavoro italiano, considerando gli aspetti etici, economici e sociali. Fornisci esempi concreti e una tua valutazione personale. (300 parole)",
          "keywords": [
            "intelligenza artificiale",
            "lavoro",
            "etica",
            "economia",
            "società"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Analizza le conseguenze della digitalizzazione della pubblica amministrazione in Italia. Quali sono i rischi e i benefici per i cittadini? Considera aspetti come l'accessibilità, la privacy e l'inclusione digitale.",
          "keywords": [
            "digitalizzazione",
            "pubblica amministrazione",
            "cittadini",
            "privacy",
            "accessibilità",
            "inclusione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI3_A1"] = {
  "title": "CELI CELI3 Impatto (A1)",
  "exam_type": "CELI",
  "set": "CELI3",
  "level": "A1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa fa Francesca la sera?",
          "opts": [
            "Guarda la TV",
            "Fa yoga",
            "Esce con amici"
          ],
          "ans": 1,
          "script": "Francesca frequenta un corso di yoga tre sere a settimana. Dice che dopo le lezioni si sente molto più rilassata e dorme meglio."
        },
        {
          "type": "listen_choice",
          "q": "Dove va Mario in vacanza?",
          "opts": [
            "In montagna",
            "Al mare in Sardegna",
            "In città d'arte"
          ],
          "ans": 1,
          "script": "Quest'anno Mario va al mare in Sardegna con la famiglia. Rimangono due settimane a luglio in un piccolo paese vicino a Cagliari."
        },
        {
          "type": "listen_choice",
          "q": "Quanto costa il biglietto?",
          "opts": [
            "25 euro",
            "30 euro",
            "40 euro"
          ],
          "ans": 1,
          "script": "Il biglietto per il concerto costa trenta euro online o trentacinque euro alla cassa. I ragazzi sotto i quattordici anni pagano la metà."
        },
        {
          "type": "listen_choice",
          "q": "Che regalo compra Anna?",
          "opts": [
            "Un libro",
            "Una sciarpa",
            "Un profumo"
          ],
          "ans": 1,
          "script": "Anna compra per il compleanno della mamma una sciarpa di seta rossa e una scatola di cioccolatini artigianali."
        },
        {
          "type": "listen_choice",
          "q": "A che ora apre il supermercato?",
          "opts": [
            "8:00",
            "8:30",
            "9:00"
          ],
          "ans": 1,
          "script": "Il supermercato apre alle otto e mezza la mattina e chiude alle otto di sera. La domenica è aperto solo la mattina dalle nove alle tredici."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Dove abita Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli con la mia famiglia. Studio medicina all'università e nel tempo libero suono la chitarra. Mi piace molto la pizza e il mare.",
          "opts": [
            "A Napoli",
            "A Roma",
            "A Milano"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa studia Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina all'università e nel tempo libero suono la chitarra.",
          "opts": [
            "Medicina",
            "Ingegneria",
            "Economia"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa piace a Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina e nel tempo libero suono la chitarra. Mi piace molto la pizza.",
          "opts": [
            "La pizza",
            "La pasta",
            "Il pesce"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Io ___ (essere) italiano.",
          "hint": "presente",
          "ans": "sono"
        },
        {
          "type": "fill",
          "q": "Loro ___ (avere) due cani.",
          "hint": "presente",
          "ans": "hanno"
        },
        {
          "type": "fill",
          "q": "Tu ___ (andare) a scuola in autobus.",
          "hint": "presente",
          "ans": "vai"
        },
        {
          "type": "fill",
          "q": "Noi ___ (parlare) italiano.",
          "hint": "presente",
          "ans": "parliamo"
        },
        {
          "type": "fill",
          "q": "Maria ___ (leggere) un libro.",
          "hint": "presente",
          "ans": "legge"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una breve email per presentarti a un nuovo amico italiano. Parla del tuo nome, della tua età, della tua città e dei tuoi hobby. (50-80 parole)",
          "keywords": [
            "mi chiamo",
            "anni",
            "abito",
            "mi piace",
            "hobby"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla della tua giornata tipica. Descrivi cosa fai dalla mattina alla sera (sveglia, colazione, lavoro/studio, pranzo, tempo libero, cena).",
          "keywords": [
            "sveglia",
            "colazione",
            "lavoro",
            "studio",
            "pranzo",
            "cena"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI3_A2"] = {
  "title": "CELI CELI3 1 (A2)",
  "exam_type": "CELI",
  "set": "CELI3",
  "level": "A2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dove ha cenato ieri sera?",
          "opts": [
            "A casa",
            "In un ristorante giapponese",
            "In mensa"
          ],
          "ans": 1,
          "script": "Ieri sera ho cenato in un ristorante giapponese con i colleghi di lavoro. Abbiamo mangiato sushi e bevuto tè verde. Il conto era quaranta euro a testa."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha comprato Lucia?",
          "opts": [
            "Un vestito",
            "Una borsa",
            "Un paio di scarpe"
          ],
          "ans": 0,
          "script": "Lucia ha comprato un vestito nuovo per la festa di compleanno della sorella. Era in saldo e costava solo trentacinque euro, un vero affare."
        },
        {
          "type": "listen_choice",
          "q": "Com'è andato l'esame?",
          "opts": [
            "Male",
            "Bene",
            "Così così"
          ],
          "ans": 1,
          "script": "L'esame di guida è andato bene. Ho sbagliato solo il parcheggio laterale, ma l'istruttore ha detto che sono migliorato molto rispetto all'ultima volta."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha detto il medico?",
          "opts": [
            "Sto bene",
            "Devo riposare",
            "Devo operarmi"
          ],
          "ans": 1,
          "script": "Il medico ha detto che devo riposare almeno tre giorni perché ho l'influenza. Mi ha prescritto delle medicine e molta acqua."
        },
        {
          "type": "listen_choice",
          "q": "Quanto hanno aspettato?",
          "opts": [
            "20 minuti",
            "30 minuti",
            "40 minuti"
          ],
          "ans": 2,
          "script": "Hanno aspettato il treno per più di mezz'ora alla stazione centrale. Poi il treno è arrivato con venticinque minuti di ritardo a causa di un guasto."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tempo fa al nord?",
          "text": "Le previsioni del tempo per domani: al nord nuvoloso con possibili piogge, temperature tra 8 e 15 gradi. Al centro sereno con qualche nuvola, 12-20 gradi. Al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "Nuvoloso",
            "Sereno",
            "Soleggiato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti gradi al sud?",
          "text": "Le previsioni del tempo per domani: al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "18-28",
            "12-20",
            "8-15"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Dov'è sereno?",
          "text": "Le previsioni del tempo per domani: al centro sereno con qualche nuvola, 12-20 gradi.",
          "opts": [
            "Al centro",
            "Al nord",
            "Al sud"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Ieri io ___ (andare) al mare.",
          "hint": "passato prossimo",
          "ans": "sono andato"
        },
        {
          "type": "fill",
          "q": "Loro ___ (finire) il lavoro.",
          "hint": "passato prossimo",
          "ans": "hanno finito"
        },
        {
          "type": "fill",
          "q": "Noi ___ (vedere) un bel film.",
          "hint": "passato prossimo",
          "ans": "abbiamo visto"
        },
        {
          "type": "fill",
          "q": "Tu ___ (comprare) il pane?",
          "hint": "passato prossimo",
          "ans": "hai comprato"
        },
        {
          "type": "fill",
          "q": "Maria ___ (arrivare) ieri sera.",
          "hint": "passato prossimo",
          "ans": "è arrivata"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una email a un albergo per prenotare una camera doppia per tre notti. Chiedi informazioni sul prezzo, sulla colazione e sul parcheggio.",
          "keywords": [
            "prenotare",
            "camera",
            "notte",
            "prezzo",
            "colazione",
            "parcheggio"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Descrivi la tua casa o il tuo appartamento. Quante stanze ci sono? Com'è la tua camera? Cosa c'è nel soggiorno? Ti piace la tua casa? Perché?",
          "keywords": [
            "casa",
            "appartamento",
            "stanza",
            "camera",
            "soggiorno",
            "cucina",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI3_B1"] = {
  "title": "CELI CELI3 2 (B1)",
  "exam_type": "CELI",
  "set": "CELI3",
  "level": "B1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa dice lo studio sulla lettura?",
          "opts": [
            "Leggere fa bene",
            "Leggere è noioso",
            "I libri costano"
          ],
          "ans": 0,
          "script": "Secondo un recente studio dell'università, leggere almeno trenta minuti al giorno riduce lo stress del sessanta per cento e migliora notevolmente la memoria."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre l'associazione culturale?",
          "opts": [
            "Visite gratuite",
            "Corsi di lingua",
            "Concerti"
          ],
          "ans": 0,
          "script": "L'associazione culturale organizza visite guidate gratuite ai musei della città ogni prima domenica del mese senza bisogno di prenotazione."
        },
        {
          "type": "listen_choice",
          "q": "Qual è il problema principale della città?",
          "opts": [
            "Il traffico",
            "L'inquinamento",
            "Il rumore"
          ],
          "ans": 0,
          "script": "Il problema principale della nostra città rimane il traffico nelle ore di punta. Il comune sta valutando l'introduzione di un pedaggio per il centro storico."
        },
        {
          "type": "listen_choice",
          "q": "Cosa chiede l'insegnante?",
          "opts": [
            "Una ricerca scritta",
            "Una presentazione orale",
            "Un esame a sorpresa"
          ],
          "ans": 1,
          "script": "L'insegnante ha detto che per l'esame finale dobbiamo preparare una presentazione su un argomento a scelta della durata di dieci minuti."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre la nuova biblioteca?",
          "opts": [
            "Prestito digitale",
            "Corsi gratuiti",
            "Sala studio"
          ],
          "ans": 0,
          "script": "La nuova biblioteca comunale offre un servizio di prestito digitale con migliaia di ebook e audiolibri scaricabili gratuitamente da casa."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tipo di lavoro offre?",
          "text": "Cerchiamo un/una cameriere/a per il nostro ristorante in centro. Richiesta esperienza di almeno un anno, conoscenza base dell'inglese, disponibilità serale e nei weekend. Offriamo contratto a tempo determinato di 6 mesi con possibilità di rinnovo. Orario: 18:00-23:00. Inviare CV a lavoro@ristorante.it",
          "opts": [
            "Cameriere/a",
            "Cuoco/a",
            "Barista"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanto dura il contratto?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Richiesta esperienza di almeno un anno. Contratto 6 mesi rinnovabile.",
          "opts": [
            "6 mesi",
            "1 anno",
            "3 mesi"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Qual è l'orario di lavoro?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Offriamo contratto a tempo determinato con possibilità di rinnovo. Orario: 18:00-23:00.",
          "opts": [
            "18:00-23:00",
            "08:00-14:00",
            "12:00-18:00"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Se avessi soldi, ___ (comprare) una casa.",
          "hint": "condizionale",
          "ans": "comprerei"
        },
        {
          "type": "fill",
          "q": "Penso che lui ___ (arrivare) domani.",
          "hint": "congiuntivo presente",
          "ans": "arrivi"
        },
        {
          "type": "fill",
          "q": "Spero che voi ___ (potere) venire.",
          "hint": "congiuntivo presente",
          "ans": "possiate"
        },
        {
          "type": "fill",
          "q": "Prima di ___ (uscire), chiudi la porta.",
          "hint": "infinito",
          "ans": "uscire"
        },
        {
          "type": "fill",
          "q": "Mentre ___ (mangiare), guardava la TV.",
          "hint": "imperfetto",
          "ans": "mangiava"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi un testo di circa 100 parole in cui descrivi la tua routine quotidiana. Parla del lavoro/studio, dei pasti, del tempo libero e dei tuoi hobby.",
          "keywords": [
            "ogni",
            "mattina",
            "lavoro",
            "studio",
            "pomeriggio",
            "sera",
            "tempo libero"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla del tuo lavoro o dei tuoi studi. Cosa fai esattamente? Da quanto tempo? Cosa ti piace di più del tuo lavoro/studio? Quali sono le difficoltà? Cosa vorresti fare in futuro?",
          "keywords": [
            "lavoro",
            "studio",
            "colleghi",
            "progetti",
            "futuro",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI3_B2"] = {
  "title": "CELI CELI3 3 (B2)",
  "exam_type": "CELI",
  "set": "CELI3",
  "level": "B2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa prevede il nuovo regolamento?",
          "opts": [
            "Raccolta differenziata obbligatoria",
            "Nuove tasse",
            "Più parcheggi"
          ],
          "ans": 0,
          "script": "Il nuovo regolamento comunale sulla gestione dei rifiuti prevede l'obbligo della raccolta differenziata dal primo marzo. Le multe vanno da cinquanta a trecento euro."
        },
        {
          "type": "listen_choice",
          "q": "Quanto costa la ristrutturazione?",
          "opts": [
            "1 milione",
            "2 milioni",
            "3 milioni"
          ],
          "ans": 1,
          "script": "L'amministrazione ha stanziato due milioni di euro per la ristrutturazione del teatro comunale che resterà chiuso per diciotto mesi."
        },
        {
          "type": "listen_choice",
          "q": "Quanti nuovi dipendenti?",
          "opts": [
            "30",
            "50",
            "100"
          ],
          "ans": 1,
          "script": "L'azienda ha annunciato l'assunzione di cinquanta nuovi dipendenti entro la fine dell'anno, principalmente nell'area della ricerca e sviluppo."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre il corso?",
          "opts": [
            "Stage retribuiti",
            "Lezioni gratis",
            "Libri inclusi"
          ],
          "ans": 0,
          "script": "Il corso di formazione professionale offre stage retribuiti presso aziende partner e un certificato riconosciuto a livello europeo."
        },
        {
          "type": "listen_choice",
          "q": "Cosa dice il rapporto ISTAT?",
          "opts": [
            "Disoccupazione in calo",
            "Occupazione in aumento",
            "Inflazione stabile"
          ],
          "ans": 1,
          "script": "Secondo l'ultimo rapporto dell'ISTAT, il tasso di occupazione giovanile è aumentato del tre per cento rispetto all'anno precedente."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Di quanto si ridurranno le emissioni?",
          "text": "Il Ministero dell'Ambiente ha annunciato un nuovo piano per la riduzione delle emissioni di CO2 del 55% entro il 2030. Il piano prevede incentivi per l'acquisto di auto elettriche, l'ampliamento delle zone a traffico limitato e investimenti nelle energie rinnovabili. Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "55%",
            "30%",
            "40%"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa NON prevede il piano?",
          "text": "Il piano prevede incentivi per auto elettriche, ampliamento zone a traffico limitato e investimenti in energie rinnovabili.",
          "opts": [
            "Nuove autostrade",
            "Auto elettriche",
            "Zone a traffico limitato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa pensano le associazioni?",
          "text": "Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "Positivo ma vogliono di più",
            "Negativo",
            "Indifferente"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Credo che loro ___ (partire) ieri.",
          "hint": "congiuntivo passato",
          "ans": "siano partiti"
        },
        {
          "type": "fill",
          "q": "Sebbene ___ (piovere), siamo usciti.",
          "hint": "congiuntivo presente",
          "ans": "piova"
        },
        {
          "type": "fill",
          "q": "Benché ___ (essere) stanco, ha finito il lavoro.",
          "hint": "congiuntivo presente",
          "ans": "sia"
        },
        {
          "type": "fill",
          "q": "È importante che tu ___ (studiare) ogni giorno.",
          "hint": "congiuntivo presente",
          "ans": "studi"
        },
        {
          "type": "fill",
          "q": "Temo che non mi ___ (capire).",
          "hint": "congiuntivo presente",
          "ans": "capisca"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una lettera formale al sindaco della tua città per esprimere la tua opinione sulla creazione di una zona a traffico limitato (ZTL) in centro. Argomenta le tue ragioni pro o contro con almeno due argomenti. (150 parole)",
          "keywords": [
            "sindaco",
            "traffico",
            "centro",
            "inquinamento",
            "opinione",
            "argomento"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla dell'importanza della sostenibilità ambientale nella vita quotidiana. Cosa fai concretamente per ridurre il tuo impatto ambientale? Quali cambiamenti vorresti vedere nella tua città?",
          "keywords": [
            "ambiente",
            "sostenibilità",
            "riciclo",
            "energia",
            "città",
            "futuro"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI3_C1"] = {
  "title": "CELI CELI3 4 (C1)",
  "exam_type": "CELI",
  "set": "CELI3",
  "level": "C1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa prevede la riforma scolastica?",
          "opts": [
            "Più ore di studio",
            "Educazione finanziaria",
            "Nuovi edifici"
          ],
          "ans": 1,
          "script": "Il Ministro dell'Istruzione ha presentato oggi la riforma che prevede l'introduzione obbligatoria dell'insegnamento dell'educazione finanziaria e digitale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa investono le PMI?",
          "opts": [
            "Digitalizzazione",
            "Nuovi uffici",
            "Più dipendenti"
          ],
          "ans": 0,
          "script": "L'ultima indagine economica rivela che le piccole e medie imprese italiane investono sempre più nella digitalizzazione, con un incremento del quindici per cento."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ospita il festival?",
          "opts": [
            "Scrittori internazionali",
            "Film",
            "Musica"
          ],
          "ans": 0,
          "script": "Il festival letterario internazionale, giunto alla ventesima edizione, ospiterà scrittori da tutto il mondo, tra cui due Premi Nobel."
        },
        {
          "type": "listen_choice",
          "q": "Cosa devono ripensare le città?",
          "opts": [
            "Gli spazi pubblici",
            "I trasporti",
            "Le tasse"
          ],
          "ans": 0,
          "script": "Secondo gli esperti di urbanistica, le città italiane devono ripensare gli spazi pubblici per favorire l'aggregazione sociale e ridurre l'impatto ambientale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha approvato l'UE?",
          "opts": [
            "Un progetto italiano",
            "Un nuovo trattato",
            "Delle sanzioni"
          ],
          "ans": 0,
          "script": "La Commissione Europea ha approvato un progetto italiano per lo sviluppo di tecnologie innovative nel campo delle energie rinnovabili marine."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa suggerisce lo studio?",
          "text": "Uno studio pubblicato sulla rivista Nature Neuroscience suggerisce che l'apprendimento di una seconda lingua in età adulta può rallentare il declino cognitivo legato all'invecchiamento. I ricercatori hanno seguito 853 partecipanti per oltre 40 anni, scoprendo che i bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui. Il fenomeno sarebbe legato alla maggiore plasticità neuronale indotta dal bilinguismo.",
          "opts": [
            "Il bilinguismo rallenta il declino cognitivo",
            "Il bilinguismo accelera l'invecchiamento",
            "Non c'è alcun effetto"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti partecipanti allo studio?",
          "text": "I ricercatori hanno seguito 853 partecipanti per oltre 40 anni.",
          "opts": [
            "853",
            "583",
            "385"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti anni di ritardo nella demenza?",
          "text": "I bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui.",
          "opts": [
            "4,5 anni",
            "2 anni",
            "10 anni"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Qualora ___ (arrivare) in ritardo, avvisateci.",
          "hint": "congiuntivo imperfetto",
          "ans": "arrivaste"
        },
        {
          "type": "fill",
          "q": "Se lo ___ (sapere), te lo avrei detto.",
          "hint": "congiuntivo trapassato",
          "ans": "avessi saputo"
        },
        {
          "type": "fill",
          "q": "Nonostante ___ (avere) ragione, ha taciuto.",
          "hint": "congiuntivo imperfetto",
          "ans": "avesse"
        },
        {
          "type": "fill",
          "q": "Pur ___ (essere) ricco, vive modestamente.",
          "hint": "gerundio",
          "ans": "essendo"
        },
        {
          "type": "fill",
          "q": "Il libro di cui ti ___ (parlare) è interessante.",
          "hint": "trapassato prossimo",
          "ans": "avevo parlato"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Il governo propone di aumentare l'età pensionabile a 67 anni per tutti i lavoratori. Scrivi un articolo di opinione di circa 200 parole esprimendo la tua posizione, analizzando sia i vantaggi che gli svantaggi della proposta.",
          "keywords": [
            "pensione",
            "lavoro",
            "governo",
            "riforma",
            "vantaggi",
            "svantaggi",
            "futuro"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Discuti il fenomeno della globalizzazione analizzandone vantaggi e svantaggi per l'economia e la cultura locale italiana. Fornisci esempi concreti e una tua opinione personale.",
          "keywords": [
            "globalizzazione",
            "economia",
            "cultura",
            "commercio",
            "identità",
            "tradizione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CELI3_C2"] = {
  "title": "CELI CELI3 5 (C2)",
  "exam_type": "CELI",
  "set": "CELI3",
  "level": "C2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa evidenzia il rapporto digitale?",
          "opts": [
            "L'Italia è avanti",
            "L'Italia è indietro",
            "L'Italia è nella media"
          ],
          "ans": 1,
          "script": "Il rapporto annuale sull'economia digitale evidenzia che l'Italia è ancora indietro nella digitalizzazione della pubblica amministrazione rispetto alla media europea."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha annunciato il museo?",
          "opts": [
            "Una partnership col Louvre",
            "Una nuova ala",
            "Un nuovo direttore"
          ],
          "ans": 0,
          "script": "La direzione del museo ha annunciato una partnership con il Louvre per lo scambio di opere d'arte e progetti di ricerca e restauro."
        },
        {
          "type": "listen_choice",
          "q": "Cosa emerge dall'indagine?",
          "opts": [
            "Più stipendio",
            "Più flessibilità",
            "Più ferie"
          ],
          "ans": 1,
          "script": "L'indagine sociologica su duemila giovani rivela che oltre il sessanta per cento considera la flessibilità lavorativa più importante dello stipendio elevato."
        },
        {
          "type": "listen_choice",
          "q": "Cosa rappresenta il nuovo centro?",
          "opts": [
            "Un passo avanti scientifico",
            "Un costo inutile",
            "Un rischio"
          ],
          "ans": 0,
          "script": "Il nuovo centro di ricerca sulla fusione nucleare inaugurato a Frascati rappresenta un passo avanti nella collaborazione scientifica internazionale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa raccomanda l'OMS?",
          "opts": [
            "150 minuti di sport a settimana",
            "Dieta vegana",
            "8 ore di sonno"
          ],
          "ans": 0,
          "script": "L'Organizzazione Mondiale della Sanità raccomanda almeno centocinquanta minuti di attività fisica moderata a settimana per prevenire malattie cardiovascolari."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa ha dichiarato la Corte?",
          "text": "La recente sentenza della Corte Costituzionale n. 152/2023 ha dichiarato l'illegittimità costituzionale di alcune norme del codice degli appalti, ritenute lesive del principio di libera concorrenza sancito dall'articolo 41 della Costituzione. La decisione avrà ripercussioni significative sul settore delle costruzioni, dove le gare d'appalto dovranno essere riformulate per garantire maggiore trasparenza e pari opportunità tra i concorrenti.",
          "opts": [
            "Illegittimità di norme sugli appalti",
            "Legittimità delle norme",
            "Rinvio della decisione"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quale settore è più colpito?",
          "text": "La decisione avrà ripercussioni sul settore delle costruzioni, dove le gare dovranno essere riformulate per garantire maggiore trasparenza.",
          "opts": [
            "Costruzioni",
            "Sanità",
            "Istruzione"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Lungi dal ___ (voler) offendere, mi scuso.",
          "hint": "infinito",
          "ans": "volere"
        },
        {
          "type": "fill",
          "q": "Per quanto ___ (sforzarsi), non ce la fa.",
          "hint": "congiuntivo presente",
          "ans": "si sforzi"
        },
        {
          "type": "fill",
          "q": "Ove mai ___ (esserci) dubbi, contattateci.",
          "hint": "congiuntivo presente",
          "ans": "ci siano"
        },
        {
          "type": "fill",
          "q": "Al fine di ___ (evitare) disguidi, confermate.",
          "hint": "infinito",
          "ans": "evitare"
        },
        {
          "type": "fill",
          "q": "Il candidato ___ (ritenere) idoneo sarà contattato.",
          "hint": "participio passato",
          "ans": "ritenuto"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Analizza criticamente l'impatto dell'intelligenza artificiale sul mercato del lavoro italiano, considerando gli aspetti etici, economici e sociali. Fornisci esempi concreti e una tua valutazione personale. (300 parole)",
          "keywords": [
            "intelligenza artificiale",
            "lavoro",
            "etica",
            "economia",
            "società"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Analizza le conseguenze della digitalizzazione della pubblica amministrazione in Italia. Quali sono i rischi e i benefici per i cittadini? Considera aspetti come l'accessibilità, la privacy e l'inclusione digitale.",
          "keywords": [
            "digitalizzazione",
            "pubblica amministrazione",
            "cittadini",
            "privacy",
            "accessibilità",
            "inclusione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS1_A1"] = {
  "title": "CILS CILS1 A1",
  "exam_type": "CILS",
  "set": "CILS1",
  "level": "A1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dove lavora Paolo?",
          "opts": [
            "In un ristorante",
            "In un'azienda informatica",
            "In un ospedale"
          ],
          "ans": 1,
          "script": "Paolo lavora in una grande azienda informatica a Torino. Si occupa di sviluppare software per banche e uffici postali."
        },
        {
          "type": "listen_choice",
          "q": "Cosa vuole la signora?",
          "opts": [
            "Frutta e latte",
            "Pane e vino",
            "Carne e formaggio"
          ],
          "ans": 0,
          "script": "Buongiorno, vorrei un chilo di mele e mezzo chilo di pere. Anche una busta di latte intero e due yogurt alla frutta, per favore."
        },
        {
          "type": "listen_choice",
          "q": "Che ora sono le lezioni?",
          "opts": [
            "8:30-11:00",
            "8:45-11:00",
            "9:00-11:00"
          ],
          "ans": 1,
          "script": "Le lezioni di italiano cominciano alle otto e tre quarti e finiscono alle undici. La pausa è dalle dieci e un quarto alle dieci e mezza."
        },
        {
          "type": "listen_choice",
          "q": "Perché Sara è contenta?",
          "opts": [
            "Ha trovato lavoro",
            "Ha vinto una borsa di studio",
            "Ha comprato casa"
          ],
          "ans": 1,
          "script": "Sara ha ricevuto una borsa di studio per studiare arte a Firenze per un anno intero. È felicissima perché è la sua città preferita."
        },
        {
          "type": "listen_choice",
          "q": "Cosa prenota il signore?",
          "opts": [
            "Un tavolo",
            "Una camera",
            "Un biglietto"
          ],
          "ans": 1,
          "script": "Buongiorno, vorrei prenotare una camera doppia per tre notti dal quindici al diciotto agosto con colazione inclusa, per favore."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Dove abita Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli con la mia famiglia. Studio medicina all'università e nel tempo libero suono la chitarra. Mi piace molto la pizza e il mare.",
          "opts": [
            "A Napoli",
            "A Roma",
            "A Milano"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa studia Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina all'università e nel tempo libero suono la chitarra.",
          "opts": [
            "Medicina",
            "Ingegneria",
            "Economia"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa piace a Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina e nel tempo libero suono la chitarra. Mi piace molto la pizza.",
          "opts": [
            "La pizza",
            "La pasta",
            "Il pesce"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Io ___ (essere) italiano.",
          "hint": "presente",
          "ans": "sono"
        },
        {
          "type": "fill",
          "q": "Loro ___ (avere) due cani.",
          "hint": "presente",
          "ans": "hanno"
        },
        {
          "type": "fill",
          "q": "Tu ___ (andare) a scuola in autobus.",
          "hint": "presente",
          "ans": "vai"
        },
        {
          "type": "fill",
          "q": "Noi ___ (parlare) italiano.",
          "hint": "presente",
          "ans": "parliamo"
        },
        {
          "type": "fill",
          "q": "Maria ___ (leggere) un libro.",
          "hint": "presente",
          "ans": "legge"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una breve email per presentarti a un nuovo amico italiano. Parla del tuo nome, della tua età, della tua città e dei tuoi hobby. (50-80 parole)",
          "keywords": [
            "mi chiamo",
            "anni",
            "abito",
            "mi piace",
            "hobby"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla della tua giornata tipica. Descrivi cosa fai dalla mattina alla sera (sveglia, colazione, lavoro/studio, pranzo, tempo libero, cena).",
          "keywords": [
            "sveglia",
            "colazione",
            "lavoro",
            "studio",
            "pranzo",
            "cena"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS1_A2"] = {
  "title": "CILS CILS1 A2",
  "exam_type": "CILS",
  "set": "CILS1",
  "level": "A2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dov'è andato Marco in vacanza?",
          "opts": [
            "In Sardegna",
            "In Sicilia",
            "In Puglia"
          ],
          "ans": 1,
          "script": "Marco è andato in vacanza in Sicilia con la sua ragazza. Sono stati una settimana a Taormina, un paese bellissimo sul mare, e hanno visitato anche l'Etna."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha perso la ragazza?",
          "opts": [
            "Il telefono",
            "Lo zaino",
            "La borsa"
          ],
          "ans": 1,
          "script": "Mi scusi, ho perso il mio zaino grigio. Dentro c'erano il computer portatile e i libri dell'università. L'ho lasciato al bar della stazione."
        },
        {
          "type": "listen_choice",
          "q": "Che lavoro fa il signor Moretti?",
          "opts": [
            "Insegnante",
            "Giornalista",
            "Avvocato"
          ],
          "ans": 1,
          "script": "Sono il signor Moretti, faccio il giornalista da più di vent'anni. Lavoro per un importante quotidiano nazionale e seguo la cronaca estera."
        },
        {
          "type": "listen_choice",
          "q": "Cosa serve per l'esame?",
          "opts": [
            "Libri e dizionario",
            "Documento e ricevuta",
            "Computer e calcolatrice"
          ],
          "ans": 1,
          "script": "Per l'esame di certificazione dovete portare un documento d'identità valido e la ricevuta del pagamento. Non sono ammessi telefoni cellulari durante la prova."
        },
        {
          "type": "listen_choice",
          "q": "A che ora parte l'ultimo treno?",
          "opts": [
            "22:30",
            "23:00",
            "23:30"
          ],
          "ans": 2,
          "script": "L'ultimo treno per Napoli parte alle ventitré e trenta dal binario sette. Il Regionale per Salerno parte ogni ora fino a mezzanotte."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tempo fa al nord?",
          "text": "Le previsioni del tempo per domani: al nord nuvoloso con possibili piogge, temperature tra 8 e 15 gradi. Al centro sereno con qualche nuvola, 12-20 gradi. Al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "Nuvoloso",
            "Sereno",
            "Soleggiato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti gradi al sud?",
          "text": "Le previsioni del tempo per domani: al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "18-28",
            "12-20",
            "8-15"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Dov'è sereno?",
          "text": "Le previsioni del tempo per domani: al centro sereno con qualche nuvola, 12-20 gradi.",
          "opts": [
            "Al centro",
            "Al nord",
            "Al sud"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Ieri io ___ (andare) al mare.",
          "hint": "passato prossimo",
          "ans": "sono andato"
        },
        {
          "type": "fill",
          "q": "Loro ___ (finire) il lavoro.",
          "hint": "passato prossimo",
          "ans": "hanno finito"
        },
        {
          "type": "fill",
          "q": "Noi ___ (vedere) un bel film.",
          "hint": "passato prossimo",
          "ans": "abbiamo visto"
        },
        {
          "type": "fill",
          "q": "Tu ___ (comprare) il pane?",
          "hint": "passato prossimo",
          "ans": "hai comprato"
        },
        {
          "type": "fill",
          "q": "Maria ___ (arrivare) ieri sera.",
          "hint": "passato prossimo",
          "ans": "è arrivata"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una email a un albergo per prenotare una camera doppia per tre notti. Chiedi informazioni sul prezzo, sulla colazione e sul parcheggio.",
          "keywords": [
            "prenotare",
            "camera",
            "notte",
            "prezzo",
            "colazione",
            "parcheggio"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Descrivi la tua casa o il tuo appartamento. Quante stanze ci sono? Com'è la tua camera? Cosa c'è nel soggiorno? Ti piace la tua casa? Perché?",
          "keywords": [
            "casa",
            "appartamento",
            "stanza",
            "camera",
            "soggiorno",
            "cucina",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS1_B1"] = {
  "title": "CILS CILS1 B1",
  "exam_type": "CILS",
  "set": "CILS1",
  "level": "B1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa propone il sindaco?",
          "opts": [
            "Nuovi parcheggi",
            "Nuovi alberi",
            "Nuove strade"
          ],
          "ans": 1,
          "script": "Il sindaco ha annunciato che entro la fine dell'anno verranno piantati cinquemila nuovi alberi nelle aree periferiche per migliorare la qualità dell'aria e creare nuove aree verdi."
        },
        {
          "type": "listen_choice",
          "q": "Perché Marta ha cambiato università?",
          "opts": [
            "Era troppo difficile",
            "Non le piaceva il corso",
            "Era troppo lontana"
          ],
          "ans": 1,
          "script": "Marta ha cambiato università perché il corso che frequentava non corrispondeva alle sue aspettative. Ora studia Mediazione Linguistica e si trova molto meglio."
        },
        {
          "type": "listen_choice",
          "q": "Cosa pensa il dottore della dieta?",
          "opts": [
            "Mangiare meno",
            "Dieta più equilibrata",
            "Più sport"
          ],
          "ans": 1,
          "script": "Il dottore mi ha detto di seguire una dieta più equilibrata: più verdura, meno grassi e attività fisica almeno tre volte a settimana per migliorare la salute."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre l'agenzia?",
          "opts": [
            "Vacanze studio all'estero",
            "Stage lavorativi",
            "Scambi culturali"
          ],
          "ans": 0,
          "script": "L'agenzia offre corsi di lingua all'estero per studenti dai sedici ai venticinque anni. Le destinazioni includono Inghilterra, Stati Uniti, Spagna e Francia."
        },
        {
          "type": "listen_choice",
          "q": "Qual è il problema del condominio?",
          "opts": [
            "Il riscaldamento",
            "L'umidità",
            "Il rumore"
          ],
          "ans": 1,
          "script": "Durante l'assemblea condominiale i residenti hanno discusso del problema dell'umidità che danneggia i muri degli appartamenti al primo piano."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tipo di lavoro offre?",
          "text": "Cerchiamo un/una cameriere/a per il nostro ristorante in centro. Richiesta esperienza di almeno un anno, conoscenza base dell'inglese, disponibilità serale e nei weekend. Offriamo contratto a tempo determinato di 6 mesi con possibilità di rinnovo. Orario: 18:00-23:00. Inviare CV a lavoro@ristorante.it",
          "opts": [
            "Cameriere/a",
            "Cuoco/a",
            "Barista"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanto dura il contratto?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Richiesta esperienza di almeno un anno. Contratto 6 mesi rinnovabile.",
          "opts": [
            "6 mesi",
            "1 anno",
            "3 mesi"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Qual è l'orario di lavoro?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Offriamo contratto a tempo determinato con possibilità di rinnovo. Orario: 18:00-23:00.",
          "opts": [
            "18:00-23:00",
            "08:00-14:00",
            "12:00-18:00"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Se avessi soldi, ___ (comprare) una casa.",
          "hint": "condizionale",
          "ans": "comprerei"
        },
        {
          "type": "fill",
          "q": "Penso che lui ___ (arrivare) domani.",
          "hint": "congiuntivo presente",
          "ans": "arrivi"
        },
        {
          "type": "fill",
          "q": "Spero che voi ___ (potere) venire.",
          "hint": "congiuntivo presente",
          "ans": "possiate"
        },
        {
          "type": "fill",
          "q": "Prima di ___ (uscire), chiudi la porta.",
          "hint": "infinito",
          "ans": "uscire"
        },
        {
          "type": "fill",
          "q": "Mentre ___ (mangiare), guardava la TV.",
          "hint": "imperfetto",
          "ans": "mangiava"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi un testo di circa 100 parole in cui descrivi la tua routine quotidiana. Parla del lavoro/studio, dei pasti, del tempo libero e dei tuoi hobby.",
          "keywords": [
            "ogni",
            "mattina",
            "lavoro",
            "studio",
            "pomeriggio",
            "sera",
            "tempo libero"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla del tuo lavoro o dei tuoi studi. Cosa fai esattamente? Da quanto tempo? Cosa ti piace di più del tuo lavoro/studio? Quali sono le difficoltà? Cosa vorresti fare in futuro?",
          "keywords": [
            "lavoro",
            "studio",
            "colleghi",
            "progetti",
            "futuro",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS1_B2"] = {
  "title": "CILS CILS1 B2",
  "exam_type": "CILS",
  "set": "CILS1",
  "level": "B2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Di cosa si occupa la conferenza?",
          "opts": [
            "Energia nucleare",
            "Sviluppo sostenibile",
            "Innovazione digitale"
          ],
          "ans": 1,
          "script": "Benvenuti alla conferenza annuale sullo sviluppo sostenibile. Quest'anno ci concentriamo sull'economia circolare e sulle strategie per ridurre i rifiuti plastici negli oceani."
        },
        {
          "type": "listen_choice",
          "q": "Quale critica viene fatta al sistema?",
          "opts": [
            "Prezzi troppo alti",
            "Mezzi non puntuali",
            "Stazioni sporche"
          ],
          "ans": 1,
          "script": "Molti cittadini lamentano che i mezzi pubblici non sono puntuali e che le corse serali sono troppo ridotte. Il comune ha promesso di potenziare il servizio."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha scoperto la ricerca?",
          "opts": [
            "Leggere fa bene",
            "Leggere è noioso",
            "I libri costano troppo"
          ],
          "ans": 0,
          "script": "Un recente studio ha scoperto che leggere almeno trenta minuti al giorno riduce lo stress del sessantotto per cento e migliora la memoria a lungo termine."
        },
        {
          "type": "listen_choice",
          "q": "Cosa propone l'associazione?",
          "opts": [
            "Visite guidate gratuite",
            "Corsi d'arte",
            "Mostre temporanee"
          ],
          "ans": 0,
          "script": "L'associazione culturale 'Arte per Tutti' organizza visite guidate gratuite ai musei della città ogni prima domenica del mese, senza necessità di prenotazione."
        },
        {
          "type": "listen_choice",
          "q": "Qual è il problema principale?",
          "opts": [
            "L'inquinamento",
            "Il traffico",
            "Il rumore"
          ],
          "ans": 1,
          "script": "Il problema principale della nostra città rimane il traffico nelle ore di punta. Il comune sta valutando l'introduzione di un pedaggio per l'accesso al centro storico."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Di quanto si ridurranno le emissioni?",
          "text": "Il Ministero dell'Ambiente ha annunciato un nuovo piano per la riduzione delle emissioni di CO2 del 55% entro il 2030. Il piano prevede incentivi per l'acquisto di auto elettriche, l'ampliamento delle zone a traffico limitato e investimenti nelle energie rinnovabili. Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "55%",
            "30%",
            "40%"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa NON prevede il piano?",
          "text": "Il piano prevede incentivi per auto elettriche, ampliamento zone a traffico limitato e investimenti in energie rinnovabili.",
          "opts": [
            "Nuove autostrade",
            "Auto elettriche",
            "Zone a traffico limitato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa pensano le associazioni?",
          "text": "Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "Positivo ma vogliono di più",
            "Negativo",
            "Indifferente"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Credo che loro ___ (partire) ieri.",
          "hint": "congiuntivo passato",
          "ans": "siano partiti"
        },
        {
          "type": "fill",
          "q": "Sebbene ___ (piovere), siamo usciti.",
          "hint": "congiuntivo presente",
          "ans": "piova"
        },
        {
          "type": "fill",
          "q": "Benché ___ (essere) stanco, ha finito il lavoro.",
          "hint": "congiuntivo presente",
          "ans": "sia"
        },
        {
          "type": "fill",
          "q": "È importante che tu ___ (studiare) ogni giorno.",
          "hint": "congiuntivo presente",
          "ans": "studi"
        },
        {
          "type": "fill",
          "q": "Temo che non mi ___ (capire).",
          "hint": "congiuntivo presente",
          "ans": "capisca"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una lettera formale al sindaco della tua città per esprimere la tua opinione sulla creazione di una zona a traffico limitato (ZTL) in centro. Argomenta le tue ragioni pro o contro con almeno due argomenti. (150 parole)",
          "keywords": [
            "sindaco",
            "traffico",
            "centro",
            "inquinamento",
            "opinione",
            "argomento"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla dell'importanza della sostenibilità ambientale nella vita quotidiana. Cosa fai concretamente per ridurre il tuo impatto ambientale? Quali cambiamenti vorresti vedere nella tua città?",
          "keywords": [
            "ambiente",
            "sostenibilità",
            "riciclo",
            "energia",
            "città",
            "futuro"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS1_C1"] = {
  "title": "CILS CILS1 C1",
  "exam_type": "CILS",
  "set": "CILS1",
  "level": "C1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Quale iniziativa viene discussa?",
          "opts": [
            "Nuova metropolitana",
            "Mobilità sostenibile",
            "Pedaggi autostradali"
          ],
          "ans": 1,
          "script": "La regione ha presentato il nuovo piano per la mobilità sostenibile che prevede l'estensione della rete ciclabile e l'introduzione di bus elettrici, con un investimento di 45 milioni di euro."
        },
        {
          "type": "listen_choice",
          "q": "Quale critica viene sollevata?",
          "opts": [
            "Disparità nord-sud",
            "Mancanza di medici",
            "Ospedali vecchi"
          ],
          "ans": 0,
          "script": "Nonostante i progressi, il rapporto segnala significative disparità tra nord e sud nell'accesso ai servizi sanitari. Le regioni meridionali registrano tempi d'attesa più lunghi."
        },
        {
          "type": "listen_choice",
          "q": "Cosa propone lo psicologo?",
          "opts": [
            "Meno ore di lavoro",
            "Pause obbligatorie",
            "Più ferie"
          ],
          "ans": 1,
          "script": "La psicologa del lavoro suggerisce pause obbligatorie di quindici minuti ogni due ore di lavoro al computer per prevenire affaticamento e aumentare la produttività."
        },
        {
          "type": "listen_choice",
          "q": "Perché l'artista è controverso?",
          "opts": [
            "Usa materiali costosi",
            "Opera provocatoria",
            "È troppo giovane"
          ],
          "ans": 1,
          "script": "Il giovane artista siciliano ha suscitato un acceso dibattito con la sua ultima opera che critica il consumismo attraverso l'utilizzo di rifiuti industriali."
        },
        {
          "type": "listen_choice",
          "q": "Cosa succederà dal prossimo anno?",
          "opts": [
            "Nuove tasse",
            "Nuovo sistema esami",
            "Più corsi online"
          ],
          "ans": 1,
          "script": "A partire dal prossimo anno accademico, l'università introdurrà un nuovo sistema di valutazione con esami scritti al computer e prove orali registrate."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa suggerisce lo studio?",
          "text": "Uno studio pubblicato sulla rivista Nature Neuroscience suggerisce che l'apprendimento di una seconda lingua in età adulta può rallentare il declino cognitivo legato all'invecchiamento. I ricercatori hanno seguito 853 partecipanti per oltre 40 anni, scoprendo che i bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui. Il fenomeno sarebbe legato alla maggiore plasticità neuronale indotta dal bilinguismo.",
          "opts": [
            "Il bilinguismo rallenta il declino cognitivo",
            "Il bilinguismo accelera l'invecchiamento",
            "Non c'è alcun effetto"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti partecipanti allo studio?",
          "text": "I ricercatori hanno seguito 853 partecipanti per oltre 40 anni.",
          "opts": [
            "853",
            "583",
            "385"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti anni di ritardo nella demenza?",
          "text": "I bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui.",
          "opts": [
            "4,5 anni",
            "2 anni",
            "10 anni"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Qualora ___ (arrivare) in ritardo, avvisateci.",
          "hint": "congiuntivo imperfetto",
          "ans": "arrivaste"
        },
        {
          "type": "fill",
          "q": "Se lo ___ (sapere), te lo avrei detto.",
          "hint": "congiuntivo trapassato",
          "ans": "avessi saputo"
        },
        {
          "type": "fill",
          "q": "Nonostante ___ (avere) ragione, ha taciuto.",
          "hint": "congiuntivo imperfetto",
          "ans": "avesse"
        },
        {
          "type": "fill",
          "q": "Pur ___ (essere) ricco, vive modestamente.",
          "hint": "gerundio",
          "ans": "essendo"
        },
        {
          "type": "fill",
          "q": "Il libro di cui ti ___ (parlare) è interessante.",
          "hint": "trapassato prossimo",
          "ans": "avevo parlato"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Il governo propone di aumentare l'età pensionabile a 67 anni per tutti i lavoratori. Scrivi un articolo di opinione di circa 200 parole esprimendo la tua posizione, analizzando sia i vantaggi che gli svantaggi della proposta.",
          "keywords": [
            "pensione",
            "lavoro",
            "governo",
            "riforma",
            "vantaggi",
            "svantaggi",
            "futuro"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Discuti il fenomeno della globalizzazione analizzandone vantaggi e svantaggi per l'economia e la cultura locale italiana. Fornisci esempi concreti e una tua opinione personale.",
          "keywords": [
            "globalizzazione",
            "economia",
            "cultura",
            "commercio",
            "identità",
            "tradizione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS1_C2"] = {
  "title": "CILS CILS1 C2",
  "exam_type": "CILS",
  "set": "CILS1",
  "level": "C2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Quale tesi sostiene il linguista?",
          "opts": [
            "L'italiano si impoverisce",
            "La lingua si evolve",
            "I dialetti scompaiono"
          ],
          "ans": 1,
          "script": "Il professor Marchesi sostiene che l'evoluzione dell'italiano contemporaneo non rappresenta un impoverimento ma una naturale trasformazione linguistica."
        },
        {
          "type": "listen_choice",
          "q": "Quale critica muove al sistema?",
          "opts": [
            "Mancanza di giudici",
            "Processi troppo lunghi",
            "Poche sentenze"
          ],
          "ans": 1,
          "script": "Il presidente della Corte Suprema ha denunciato la lentezza della giustizia italiana, definendola una piaga che mina la fiducia dei cittadini nello Stato."
        },
        {
          "type": "listen_choice",
          "q": "Cosa emerge dallo studio?",
          "opts": [
            "I giovani non vogliono lavorare",
            "Priorità alla qualità della vita",
            "Tutti vogliono carriera"
          ],
          "ans": 1,
          "script": "La ricerca rivela che il settanta per cento dei giovani tra diciotto e trent'anni privilegia la qualità della vita rispetto alla carriera."
        },
        {
          "type": "listen_choice",
          "q": "Cosa si propone per il turismo?",
          "opts": [
            "Più voli low-cost",
            "Destagionalizzazione",
            "Meno turisti"
          ],
          "ans": 1,
          "script": "Il nuovo piano strategico per il turismo punta sulla destagionalizzazione e sulla promozione dei borghi meno conosciuti."
        },
        {
          "type": "listen_choice",
          "q": "Qual è la posizione del filosofo?",
          "opts": [
            "L'IA va potenziata",
            "L'IA ha bisogno di etica",
            "L'IA va vietata"
          ],
          "ans": 1,
          "script": "Il filosofo ha espresso una posizione critica sull'intelligenza artificiale, avvertendo che lo sviluppo senza regolamentazione etica rischia di delegare il pensiero critico alle macchine."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa ha dichiarato la Corte?",
          "text": "La recente sentenza della Corte Costituzionale n. 152/2023 ha dichiarato l'illegittimità costituzionale di alcune norme del codice degli appalti, ritenute lesive del principio di libera concorrenza sancito dall'articolo 41 della Costituzione. La decisione avrà ripercussioni significative sul settore delle costruzioni, dove le gare d'appalto dovranno essere riformulate per garantire maggiore trasparenza e pari opportunità tra i concorrenti.",
          "opts": [
            "Illegittimità di norme sugli appalti",
            "Legittimità delle norme",
            "Rinvio della decisione"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quale settore è più colpito?",
          "text": "La decisione avrà ripercussioni sul settore delle costruzioni, dove le gare dovranno essere riformulate per garantire maggiore trasparenza.",
          "opts": [
            "Costruzioni",
            "Sanità",
            "Istruzione"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Lungi dal ___ (voler) offendere, mi scuso.",
          "hint": "infinito",
          "ans": "volere"
        },
        {
          "type": "fill",
          "q": "Per quanto ___ (sforzarsi), non ce la fa.",
          "hint": "congiuntivo presente",
          "ans": "si sforzi"
        },
        {
          "type": "fill",
          "q": "Ove mai ___ (esserci) dubbi, contattateci.",
          "hint": "congiuntivo presente",
          "ans": "ci siano"
        },
        {
          "type": "fill",
          "q": "Al fine di ___ (evitare) disguidi, confermate.",
          "hint": "infinito",
          "ans": "evitare"
        },
        {
          "type": "fill",
          "q": "Il candidato ___ (ritenere) idoneo sarà contattato.",
          "hint": "participio passato",
          "ans": "ritenuto"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Analizza criticamente l'impatto dell'intelligenza artificiale sul mercato del lavoro italiano, considerando gli aspetti etici, economici e sociali. Fornisci esempi concreti e una tua valutazione personale. (300 parole)",
          "keywords": [
            "intelligenza artificiale",
            "lavoro",
            "etica",
            "economia",
            "società"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Analizza le conseguenze della digitalizzazione della pubblica amministrazione in Italia. Quali sono i rischi e i benefici per i cittadini? Considera aspetti come l'accessibilità, la privacy e l'inclusione digitale.",
          "keywords": [
            "digitalizzazione",
            "pubblica amministrazione",
            "cittadini",
            "privacy",
            "accessibilità",
            "inclusione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS2_A1"] = {
  "title": "CILS CILS2 A1",
  "exam_type": "CILS",
  "set": "CILS2",
  "level": "A1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa fa Francesca la sera?",
          "opts": [
            "Guarda la TV",
            "Fa yoga",
            "Esce con amici"
          ],
          "ans": 1,
          "script": "Francesca frequenta un corso di yoga tre sere a settimana. Dice che dopo le lezioni si sente molto più rilassata e dorme meglio."
        },
        {
          "type": "listen_choice",
          "q": "Dove va Mario in vacanza?",
          "opts": [
            "In montagna",
            "Al mare in Sardegna",
            "In città d'arte"
          ],
          "ans": 1,
          "script": "Quest'anno Mario va al mare in Sardegna con la famiglia. Rimangono due settimane a luglio in un piccolo paese vicino a Cagliari."
        },
        {
          "type": "listen_choice",
          "q": "Quanto costa il biglietto?",
          "opts": [
            "25 euro",
            "30 euro",
            "40 euro"
          ],
          "ans": 1,
          "script": "Il biglietto per il concerto costa trenta euro online o trentacinque euro alla cassa. I ragazzi sotto i quattordici anni pagano la metà."
        },
        {
          "type": "listen_choice",
          "q": "Che regalo compra Anna?",
          "opts": [
            "Un libro",
            "Una sciarpa",
            "Un profumo"
          ],
          "ans": 1,
          "script": "Anna compra per il compleanno della mamma una sciarpa di seta rossa e una scatola di cioccolatini artigianali."
        },
        {
          "type": "listen_choice",
          "q": "A che ora apre il supermercato?",
          "opts": [
            "8:00",
            "8:30",
            "9:00"
          ],
          "ans": 1,
          "script": "Il supermercato apre alle otto e mezza la mattina e chiude alle otto di sera. La domenica è aperto solo la mattina dalle nove alle tredici."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Dove abita Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli con la mia famiglia. Studio medicina all'università e nel tempo libero suono la chitarra. Mi piace molto la pizza e il mare.",
          "opts": [
            "A Napoli",
            "A Roma",
            "A Milano"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa studia Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina all'università e nel tempo libero suono la chitarra.",
          "opts": [
            "Medicina",
            "Ingegneria",
            "Economia"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa piace a Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina e nel tempo libero suono la chitarra. Mi piace molto la pizza.",
          "opts": [
            "La pizza",
            "La pasta",
            "Il pesce"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Io ___ (essere) italiano.",
          "hint": "presente",
          "ans": "sono"
        },
        {
          "type": "fill",
          "q": "Loro ___ (avere) due cani.",
          "hint": "presente",
          "ans": "hanno"
        },
        {
          "type": "fill",
          "q": "Tu ___ (andare) a scuola in autobus.",
          "hint": "presente",
          "ans": "vai"
        },
        {
          "type": "fill",
          "q": "Noi ___ (parlare) italiano.",
          "hint": "presente",
          "ans": "parliamo"
        },
        {
          "type": "fill",
          "q": "Maria ___ (leggere) un libro.",
          "hint": "presente",
          "ans": "legge"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una breve email per presentarti a un nuovo amico italiano. Parla del tuo nome, della tua età, della tua città e dei tuoi hobby. (50-80 parole)",
          "keywords": [
            "mi chiamo",
            "anni",
            "abito",
            "mi piace",
            "hobby"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla della tua giornata tipica. Descrivi cosa fai dalla mattina alla sera (sveglia, colazione, lavoro/studio, pranzo, tempo libero, cena).",
          "keywords": [
            "sveglia",
            "colazione",
            "lavoro",
            "studio",
            "pranzo",
            "cena"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS2_A2"] = {
  "title": "CILS CILS2 A2",
  "exam_type": "CILS",
  "set": "CILS2",
  "level": "A2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dove ha cenato ieri sera?",
          "opts": [
            "A casa",
            "In un ristorante giapponese",
            "In mensa"
          ],
          "ans": 1,
          "script": "Ieri sera ho cenato in un ristorante giapponese con i colleghi di lavoro. Abbiamo mangiato sushi e bevuto tè verde. Il conto era quaranta euro a testa."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha comprato Lucia?",
          "opts": [
            "Un vestito",
            "Una borsa",
            "Un paio di scarpe"
          ],
          "ans": 0,
          "script": "Lucia ha comprato un vestito nuovo per la festa di compleanno della sorella. Era in saldo e costava solo trentacinque euro, un vero affare."
        },
        {
          "type": "listen_choice",
          "q": "Com'è andato l'esame?",
          "opts": [
            "Male",
            "Bene",
            "Così così"
          ],
          "ans": 1,
          "script": "L'esame di guida è andato bene. Ho sbagliato solo il parcheggio laterale, ma l'istruttore ha detto che sono migliorato molto rispetto all'ultima volta."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha detto il medico?",
          "opts": [
            "Sto bene",
            "Devo riposare",
            "Devo operarmi"
          ],
          "ans": 1,
          "script": "Il medico ha detto che devo riposare almeno tre giorni perché ho l'influenza. Mi ha prescritto delle medicine e molta acqua."
        },
        {
          "type": "listen_choice",
          "q": "Quanto hanno aspettato?",
          "opts": [
            "20 minuti",
            "30 minuti",
            "40 minuti"
          ],
          "ans": 2,
          "script": "Hanno aspettato il treno per più di mezz'ora alla stazione centrale. Poi il treno è arrivato con venticinque minuti di ritardo a causa di un guasto."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tempo fa al nord?",
          "text": "Le previsioni del tempo per domani: al nord nuvoloso con possibili piogge, temperature tra 8 e 15 gradi. Al centro sereno con qualche nuvola, 12-20 gradi. Al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "Nuvoloso",
            "Sereno",
            "Soleggiato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti gradi al sud?",
          "text": "Le previsioni del tempo per domani: al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "18-28",
            "12-20",
            "8-15"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Dov'è sereno?",
          "text": "Le previsioni del tempo per domani: al centro sereno con qualche nuvola, 12-20 gradi.",
          "opts": [
            "Al centro",
            "Al nord",
            "Al sud"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Ieri io ___ (andare) al mare.",
          "hint": "passato prossimo",
          "ans": "sono andato"
        },
        {
          "type": "fill",
          "q": "Loro ___ (finire) il lavoro.",
          "hint": "passato prossimo",
          "ans": "hanno finito"
        },
        {
          "type": "fill",
          "q": "Noi ___ (vedere) un bel film.",
          "hint": "passato prossimo",
          "ans": "abbiamo visto"
        },
        {
          "type": "fill",
          "q": "Tu ___ (comprare) il pane?",
          "hint": "passato prossimo",
          "ans": "hai comprato"
        },
        {
          "type": "fill",
          "q": "Maria ___ (arrivare) ieri sera.",
          "hint": "passato prossimo",
          "ans": "è arrivata"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una email a un albergo per prenotare una camera doppia per tre notti. Chiedi informazioni sul prezzo, sulla colazione e sul parcheggio.",
          "keywords": [
            "prenotare",
            "camera",
            "notte",
            "prezzo",
            "colazione",
            "parcheggio"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Descrivi la tua casa o il tuo appartamento. Quante stanze ci sono? Com'è la tua camera? Cosa c'è nel soggiorno? Ti piace la tua casa? Perché?",
          "keywords": [
            "casa",
            "appartamento",
            "stanza",
            "camera",
            "soggiorno",
            "cucina",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS2_B1"] = {
  "title": "CILS CILS2 B1",
  "exam_type": "CILS",
  "set": "CILS2",
  "level": "B1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa dice lo studio sulla lettura?",
          "opts": [
            "Leggere fa bene",
            "Leggere è noioso",
            "I libri costano"
          ],
          "ans": 0,
          "script": "Secondo un recente studio dell'università, leggere almeno trenta minuti al giorno riduce lo stress del sessanta per cento e migliora notevolmente la memoria."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre l'associazione culturale?",
          "opts": [
            "Visite gratuite",
            "Corsi di lingua",
            "Concerti"
          ],
          "ans": 0,
          "script": "L'associazione culturale organizza visite guidate gratuite ai musei della città ogni prima domenica del mese senza bisogno di prenotazione."
        },
        {
          "type": "listen_choice",
          "q": "Qual è il problema principale della città?",
          "opts": [
            "Il traffico",
            "L'inquinamento",
            "Il rumore"
          ],
          "ans": 0,
          "script": "Il problema principale della nostra città rimane il traffico nelle ore di punta. Il comune sta valutando l'introduzione di un pedaggio per il centro storico."
        },
        {
          "type": "listen_choice",
          "q": "Cosa chiede l'insegnante?",
          "opts": [
            "Una ricerca scritta",
            "Una presentazione orale",
            "Un esame a sorpresa"
          ],
          "ans": 1,
          "script": "L'insegnante ha detto che per l'esame finale dobbiamo preparare una presentazione su un argomento a scelta della durata di dieci minuti."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre la nuova biblioteca?",
          "opts": [
            "Prestito digitale",
            "Corsi gratuiti",
            "Sala studio"
          ],
          "ans": 0,
          "script": "La nuova biblioteca comunale offre un servizio di prestito digitale con migliaia di ebook e audiolibri scaricabili gratuitamente da casa."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tipo di lavoro offre?",
          "text": "Cerchiamo un/una cameriere/a per il nostro ristorante in centro. Richiesta esperienza di almeno un anno, conoscenza base dell'inglese, disponibilità serale e nei weekend. Offriamo contratto a tempo determinato di 6 mesi con possibilità di rinnovo. Orario: 18:00-23:00. Inviare CV a lavoro@ristorante.it",
          "opts": [
            "Cameriere/a",
            "Cuoco/a",
            "Barista"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanto dura il contratto?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Richiesta esperienza di almeno un anno. Contratto 6 mesi rinnovabile.",
          "opts": [
            "6 mesi",
            "1 anno",
            "3 mesi"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Qual è l'orario di lavoro?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Offriamo contratto a tempo determinato con possibilità di rinnovo. Orario: 18:00-23:00.",
          "opts": [
            "18:00-23:00",
            "08:00-14:00",
            "12:00-18:00"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Se avessi soldi, ___ (comprare) una casa.",
          "hint": "condizionale",
          "ans": "comprerei"
        },
        {
          "type": "fill",
          "q": "Penso che lui ___ (arrivare) domani.",
          "hint": "congiuntivo presente",
          "ans": "arrivi"
        },
        {
          "type": "fill",
          "q": "Spero che voi ___ (potere) venire.",
          "hint": "congiuntivo presente",
          "ans": "possiate"
        },
        {
          "type": "fill",
          "q": "Prima di ___ (uscire), chiudi la porta.",
          "hint": "infinito",
          "ans": "uscire"
        },
        {
          "type": "fill",
          "q": "Mentre ___ (mangiare), guardava la TV.",
          "hint": "imperfetto",
          "ans": "mangiava"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi un testo di circa 100 parole in cui descrivi la tua routine quotidiana. Parla del lavoro/studio, dei pasti, del tempo libero e dei tuoi hobby.",
          "keywords": [
            "ogni",
            "mattina",
            "lavoro",
            "studio",
            "pomeriggio",
            "sera",
            "tempo libero"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla del tuo lavoro o dei tuoi studi. Cosa fai esattamente? Da quanto tempo? Cosa ti piace di più del tuo lavoro/studio? Quali sono le difficoltà? Cosa vorresti fare in futuro?",
          "keywords": [
            "lavoro",
            "studio",
            "colleghi",
            "progetti",
            "futuro",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS2_B2"] = {
  "title": "CILS CILS2 B2",
  "exam_type": "CILS",
  "set": "CILS2",
  "level": "B2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa prevede il nuovo regolamento?",
          "opts": [
            "Raccolta differenziata obbligatoria",
            "Nuove tasse",
            "Più parcheggi"
          ],
          "ans": 0,
          "script": "Il nuovo regolamento comunale sulla gestione dei rifiuti prevede l'obbligo della raccolta differenziata dal primo marzo. Le multe vanno da cinquanta a trecento euro."
        },
        {
          "type": "listen_choice",
          "q": "Quanto costa la ristrutturazione?",
          "opts": [
            "1 milione",
            "2 milioni",
            "3 milioni"
          ],
          "ans": 1,
          "script": "L'amministrazione ha stanziato due milioni di euro per la ristrutturazione del teatro comunale che resterà chiuso per diciotto mesi."
        },
        {
          "type": "listen_choice",
          "q": "Quanti nuovi dipendenti?",
          "opts": [
            "30",
            "50",
            "100"
          ],
          "ans": 1,
          "script": "L'azienda ha annunciato l'assunzione di cinquanta nuovi dipendenti entro la fine dell'anno, principalmente nell'area della ricerca e sviluppo."
        },
        {
          "type": "listen_choice",
          "q": "Cosa offre il corso?",
          "opts": [
            "Stage retribuiti",
            "Lezioni gratis",
            "Libri inclusi"
          ],
          "ans": 0,
          "script": "Il corso di formazione professionale offre stage retribuiti presso aziende partner e un certificato riconosciuto a livello europeo."
        },
        {
          "type": "listen_choice",
          "q": "Cosa dice il rapporto ISTAT?",
          "opts": [
            "Disoccupazione in calo",
            "Occupazione in aumento",
            "Inflazione stabile"
          ],
          "ans": 1,
          "script": "Secondo l'ultimo rapporto dell'ISTAT, il tasso di occupazione giovanile è aumentato del tre per cento rispetto all'anno precedente."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Di quanto si ridurranno le emissioni?",
          "text": "Il Ministero dell'Ambiente ha annunciato un nuovo piano per la riduzione delle emissioni di CO2 del 55% entro il 2030. Il piano prevede incentivi per l'acquisto di auto elettriche, l'ampliamento delle zone a traffico limitato e investimenti nelle energie rinnovabili. Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "55%",
            "30%",
            "40%"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa NON prevede il piano?",
          "text": "Il piano prevede incentivi per auto elettriche, ampliamento zone a traffico limitato e investimenti in energie rinnovabili.",
          "opts": [
            "Nuove autostrade",
            "Auto elettriche",
            "Zone a traffico limitato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa pensano le associazioni?",
          "text": "Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "Positivo ma vogliono di più",
            "Negativo",
            "Indifferente"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Credo che loro ___ (partire) ieri.",
          "hint": "congiuntivo passato",
          "ans": "siano partiti"
        },
        {
          "type": "fill",
          "q": "Sebbene ___ (piovere), siamo usciti.",
          "hint": "congiuntivo presente",
          "ans": "piova"
        },
        {
          "type": "fill",
          "q": "Benché ___ (essere) stanco, ha finito il lavoro.",
          "hint": "congiuntivo presente",
          "ans": "sia"
        },
        {
          "type": "fill",
          "q": "È importante che tu ___ (studiare) ogni giorno.",
          "hint": "congiuntivo presente",
          "ans": "studi"
        },
        {
          "type": "fill",
          "q": "Temo che non mi ___ (capire).",
          "hint": "congiuntivo presente",
          "ans": "capisca"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una lettera formale al sindaco della tua città per esprimere la tua opinione sulla creazione di una zona a traffico limitato (ZTL) in centro. Argomenta le tue ragioni pro o contro con almeno due argomenti. (150 parole)",
          "keywords": [
            "sindaco",
            "traffico",
            "centro",
            "inquinamento",
            "opinione",
            "argomento"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla dell'importanza della sostenibilità ambientale nella vita quotidiana. Cosa fai concretamente per ridurre il tuo impatto ambientale? Quali cambiamenti vorresti vedere nella tua città?",
          "keywords": [
            "ambiente",
            "sostenibilità",
            "riciclo",
            "energia",
            "città",
            "futuro"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS2_C1"] = {
  "title": "CILS CILS2 C1",
  "exam_type": "CILS",
  "set": "CILS2",
  "level": "C1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa prevede la riforma scolastica?",
          "opts": [
            "Più ore di studio",
            "Educazione finanziaria",
            "Nuovi edifici"
          ],
          "ans": 1,
          "script": "Il Ministro dell'Istruzione ha presentato oggi la riforma che prevede l'introduzione obbligatoria dell'insegnamento dell'educazione finanziaria e digitale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa investono le PMI?",
          "opts": [
            "Digitalizzazione",
            "Nuovi uffici",
            "Più dipendenti"
          ],
          "ans": 0,
          "script": "L'ultima indagine economica rivela che le piccole e medie imprese italiane investono sempre più nella digitalizzazione, con un incremento del quindici per cento."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ospita il festival?",
          "opts": [
            "Scrittori internazionali",
            "Film",
            "Musica"
          ],
          "ans": 0,
          "script": "Il festival letterario internazionale, giunto alla ventesima edizione, ospiterà scrittori da tutto il mondo, tra cui due Premi Nobel."
        },
        {
          "type": "listen_choice",
          "q": "Cosa devono ripensare le città?",
          "opts": [
            "Gli spazi pubblici",
            "I trasporti",
            "Le tasse"
          ],
          "ans": 0,
          "script": "Secondo gli esperti di urbanistica, le città italiane devono ripensare gli spazi pubblici per favorire l'aggregazione sociale e ridurre l'impatto ambientale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha approvato l'UE?",
          "opts": [
            "Un progetto italiano",
            "Un nuovo trattato",
            "Delle sanzioni"
          ],
          "ans": 0,
          "script": "La Commissione Europea ha approvato un progetto italiano per lo sviluppo di tecnologie innovative nel campo delle energie rinnovabili marine."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa suggerisce lo studio?",
          "text": "Uno studio pubblicato sulla rivista Nature Neuroscience suggerisce che l'apprendimento di una seconda lingua in età adulta può rallentare il declino cognitivo legato all'invecchiamento. I ricercatori hanno seguito 853 partecipanti per oltre 40 anni, scoprendo che i bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui. Il fenomeno sarebbe legato alla maggiore plasticità neuronale indotta dal bilinguismo.",
          "opts": [
            "Il bilinguismo rallenta il declino cognitivo",
            "Il bilinguismo accelera l'invecchiamento",
            "Non c'è alcun effetto"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti partecipanti allo studio?",
          "text": "I ricercatori hanno seguito 853 partecipanti per oltre 40 anni.",
          "opts": [
            "853",
            "583",
            "385"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti anni di ritardo nella demenza?",
          "text": "I bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui.",
          "opts": [
            "4,5 anni",
            "2 anni",
            "10 anni"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Qualora ___ (arrivare) in ritardo, avvisateci.",
          "hint": "congiuntivo imperfetto",
          "ans": "arrivaste"
        },
        {
          "type": "fill",
          "q": "Se lo ___ (sapere), te lo avrei detto.",
          "hint": "congiuntivo trapassato",
          "ans": "avessi saputo"
        },
        {
          "type": "fill",
          "q": "Nonostante ___ (avere) ragione, ha taciuto.",
          "hint": "congiuntivo imperfetto",
          "ans": "avesse"
        },
        {
          "type": "fill",
          "q": "Pur ___ (essere) ricco, vive modestamente.",
          "hint": "gerundio",
          "ans": "essendo"
        },
        {
          "type": "fill",
          "q": "Il libro di cui ti ___ (parlare) è interessante.",
          "hint": "trapassato prossimo",
          "ans": "avevo parlato"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Il governo propone di aumentare l'età pensionabile a 67 anni per tutti i lavoratori. Scrivi un articolo di opinione di circa 200 parole esprimendo la tua posizione, analizzando sia i vantaggi che gli svantaggi della proposta.",
          "keywords": [
            "pensione",
            "lavoro",
            "governo",
            "riforma",
            "vantaggi",
            "svantaggi",
            "futuro"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Discuti il fenomeno della globalizzazione analizzandone vantaggi e svantaggi per l'economia e la cultura locale italiana. Fornisci esempi concreti e una tua opinione personale.",
          "keywords": [
            "globalizzazione",
            "economia",
            "cultura",
            "commercio",
            "identità",
            "tradizione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS2_C2"] = {
  "title": "CILS CILS2 C2",
  "exam_type": "CILS",
  "set": "CILS2",
  "level": "C2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa evidenzia il rapporto digitale?",
          "opts": [
            "L'Italia è avanti",
            "L'Italia è indietro",
            "L'Italia è nella media"
          ],
          "ans": 1,
          "script": "Il rapporto annuale sull'economia digitale evidenzia che l'Italia è ancora indietro nella digitalizzazione della pubblica amministrazione rispetto alla media europea."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha annunciato il museo?",
          "opts": [
            "Una partnership col Louvre",
            "Una nuova ala",
            "Un nuovo direttore"
          ],
          "ans": 0,
          "script": "La direzione del museo ha annunciato una partnership con il Louvre per lo scambio di opere d'arte e progetti di ricerca e restauro."
        },
        {
          "type": "listen_choice",
          "q": "Cosa emerge dall'indagine?",
          "opts": [
            "Più stipendio",
            "Più flessibilità",
            "Più ferie"
          ],
          "ans": 1,
          "script": "L'indagine sociologica su duemila giovani rivela che oltre il sessanta per cento considera la flessibilità lavorativa più importante dello stipendio elevato."
        },
        {
          "type": "listen_choice",
          "q": "Cosa rappresenta il nuovo centro?",
          "opts": [
            "Un passo avanti scientifico",
            "Un costo inutile",
            "Un rischio"
          ],
          "ans": 0,
          "script": "Il nuovo centro di ricerca sulla fusione nucleare inaugurato a Frascati rappresenta un passo avanti nella collaborazione scientifica internazionale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa raccomanda l'OMS?",
          "opts": [
            "150 minuti di sport a settimana",
            "Dieta vegana",
            "8 ore di sonno"
          ],
          "ans": 0,
          "script": "L'Organizzazione Mondiale della Sanità raccomanda almeno centocinquanta minuti di attività fisica moderata a settimana per prevenire malattie cardiovascolari."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa ha dichiarato la Corte?",
          "text": "La recente sentenza della Corte Costituzionale n. 152/2023 ha dichiarato l'illegittimità costituzionale di alcune norme del codice degli appalti, ritenute lesive del principio di libera concorrenza sancito dall'articolo 41 della Costituzione. La decisione avrà ripercussioni significative sul settore delle costruzioni, dove le gare d'appalto dovranno essere riformulate per garantire maggiore trasparenza e pari opportunità tra i concorrenti.",
          "opts": [
            "Illegittimità di norme sugli appalti",
            "Legittimità delle norme",
            "Rinvio della decisione"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quale settore è più colpito?",
          "text": "La decisione avrà ripercussioni sul settore delle costruzioni, dove le gare dovranno essere riformulate per garantire maggiore trasparenza.",
          "opts": [
            "Costruzioni",
            "Sanità",
            "Istruzione"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Lungi dal ___ (voler) offendere, mi scuso.",
          "hint": "infinito",
          "ans": "volere"
        },
        {
          "type": "fill",
          "q": "Per quanto ___ (sforzarsi), non ce la fa.",
          "hint": "congiuntivo presente",
          "ans": "si sforzi"
        },
        {
          "type": "fill",
          "q": "Ove mai ___ (esserci) dubbi, contattateci.",
          "hint": "congiuntivo presente",
          "ans": "ci siano"
        },
        {
          "type": "fill",
          "q": "Al fine di ___ (evitare) disguidi, confermate.",
          "hint": "infinito",
          "ans": "evitare"
        },
        {
          "type": "fill",
          "q": "Il candidato ___ (ritenere) idoneo sarà contattato.",
          "hint": "participio passato",
          "ans": "ritenuto"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Analizza criticamente l'impatto dell'intelligenza artificiale sul mercato del lavoro italiano, considerando gli aspetti etici, economici e sociali. Fornisci esempi concreti e una tua valutazione personale. (300 parole)",
          "keywords": [
            "intelligenza artificiale",
            "lavoro",
            "etica",
            "economia",
            "società"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Analizza le conseguenze della digitalizzazione della pubblica amministrazione in Italia. Quali sono i rischi e i benefici per i cittadini? Considera aspetti come l'accessibilità, la privacy e l'inclusione digitale.",
          "keywords": [
            "digitalizzazione",
            "pubblica amministrazione",
            "cittadini",
            "privacy",
            "accessibilità",
            "inclusione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS3_A1"] = {
  "title": "CILS CILS3 A1",
  "exam_type": "CILS",
  "set": "CILS3",
  "level": "A1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa fa il signor Rossi nel weekend?",
          "opts": [
            "Gioca a calcio",
            "Va a pesca",
            "Va al cinema"
          ],
          "ans": 1,
          "script": "Il sabato il signor Rossi va sempre a pesca con suo figlio. La domenica invece legge il giornale e si prende cura del suo giardino."
        },
        {
          "type": "listen_choice",
          "q": "Dov'è la biblioteca?",
          "opts": [
            "In piazza centrale",
            "In via Garibaldi",
            "All'università"
          ],
          "ans": 1,
          "script": "La biblioteca comunale è in via Garibaldi, di fronte al parco. È aperta dal lunedì al venerdì dalle nove alle diciannove."
        },
        {
          "type": "listen_choice",
          "q": "Cosa mangia a pranzo?",
          "opts": [
            "Pasta",
            "Un'insalata con pollo",
            "Pizza"
          ],
          "ans": 1,
          "script": "Di solito a pranzo mangio un'insalata con pollo e pomodori. Qualche volta prendo anche un gelato per dessert."
        },
        {
          "type": "listen_choice",
          "q": "Perché Luca è triste?",
          "opts": [
            "Ha perso il lavoro",
            "Il suo cane è malato",
            "Ha litigato"
          ],
          "ans": 1,
          "script": "Luca è triste perché il suo cane è malato. Domani lo porterà dal veterinario per una visita approfondita."
        },
        {
          "type": "listen_choice",
          "q": "Che tempo farà?",
          "opts": [
            "Pioverà",
            "Farà bello",
            "Nevicherà"
          ],
          "ans": 1,
          "script": "Le previsioni dicono che domani farà bello con temperature intorno ai venticinque gradi. Una giornata perfetta per una gita."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Dove abita Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli con la mia famiglia. Studio medicina all'università e nel tempo libero suono la chitarra. Mi piace molto la pizza e il mare.",
          "opts": [
            "A Napoli",
            "A Roma",
            "A Milano"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa studia Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina all'università e nel tempo libero suono la chitarra.",
          "opts": [
            "Medicina",
            "Ingegneria",
            "Economia"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa piace a Marco?",
          "text": "Ciao! Mi chiamo Marco, ho 25 anni e abito a Napoli. Studio medicina e nel tempo libero suono la chitarra. Mi piace molto la pizza.",
          "opts": [
            "La pizza",
            "La pasta",
            "Il pesce"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Io ___ (essere) italiano.",
          "hint": "presente",
          "ans": "sono"
        },
        {
          "type": "fill",
          "q": "Loro ___ (avere) due cani.",
          "hint": "presente",
          "ans": "hanno"
        },
        {
          "type": "fill",
          "q": "Tu ___ (andare) a scuola in autobus.",
          "hint": "presente",
          "ans": "vai"
        },
        {
          "type": "fill",
          "q": "Noi ___ (parlare) italiano.",
          "hint": "presente",
          "ans": "parliamo"
        },
        {
          "type": "fill",
          "q": "Maria ___ (leggere) un libro.",
          "hint": "presente",
          "ans": "legge"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una breve email per presentarti a un nuovo amico italiano. Parla del tuo nome, della tua età, della tua città e dei tuoi hobby. (50-80 parole)",
          "keywords": [
            "mi chiamo",
            "anni",
            "abito",
            "mi piace",
            "hobby"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla della tua giornata tipica. Descrivi cosa fai dalla mattina alla sera (sveglia, colazione, lavoro/studio, pranzo, tempo libero, cena).",
          "keywords": [
            "sveglia",
            "colazione",
            "lavoro",
            "studio",
            "pranzo",
            "cena"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS3_A2"] = {
  "title": "CILS CILS3 A2",
  "exam_type": "CILS",
  "set": "CILS3",
  "level": "A2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Perché Maria non è venuta?",
          "opts": [
            "Era stanca",
            "Ha lavorato fino a tardi",
            "Era malata"
          ],
          "ans": 1,
          "script": "Maria non è venuta alla festa perché ha dovuto lavorare fino a tardi. Stava finendo un progetto importante per un cliente internazionale."
        },
        {
          "type": "listen_choice",
          "q": "Cosa hanno visitato a Roma?",
          "opts": [
            "Solo il Colosseo",
            "Musei e monumenti",
            "Negozi"
          ],
          "ans": 1,
          "script": "Durante il viaggio a Roma hanno visitato il Colosseo, i Musei Vaticani e la Fontana di Trevi. Sono stati tre giorni molto intensi."
        },
        {
          "type": "listen_choice",
          "q": "Dove ha studiato italiano?",
          "opts": [
            "A Siena",
            "A Roma",
            "A Milano"
          ],
          "ans": 0,
          "script": "Ho studiato italiano all'università per due anni. Poi ho frequentato un corso intensivo a Siena per un mese durante l'estate."
        },
        {
          "type": "listen_choice",
          "q": "Cosa regala a Natale?",
          "opts": [
            "Un viaggio a Parigi",
            "Un libro",
            "Un profumo"
          ],
          "ans": 0,
          "script": "Quest'anno per Natale regalo ai miei genitori un viaggio a Parigi. L'anno scorso avevo regalato una cena in un ristorante stellato."
        },
        {
          "type": "listen_choice",
          "q": "Com'era l'appartamento?",
          "opts": [
            "Grande e scuro",
            "Piccolo ma luminoso",
            "Vecchio e rumoroso"
          ],
          "ans": 1,
          "script": "L'appartamento che ho visitato era piccolo ma luminoso. Aveva due camere da letto, un soggiorno spazioso e una cucina moderna."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tempo fa al nord?",
          "text": "Le previsioni del tempo per domani: al nord nuvoloso con possibili piogge, temperature tra 8 e 15 gradi. Al centro sereno con qualche nuvola, 12-20 gradi. Al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "Nuvoloso",
            "Sereno",
            "Soleggiato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti gradi al sud?",
          "text": "Le previsioni del tempo per domani: al sud soleggiato e caldo, 18-28 gradi.",
          "opts": [
            "18-28",
            "12-20",
            "8-15"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Dov'è sereno?",
          "text": "Le previsioni del tempo per domani: al centro sereno con qualche nuvola, 12-20 gradi.",
          "opts": [
            "Al centro",
            "Al nord",
            "Al sud"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Ieri io ___ (andare) al mare.",
          "hint": "passato prossimo",
          "ans": "sono andato"
        },
        {
          "type": "fill",
          "q": "Loro ___ (finire) il lavoro.",
          "hint": "passato prossimo",
          "ans": "hanno finito"
        },
        {
          "type": "fill",
          "q": "Noi ___ (vedere) un bel film.",
          "hint": "passato prossimo",
          "ans": "abbiamo visto"
        },
        {
          "type": "fill",
          "q": "Tu ___ (comprare) il pane?",
          "hint": "passato prossimo",
          "ans": "hai comprato"
        },
        {
          "type": "fill",
          "q": "Maria ___ (arrivare) ieri sera.",
          "hint": "passato prossimo",
          "ans": "è arrivata"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una email a un albergo per prenotare una camera doppia per tre notti. Chiedi informazioni sul prezzo, sulla colazione e sul parcheggio.",
          "keywords": [
            "prenotare",
            "camera",
            "notte",
            "prezzo",
            "colazione",
            "parcheggio"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Descrivi la tua casa o il tuo appartamento. Quante stanze ci sono? Com'è la tua camera? Cosa c'è nel soggiorno? Ti piace la tua casa? Perché?",
          "keywords": [
            "casa",
            "appartamento",
            "stanza",
            "camera",
            "soggiorno",
            "cucina",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS3_B1"] = {
  "title": "CILS CILS3 B1",
  "exam_type": "CILS",
  "set": "CILS3",
  "level": "B1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Cosa ha proposto l'associazione?",
          "opts": [
            "Un mercato settimanale",
            "Una festa",
            "Un concorso"
          ],
          "ans": 0,
          "script": "Il presidente dell'associazione ha proposto di organizzare un mercato settimanale dei prodotti locali nella piazza principale del paese."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha assegnato la professoressa?",
          "opts": [
            "Un esame",
            "Una ricerca",
            "Un progetto"
          ],
          "ans": 1,
          "script": "La professoressa di storia ci ha assegnato una ricerca sulla Seconda Guerra Mondiale da consegnare entro la fine del mese prossimo."
        },
        {
          "type": "listen_choice",
          "q": "Cosa dice la recensione?",
          "opts": [
            "Il ristorante è buono",
            "Il ristorante è caro",
            "Il servizio è lento"
          ],
          "ans": 0,
          "script": "Il ristorante ha ricevuto una recensione positiva sul giornale locale per la qualità dei suoi piatti tipici della cucina toscana."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha inaugurato la palestra?",
          "opts": [
            "Una nuova area yoga",
            "Una piscina",
            "Un campo da tennis"
          ],
          "ans": 0,
          "script": "La palestra in centro ha inaugurato una nuova area dedicata allo yoga e al pilates con istruttori qualificati e attrezzature moderne."
        },
        {
          "type": "listen_choice",
          "q": "Cosa è successo ieri sera?",
          "opts": [
            "Un incendio",
            "Un furto",
            "Un incidente"
          ],
          "ans": 0,
          "script": "I vigili del fuoco sono intervenuti ieri sera per spegnere un incendio scoppiato in un appartamento al terzo piano di via Roma."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Che tipo di lavoro offre?",
          "text": "Cerchiamo un/una cameriere/a per il nostro ristorante in centro. Richiesta esperienza di almeno un anno, conoscenza base dell'inglese, disponibilità serale e nei weekend. Offriamo contratto a tempo determinato di 6 mesi con possibilità di rinnovo. Orario: 18:00-23:00. Inviare CV a lavoro@ristorante.it",
          "opts": [
            "Cameriere/a",
            "Cuoco/a",
            "Barista"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanto dura il contratto?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Richiesta esperienza di almeno un anno. Contratto 6 mesi rinnovabile.",
          "opts": [
            "6 mesi",
            "1 anno",
            "3 mesi"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Qual è l'orario di lavoro?",
          "text": "Cerchiamo cameriere/a per ristorante in centro. Offriamo contratto a tempo determinato con possibilità di rinnovo. Orario: 18:00-23:00.",
          "opts": [
            "18:00-23:00",
            "08:00-14:00",
            "12:00-18:00"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Se avessi soldi, ___ (comprare) una casa.",
          "hint": "condizionale",
          "ans": "comprerei"
        },
        {
          "type": "fill",
          "q": "Penso che lui ___ (arrivare) domani.",
          "hint": "congiuntivo presente",
          "ans": "arrivi"
        },
        {
          "type": "fill",
          "q": "Spero che voi ___ (potere) venire.",
          "hint": "congiuntivo presente",
          "ans": "possiate"
        },
        {
          "type": "fill",
          "q": "Prima di ___ (uscire), chiudi la porta.",
          "hint": "infinito",
          "ans": "uscire"
        },
        {
          "type": "fill",
          "q": "Mentre ___ (mangiare), guardava la TV.",
          "hint": "imperfetto",
          "ans": "mangiava"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi un testo di circa 100 parole in cui descrivi la tua routine quotidiana. Parla del lavoro/studio, dei pasti, del tempo libero e dei tuoi hobby.",
          "keywords": [
            "ogni",
            "mattina",
            "lavoro",
            "studio",
            "pomeriggio",
            "sera",
            "tempo libero"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla del tuo lavoro o dei tuoi studi. Cosa fai esattamente? Da quanto tempo? Cosa ti piace di più del tuo lavoro/studio? Quali sono le difficoltà? Cosa vorresti fare in futuro?",
          "keywords": [
            "lavoro",
            "studio",
            "colleghi",
            "progetti",
            "futuro",
            "mi piace"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS3_B2"] = {
  "title": "CILS CILS3 B2",
  "exam_type": "CILS",
  "set": "CILS3",
  "level": "B2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Di cosa parla la mostra?",
          "opts": [
            "Fotografia contemporanea",
            "Pittura rinascimentale",
            "Scultura moderna"
          ],
          "ans": 0,
          "script": "La mostra internazionale di fotografia contemporanea ospiterà opere di artisti provenienti da quindici paesi diversi."
        },
        {
          "type": "listen_choice",
          "q": "Cosa prevede il progetto urbano?",
          "opts": [
            "Piste ciclabili e aree verdi",
            "Un nuovo stadio",
            "Un centro commerciale"
          ],
          "ans": 0,
          "script": "Il progetto di riqualificazione urbana prevede la creazione di nuove piste ciclabili, aree verdi e spazi pedonali nel centro della città."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha attivato l'università?",
          "opts": [
            "Un master in IA medica",
            "Un corso di cucina",
            "Un dottorato"
          ],
          "ans": 0,
          "script": "L'università ha attivato un nuovo master in Intelligenza Artificiale applicata alla medicina, con borse di studio per studenti meritevoli."
        },
        {
          "type": "listen_choice",
          "q": "Cosa organizza la fondazione?",
          "opts": [
            "Conferenze su etica e IA",
            "Un festival musicale",
            "Un premio letterario"
          ],
          "ans": 0,
          "script": "La fondazione culturale organizza un ciclo di conferenze sul rapporto tra etica e intelligenza artificiale con relatori internazionali."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha approvato il consiglio?",
          "opts": [
            "Il bilancio previsionale",
            "Un nuovo regolamento",
            "Una tassa"
          ],
          "ans": 0,
          "script": "Il consiglio comunale ha approvato all'unanimità il bilancio che destina il quaranta per cento delle risorse all'istruzione e ai servizi sociali."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Di quanto si ridurranno le emissioni?",
          "text": "Il Ministero dell'Ambiente ha annunciato un nuovo piano per la riduzione delle emissioni di CO2 del 55% entro il 2030. Il piano prevede incentivi per l'acquisto di auto elettriche, l'ampliamento delle zone a traffico limitato e investimenti nelle energie rinnovabili. Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "55%",
            "30%",
            "40%"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa NON prevede il piano?",
          "text": "Il piano prevede incentivi per auto elettriche, ampliamento zone a traffico limitato e investimenti in energie rinnovabili.",
          "opts": [
            "Nuove autostrade",
            "Auto elettriche",
            "Zone a traffico limitato"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Cosa pensano le associazioni?",
          "text": "Le associazioni ambientaliste hanno accolto positivamente la notizia, pur chiedendo obiettivi ancora più ambiziosi.",
          "opts": [
            "Positivo ma vogliono di più",
            "Negativo",
            "Indifferente"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Credo che loro ___ (partire) ieri.",
          "hint": "congiuntivo passato",
          "ans": "siano partiti"
        },
        {
          "type": "fill",
          "q": "Sebbene ___ (piovere), siamo usciti.",
          "hint": "congiuntivo presente",
          "ans": "piova"
        },
        {
          "type": "fill",
          "q": "Benché ___ (essere) stanco, ha finito il lavoro.",
          "hint": "congiuntivo presente",
          "ans": "sia"
        },
        {
          "type": "fill",
          "q": "È importante che tu ___ (studiare) ogni giorno.",
          "hint": "congiuntivo presente",
          "ans": "studi"
        },
        {
          "type": "fill",
          "q": "Temo che non mi ___ (capire).",
          "hint": "congiuntivo presente",
          "ans": "capisca"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Scrivi una lettera formale al sindaco della tua città per esprimere la tua opinione sulla creazione di una zona a traffico limitato (ZTL) in centro. Argomenta le tue ragioni pro o contro con almeno due argomenti. (150 parole)",
          "keywords": [
            "sindaco",
            "traffico",
            "centro",
            "inquinamento",
            "opinione",
            "argomento"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Parla dell'importanza della sostenibilità ambientale nella vita quotidiana. Cosa fai concretamente per ridurre il tuo impatto ambientale? Quali cambiamenti vorresti vedere nella tua città?",
          "keywords": [
            "ambiente",
            "sostenibilità",
            "riciclo",
            "energia",
            "città",
            "futuro"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS3_C1"] = {
  "title": "CILS CILS3 C1",
  "exam_type": "CILS",
  "set": "CILS3",
  "level": "C1",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Dov'è l'Italia nella digitalizzazione?",
          "opts": [
            "Avanzata",
            "In ritardo",
            "Nella media"
          ],
          "ans": 1,
          "script": "Il rapporto evidenzia che l'Italia è ancora indietro nella digitalizzazione della PA rispetto alla media europea, nonostante i progressi recenti."
        },
        {
          "type": "listen_choice",
          "q": "Con chi collabora il museo?",
          "opts": [
            "Col Louvre",
            "Col British Museum",
            "Col Prado"
          ],
          "ans": 0,
          "script": "La direzione del museo ha annunciato una partnership con il Louvre per lo scambio di opere e la collaborazione su progetti di restauro."
        },
        {
          "type": "listen_choice",
          "q": "Cosa preferiscono i giovani?",
          "opts": [
            "Flessibilità lavorativa",
            "Alto stipendio",
            "Carriera veloce"
          ],
          "ans": 0,
          "script": "L'indagine rivela che oltre il sessanta per cento dei giovani intervistati considera la flessibilità lavorativa più importante dello stipendio."
        },
        {
          "type": "listen_choice",
          "q": "Dov'è il nuovo centro di ricerca?",
          "opts": [
            "A Frascati",
            "A Milano",
            "A Bologna"
          ],
          "ans": 0,
          "script": "Il nuovo centro di ricerca sulla fusione nucleare inaugurato oggi a Frascati rappresenta un passo avanti nella collaborazione scientifica internazionale."
        },
        {
          "type": "listen_choice",
          "q": "Quanto sport raccomanda l'OMS?",
          "opts": [
            "150 minuti a settimana",
            "30 minuti al giorno",
            "2 ore al giorno"
          ],
          "ans": 0,
          "script": "L'OMS raccomanda almeno centocinquanta minuti di attività fisica moderata a settimana per la prevenzione di malattie cardiovascolari."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa suggerisce lo studio?",
          "text": "Uno studio pubblicato sulla rivista Nature Neuroscience suggerisce che l'apprendimento di una seconda lingua in età adulta può rallentare il declino cognitivo legato all'invecchiamento. I ricercatori hanno seguito 853 partecipanti per oltre 40 anni, scoprendo che i bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui. Il fenomeno sarebbe legato alla maggiore plasticità neuronale indotta dal bilinguismo.",
          "opts": [
            "Il bilinguismo rallenta il declino cognitivo",
            "Il bilinguismo accelera l'invecchiamento",
            "Non c'è alcun effetto"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti partecipanti allo studio?",
          "text": "I ricercatori hanno seguito 853 partecipanti per oltre 40 anni.",
          "opts": [
            "853",
            "583",
            "385"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quanti anni di ritardo nella demenza?",
          "text": "I bilingui mostravano sintomi di demenza in media 4,5 anni più tardi rispetto ai monolingui.",
          "opts": [
            "4,5 anni",
            "2 anni",
            "10 anni"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Qualora ___ (arrivare) in ritardo, avvisateci.",
          "hint": "congiuntivo imperfetto",
          "ans": "arrivaste"
        },
        {
          "type": "fill",
          "q": "Se lo ___ (sapere), te lo avrei detto.",
          "hint": "congiuntivo trapassato",
          "ans": "avessi saputo"
        },
        {
          "type": "fill",
          "q": "Nonostante ___ (avere) ragione, ha taciuto.",
          "hint": "congiuntivo imperfetto",
          "ans": "avesse"
        },
        {
          "type": "fill",
          "q": "Pur ___ (essere) ricco, vive modestamente.",
          "hint": "gerundio",
          "ans": "essendo"
        },
        {
          "type": "fill",
          "q": "Il libro di cui ti ___ (parlare) è interessante.",
          "hint": "trapassato prossimo",
          "ans": "avevo parlato"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Il governo propone di aumentare l'età pensionabile a 67 anni per tutti i lavoratori. Scrivi un articolo di opinione di circa 200 parole esprimendo la tua posizione, analizzando sia i vantaggi che gli svantaggi della proposta.",
          "keywords": [
            "pensione",
            "lavoro",
            "governo",
            "riforma",
            "vantaggi",
            "svantaggi",
            "futuro"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Discuti il fenomeno della globalizzazione analizzandone vantaggi e svantaggi per l'economia e la cultura locale italiana. Fornisci esempi concreti e una tua opinione personale.",
          "keywords": [
            "globalizzazione",
            "economia",
            "cultura",
            "commercio",
            "identità",
            "tradizione"
          ]
        }
      ]
    }
  ]
}

EXAMS["CILS3_C2"] = {
  "title": "CILS CILS3 C2",
  "exam_type": "CILS",
  "set": "CILS3",
  "level": "C2",
  "sections": [
    {
      "id": "ascolto",
      "title": "Ascolto",
      "max_points": 20,
      "items": [
        {
          "type": "listen_choice",
          "q": "Di cosa ha parlato il Nobel?",
          "opts": [
            "Meccanica quantistica e coscienza",
            "Buchi neri",
            "Energia nucleare"
          ],
          "ans": 0,
          "script": "Il premio Nobel per la fisica ha tenuto una lectio magistralis sul rapporto tra meccanica quantistica e coscienza, suscitando un vivace dibattito."
        },
        {
          "type": "listen_choice",
          "q": "Cosa ha stabilito la Corte?",
          "opts": [
            "Principi sulla privacy digitale",
            "Nuove leggi",
            "Divieti"
          ],
          "ans": 0,
          "script": "La Corte Costituzionale si è pronunciata sulla legittimità delle nuove norme in materia di privacy digitale, stabilendo principi importanti per la tutela dei dati."
        },
        {
          "type": "listen_choice",
          "q": "Dov'è l'Italia nella mobilità sociale?",
          "opts": [
            "Ultime posizioni",
            "Prime posizioni",
            "A metà classifica"
          ],
          "ans": 0,
          "script": "L'indagine dell'OCSE sulla mobilità sociale colloca l'Italia nelle ultime posizioni per equità di opportunità tra generazioni."
        },
        {
          "type": "listen_choice",
          "q": "Di cosa ha discusso il festival?",
          "opts": [
            "Etica dell'editing genetico",
            "Cambiamento climatico",
            "Intelligenza artificiale"
          ],
          "ans": 0,
          "script": "Il festival della scienza ha ospitato un dibattito sulle implicazioni etiche dell'editing genetico con biologi, filosofi e giuristi."
        },
        {
          "type": "listen_choice",
          "q": "Cosa analizza Foreign Affairs?",
          "opts": [
            "La transizione multipolare",
            "La crisi economica",
            "Il riscaldamento globale"
          ],
          "ans": 0,
          "script": "L'analisi geopolitica pubblicata su Foreign Affairs esamina le conseguenze della transizione multipolare sugli equilibri di potere globali."
        }
      ]
    },
    {
      "id": "lettura",
      "title": "Lettura",
      "max_points": 20,
      "items": [
        {
          "type": "read_choice",
          "q": "Cosa ha dichiarato la Corte?",
          "text": "La recente sentenza della Corte Costituzionale n. 152/2023 ha dichiarato l'illegittimità costituzionale di alcune norme del codice degli appalti, ritenute lesive del principio di libera concorrenza sancito dall'articolo 41 della Costituzione. La decisione avrà ripercussioni significative sul settore delle costruzioni, dove le gare d'appalto dovranno essere riformulate per garantire maggiore trasparenza e pari opportunità tra i concorrenti.",
          "opts": [
            "Illegittimità di norme sugli appalti",
            "Legittimità delle norme",
            "Rinvio della decisione"
          ],
          "ans": 0
        },
        {
          "type": "read_choice",
          "q": "Quale settore è più colpito?",
          "text": "La decisione avrà ripercussioni sul settore delle costruzioni, dove le gare dovranno essere riformulate per garantire maggiore trasparenza.",
          "opts": [
            "Costruzioni",
            "Sanità",
            "Istruzione"
          ],
          "ans": 0
        }
      ]
    },
    {
      "id": "grammatica",
      "title": "Grammatica",
      "max_points": 20,
      "items": [
        {
          "type": "fill",
          "q": "Lungi dal ___ (voler) offendere, mi scuso.",
          "hint": "infinito",
          "ans": "volere"
        },
        {
          "type": "fill",
          "q": "Per quanto ___ (sforzarsi), non ce la fa.",
          "hint": "congiuntivo presente",
          "ans": "si sforzi"
        },
        {
          "type": "fill",
          "q": "Ove mai ___ (esserci) dubbi, contattateci.",
          "hint": "congiuntivo presente",
          "ans": "ci siano"
        },
        {
          "type": "fill",
          "q": "Al fine di ___ (evitare) disguidi, confermate.",
          "hint": "infinito",
          "ans": "evitare"
        },
        {
          "type": "fill",
          "q": "Il candidato ___ (ritenere) idoneo sarà contattato.",
          "hint": "participio passato",
          "ans": "ritenuto"
        }
      ]
    },
    {
      "id": "scrittura",
      "title": "Scrittura/Oralità",
      "max_points": 20,
      "items": [
        {
          "type": "write",
          "q": "Analizza criticamente l'impatto dell'intelligenza artificiale sul mercato del lavoro italiano, considerando gli aspetti etici, economici e sociali. Fornisci esempi concreti e una tua valutazione personale. (300 parole)",
          "keywords": [
            "intelligenza artificiale",
            "lavoro",
            "etica",
            "economia",
            "società"
          ]
        }
      ]
    },
    {
      "id": "orale",
      "title": "Produzione Orale",
      "max_points": 20,
      "items": [
        {
          "type": "speak",
          "q": "Analizza le conseguenze della digitalizzazione della pubblica amministrazione in Italia. Quali sono i rischi e i benefici per i cittadini? Considera aspetti come l'accessibilità, la privacy e l'inclusione digitale.",
          "keywords": [
            "digitalizzazione",
            "pubblica amministrazione",
            "cittadini",
            "privacy",
            "accessibilità",
            "inclusione"
          ]
        }
      ]
    }
  ]
}


def generate_exam_html(exam_key, exam_data):

    # Original layout CSS and JS (from video reference)
    _orig_css = base64.b64decode("KiB7IGJveC1zaXppbmc6IGJvcmRlci1ib3g7IH0NCiAgYm9keSB7IGZvbnQtZmFtaWx5OiAnU2Vnb2UgVUknLCBzeXN0ZW0tdWksIHNhbnMtc2VyaWY7IG1heC13aWR0aDogOTAwcHg7IG1hcmdpbjogMCBhdXRvOyBwYWRkaW5nOiAzMHB4IDIwcHg7IGJhY2tncm91bmQ6ICNmOGY5ZmE7IGNvbG9yOiAjMjIyOyB9DQogIC5oZWFkZXIgeyBiYWNrZ3JvdW5kOiBsaW5lYXItZ3JhZGllbnQoMTM1ZGVnLCAjMWE1Mjc2LCAjMmU4NmMxKTsgY29sb3I6IHdoaXRlOyBwYWRkaW5nOiAyNXB4OyBib3JkZXItcmFkaXVzOiAxMnB4OyBtYXJnaW4tYm90dG9tOiAyNXB4OyB9DQogIC5oZWFkZXIgaDEgeyBtYXJnaW46IDA7IGZvbnQtc2l6ZTogMjJweDsgfQ0KICAuaGVhZGVyIHAgeyBtYXJnaW46IDVweCAwIDA7IG9wYWNpdHk6IC44NTsgZm9udC1zaXplOiAxM3B4OyB9DQogIC5zZWN0aW9uIHsgYmFja2dyb3VuZDogd2hpdGU7IGJvcmRlci1yYWRpdXM6IDEwcHg7IHBhZGRpbmc6IDIwcHg7IG1hcmdpbi1ib3R0b206IDIwcHg7IGJveC1zaGFkb3c6IDAgMXB4IDRweCByZ2JhKDAsMCwwLC4wOCk7IH0NCiAgLnNlY3Rpb24gaDIgeyBmb250LXNpemU6IDE2cHg7IGNvbG9yOiAjMWE1Mjc2OyBtYXJnaW46IDAgMCAxNXB4OyBwYWRkaW5nLWJvdHRvbTogOHB4OyBib3JkZXItYm90dG9tOiAycHggc29saWQgIzFhNTI3NjsgfQ0KICAucXVlc3Rpb24geyBtYXJnaW46IDE2cHggMDsgcGFkZGluZzogMTJweDsgYm9yZGVyLXJhZGl1czogOHB4OyBiYWNrZ3JvdW5kOiAjZjhmYmZmOyB9DQogIC5xdWVzdGlvbi5zdGVtIHsgYmFja2dyb3VuZDogI2ZmZjhlMTsgfQ0KICAucmVhZC10ZXh0IHsgYmFja2dyb3VuZDogI2YwZjBmMDsgcGFkZGluZzogMTVweDsgYm9yZGVyLXJhZGl1czogOHB4OyBtYXJnaW46IDEwcHggMDsgZm9udC1zaXplOiAxNHB4OyBsaW5lLWhlaWdodDogMS43OyB9DQogIC5vcHRzIHsgbWFyZ2luOiA4cHggMDsgfQ0KICAub3B0cyBsYWJlbCB7IGRpc3BsYXk6IGJsb2NrOyBwYWRkaW5nOiA2cHggMTBweDsgYm9yZGVyLXJhZGl1czogNnB4OyBjdXJzb3I6IHBvaW50ZXI7IHRyYW5zaXRpb246IGJhY2tncm91bmQgLjE1czsgfQ0KICAub3B0cyBsYWJlbDpob3ZlciB7IGJhY2tncm91bmQ6ICNlOGYwZmU7IH0NCiAgLm9wdHMgaW5wdXRbdHlwZT0icmFkaW8iXSB7IG1hcmdpbi1yaWdodDogOHB4OyB9DQogIC5maWxsLWlucHV0IHsgcGFkZGluZzogNnB4IDEwcHg7IGJvcmRlcjogMXB4IHNvbGlkICNjY2M7IGJvcmRlci1yYWRpdXM6IDRweDsgZm9udC1zaXplOiAxNHB4OyB3aWR0aDogMjAwcHg7IH0NCiAgLmZpbGwtaW5wdXQ6Zm9jdXMgeyBib3JkZXItY29sb3I6ICMxYTUyNzY7IG91dGxpbmU6IG5vbmU7IGJveC1zaGFkb3c6IDAgMCAwIDJweCByZ2JhKDI2LDgyLDExOCwuMik7IH0NCiAgLndyaXRpbmctYXJlYSB7IHdpZHRoOiAxMDAlOyBtaW4taGVpZ2h0OiAxMjBweDsgcGFkZGluZzogMTJweDsgYm9yZGVyOiAxcHggc29saWQgI2NjYzsgYm9yZGVyLXJhZGl1czogOHB4OyBmb250LXNpemU6IDE0cHg7IGxpbmUtaGVpZ2h0OiAxLjY7IGZvbnQtZmFtaWx5OiBpbmhlcml0OyByZXNpemU6IHZlcnRpY2FsOyB9DQogIC53cml0aW5nLWFyZWE6Zm9jdXMgeyBib3JkZXItY29sb3I6ICM3YjFmYTI7IG91dGxpbmU6IG5vbmU7IH0NCiAgLnBsYXktYnRuIHsgZGlzcGxheTogaW5saW5lLWZsZXg7IGFsaWduLWl0ZW1zOiBjZW50ZXI7IGdhcDogNnB4OyBwYWRkaW5nOiA2cHggMTRweDsgYmFja2dyb3VuZDogI2U4ZjVlOTsgY29sb3I6ICMyZTdkMzI7IGJvcmRlcjogMXB4IHNvbGlkICNhNWQ2YTc7IGJvcmRlci1yYWRpdXM6IDIwcHg7IGN1cnNvcjogcG9pbnRlcjsgZm9udC1zaXplOiAxM3B4OyBtYXJnaW4tYm90dG9tOiA4cHg7IHRyYW5zaXRpb246IGFsbCAuMTVzOyB9DQogIC5wbGF5LWJ0bjpob3ZlciB7IGJhY2tncm91bmQ6ICNjOGU2Yzk7IH0NCiAgLnBsYXktYnRuLnBsYXlpbmcgeyBiYWNrZ3JvdW5kOiAjZmZmM2NkOyBib3JkZXItY29sb3I6ICNmZmMxMDc7IGNvbG9yOiAjODU2NDA0OyB9DQogIC5wbGF5LWJ0bi5sb2FkaW5nIHsgYmFja2dyb3VuZDogI2UzZjJmZDsgYm9yZGVyLWNvbG9yOiAjOTBjYWY5OyBjb2xvcjogIzE1NjVjMDsgfQ0KICAuc2NvcmUtYmFyIHsgYmFja2dyb3VuZDogbGluZWFyLWdyYWRpZW50KDEzNWRlZywgIzI3YWU2MCwgIzJlY2M3MSk7IGNvbG9yOiB3aGl0ZTsgcGFkZGluZzogMjBweDsgYm9yZGVyLXJhZGl1czogMTJweDsgdGV4dC1hbGlnbjogY2VudGVyOyBtYXJnaW4tYm90dG9tOiAyMHB4OyBkaXNwbGF5OiBub25lOyB9DQogIC5zY29yZS1iYXIgaDIgeyBtYXJnaW46IDA7IGZvbnQtc2l6ZTogMjhweDsgfQ0KICAuc2NvcmUtYmFyIHAgeyBtYXJnaW46IDVweCAwIDA7IGZvbnQtc2l6ZTogMTRweDsgfQ0KICAuYnRuLXN1Ym1pdCB7IHBhZGRpbmc6IDEycHggNDBweDsgYmFja2dyb3VuZDogbGluZWFyLWdyYWRpZW50KDEzNWRlZywgIzFhNTI3NiwgIzJlODZjMSk7IGNvbG9yOiB3aGl0ZTsgYm9yZGVyOiBub25lOyBib3JkZXItcmFkaXVzOiA4cHg7IGZvbnQtc2l6ZTogMTZweDsgY3Vyc29yOiBwb2ludGVyOyB9DQogIC5idG4tc3VibWl0OmhvdmVyIHsgb3BhY2l0eTogLjk7IH0NCiAgLmJ0bi1yZXNldCB7IHBhZGRpbmc6IDEwcHggMzBweDsgYmFja2dyb3VuZDogd2hpdGU7IGNvbG9yOiAjNjY2OyBib3JkZXI6IDFweCBzb2xpZCAjY2NjOyBib3JkZXItcmFkaXVzOiA4cHg7IGZvbnQtc2l6ZTogMTRweDsgY3Vyc29yOiBwb2ludGVyOyBtYXJnaW4tbGVmdDogMTBweDsgfQ0KICAuZmVlZGJhY2sgeyBkaXNwbGF5OiBub25lOyBtYXJnaW4tdG9wOiA4cHg7IHBhZGRpbmc6IDZweCAxMHB4OyBib3JkZXItcmFkaXVzOiA0cHg7IGZvbnQtc2l6ZTogMTNweDsgfQ0KICAuZmVlZGJhY2suY29ycmVjdCB7IGJhY2tncm91bmQ6ICNlOGY1ZTk7IGNvbG9yOiAjMmU3ZDMyOyBkaXNwbGF5OiBibG9jazsgfQ0KICAuZmVlZGJhY2sud3JvbmcgeyBiYWNrZ3JvdW5kOiAjZmZlYmVlOyBjb2xvcjogI2M2MjgyODsgZGlzcGxheTogYmxvY2s7IH0NCiAgLmhpbnQgeyBmb250LXNpemU6IDEycHg7IGNvbG9yOiAjODg4OyBtYXJnaW4tbGVmdDogNHB4OyB9DQogIC5zZWN0aW9uLXNjb3JlIHsgbWFyZ2luLXRvcDogMTBweDsgcGFkZGluZzogOHB4OyBiYWNrZ3JvdW5kOiAjZjVmNWY1OyBib3JkZXItcmFkaXVzOiA2cHg7IHRleHQtYWxpZ246IHJpZ2h0OyBmb250LXNpemU6IDEzcHg7IGNvbG9yOiAjNjY2OyBkaXNwbGF5OiBub25lOyB9DQogIC5kZXRhaWwtdGFibGUgeyB3aWR0aDogMTAwJTsgbWFyZ2luLXRvcDogMjBweDsgYm9yZGVyLWNvbGxhcHNlOiBjb2xsYXBzZTsgZm9udC1zaXplOiAxM3B4OyB9DQogIC5kZXRhaWwtdGFibGUgdGgsIC5kZXRhaWwtdGFibGUgdGQgeyBwYWRkaW5nOiA4cHggMTJweDsgYm9yZGVyOiAxcHggc29saWQgI2RkZDsgdGV4dC1hbGlnbjogbGVmdDsgfQ0KICAuZGV0YWlsLXRhYmxlIHRoIHsgYmFja2dyb3VuZDogI2YwZjBmMDsgfQ0KICAuZGV0YWlsLXRhYmxlIC5wYXNzIHsgY29sb3I6ICMyZTdkMzI7IGZvbnQtd2VpZ2h0OiBib2xkOyB9DQogIC5kZXRhaWwtdGFibGUgLmZhaWwgeyBjb2xvcjogI2M2MjgyODsgZm9udC13ZWlnaHQ6IGJvbGQ7IH0NCiAgLnJlZi10YWJsZSB7IHdpZHRoOiAxMDAlOyBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOyBmb250LXNpemU6IDEycHg7IG1hcmdpbi10b3A6IDhweDsgfQ0KICAucmVmLXRhYmxlIHRoLCAucmVmLXRhYmxlIHRkIHsgcGFkZGluZzogNnB4IDhweDsgYm9yZGVyOiAxcHggc29saWQgI2UwZTBlMDsgdGV4dC1hbGlnbjogbGVmdDsgfQ0KICAucmVmLXRhYmxlIHRoIHsgYmFja2dyb3VuZDogI2Y1ZjVmNTsgZm9udC13ZWlnaHQ6IDUwMDsgfQ0KICAucmVmLXRhYmxlIHRyLnJlZi1jb3JyIHRkIHsgYmFja2dyb3VuZDogI2YxZjhlOTsgfQ0KICAucmVmLXRhYmxlIHRyLnJlZi13cm9uZyB0ZCB7IGJhY2tncm91bmQ6ICNmZmYzZjA7IH0KCi5zY3JpcHQtYnRuIHsgcGFkZGluZzogM3B4IDEwcHg7IGJhY2tncm91bmQ6ICNmZmY4ZTE7IGJvcmRlcjogMXB4IHNvbGlkICNmZmMxMDc7IGJvcmRlci1yYWRpdXM6IDE2cHg7IGN1cnNvcjogcG9pbnRlcjsgZm9udC1zaXplOiAxMXB4OyB2ZXJ0aWNhbC1hbGlnbjogbWlkZGxlOyBtYXJnaW4tbGVmdDogNHB4OyB9Ci5zY3JpcHQtYnRuOmhvdmVyIHsgYmFja2dyb3VuZDogI2ZmZWNiMzsgfQouc2NyaXB0LXRleHQgeyBtYXJnaW4tdG9wOiA4cHg7IHBhZGRpbmc6IDEwcHg7IGJhY2tncm91bmQ6ICNmZmY4ZTE7IGJvcmRlci1yYWRpdXM6IDZweDsgZm9udC1zaXplOiAxM3B4OyBsaW5lLWhlaWdodDogMS42OyBib3JkZXItbGVmdDogM3B4IHNvbGlkICNmZmMxMDc7IH0=").decode("utf-8")
    _orig_js = base64.b64decode("dmFyIF9hdWRpb0N0eCA9IG51bGw7DQpmdW5jdGlvbiBfZ2V0QXVkaW9DdHgoKSB7DQogIGlmICghX2F1ZGlvQ3R4KSBfYXVkaW9DdHggPSBuZXcgKHdpbmRvdy5BdWRpb0NvbnRleHQgfHwgd2luZG93LndlYmtpdEF1ZGlvQ29udGV4dCkoKTsNCiAgcmV0dXJuIF9hdWRpb0N0eDsNCn0NCg0KZnVuY3Rpb24gX3N0b3BDdXJyZW50KCkgew0KICBpZiAod2luZG93Ll9jdXJTb3VyY2UpIHsNCiAgICB0cnkgeyBfY3VyU291cmNlLnN0b3AoKTsgfSBjYXRjaChlKSB7fQ0KICAgIHdpbmRvdy5fY3VyU291cmNlID0gbnVsbDsNCiAgfQ0KICBpZiAod2luZG93Ll9jdXJCdG4pIHsNCiAgICB3aW5kb3cuX2N1ckJ0bi5jbGFzc0xpc3QucmVtb3ZlKCdwbGF5aW5nJyk7DQogICAgd2luZG93Ll9jdXJCdG4uaW5uZXJIVE1MID0gJ+KWtiBBc2NvbHRhJzsNCiAgICB3aW5kb3cuX2N1ckJ0biA9IG51bGw7DQogIH0NCn0NCg0KdmFyIF9hdWRpb0dlbiA9IDA7DQoNCmZ1bmN0aW9uIHBsYXlBdWRpbyhidG4pIHsNCiAgdmFyIHNyYyA9IGJ0bi5nZXRBdHRyaWJ1dGUoJ2RhdGEtYXVkaW8tc3JjJyk7DQogIGlmICghc3JjKSB7IGNvbnNvbGUuZXJyb3IoJ05vIGF1ZGlvIHNvdXJjZScpOyByZXR1cm47IH0NCiAgDQogIC8vIElmIHRoaXMgYnV0dG9uIGlzIGFscmVhZHkgcGxheWluZywgc3RvcCBpdA0KICBpZiAoYnRuLmNsYXNzTGlzdC5jb250YWlucygncGxheWluZycpKSB7IF9zdG9wQ3VycmVudCgpOyByZXR1cm47IH0NCiAgDQogIC8vIFN0b3AgcHJldmlvdXMgYW5kIG1hcmsgdGhpcyBhcyBsYXRlc3QNCiAgX3N0b3BDdXJyZW50KCk7DQogIHZhciBteUdlbiA9ICsrX2F1ZGlvR2VuOw0KICANCiAgYnRuLmNsYXNzTGlzdC5hZGQoJ2xvYWRpbmcnKTsNCiAgYnRuLmlubmVySFRNTCA9ICfij7MuLi4nOw0KICANCiAgZmV0Y2goc3JjKQ0KICAgIC50aGVuKGZ1bmN0aW9uKHIpIHsNCiAgICAgIGlmICghci5vaykgdGhyb3cgbmV3IEVycm9yKCdIVFRQICcgKyByLnN0YXR1cyk7DQogICAgICByZXR1cm4gci5hcnJheUJ1ZmZlcigpOw0KICAgIH0pDQogICAgLnRoZW4oZnVuY3Rpb24oYnVmKSB7DQogICAgICBpZiAobXlHZW4gIT09IF9hdWRpb0dlbikgcmV0dXJuOyAgLy8gQW5vdGhlciBidXR0b24gd2FzIGNsaWNrZWQsIGRpc2NhcmQNCiAgICAgIHZhciBjdHggPSBfZ2V0QXVkaW9DdHgoKTsNCiAgICAgIGlmIChjdHguc3RhdGUgPT09ICdzdXNwZW5kZWQnKSBjdHgucmVzdW1lKCk7DQogICAgICBjdHguZGVjb2RlQXVkaW9EYXRhKGJ1ZiwgZnVuY3Rpb24oYnVmZmVyKSB7DQogICAgICAgIGlmIChteUdlbiAhPT0gX2F1ZGlvR2VuKSByZXR1cm47ICAvLyBDaGVjayBhZ2FpbiBhZnRlciBkZWNvZGUNCiAgICAgICAgdmFyIHNvdXJjZSA9IGN0eC5jcmVhdGVCdWZmZXJTb3VyY2UoKTsNCiAgICAgICAgc291cmNlLmJ1ZmZlciA9IGJ1ZmZlcjsNCiAgICAgICAgc291cmNlLmNvbm5lY3QoY3R4LmRlc3RpbmF0aW9uKTsNCiAgICAgICAgc291cmNlLnN0YXJ0KDApOw0KICAgICAgICB3aW5kb3cuX2N1clNvdXJjZSA9IHNvdXJjZTsNCiAgICAgICAgd2luZG93Ll9jdXJCdG4gPSBidG47DQogICAgICAgIGJ0bi5jbGFzc0xpc3QucmVtb3ZlKCdsb2FkaW5nJyk7DQogICAgICAgIGJ0bi5jbGFzc0xpc3QuYWRkKCdwbGF5aW5nJyk7DQogICAgICAgIGJ0bi5pbm5lckhUTUwgPSAn4o+5IEZlcm1hJzsNCiAgICAgICAgc291cmNlLm9uZW5kZWQgPSBmdW5jdGlvbigpIHsgX3N0b3BDdXJyZW50KCk7IH07DQogICAgICB9LCBmdW5jdGlvbihlcnIpIHsNCiAgICAgICAgY29uc29sZS5lcnJvcignRGVjb2RlIGZhaWxlZDonLCBlcnIpOw0KICAgICAgICBidG4uY2xhc3NMaXN0LnJlbW92ZSgnbG9hZGluZycpOw0KICAgICAgICBidG4uaW5uZXJIVE1MID0gJ+KdjCc7DQogICAgICAgIHNldFRpbWVvdXQoZnVuY3Rpb24oKSB7IGJ0bi5pbm5lckhUTUwgPSAn4pa2IFJpcHJvdmEnOyB9LCAyMDAwKTsNCiAgICAgIH0pOw0KICAgIH0pDQogICAgLmNhdGNoKGZ1bmN0aW9uKGVycikgew0KICAgICAgY29uc29sZS5lcnJvcignRmV0Y2ggZmFpbGVkOicsIGVycik7DQogICAgICBidG4uY2xhc3NMaXN0LnJlbW92ZSgnbG9hZGluZycpOw0KICAgICAgYnRuLmlubmVySFRNTCA9ICfinYwnOw0KICAgICAgc2V0VGltZW91dChmdW5jdGlvbigpIHsgYnRuLmlubmVySFRNTCA9ICfilrYgUmlwcm92YSc7IH0sIDIwMDApOw0KICAgIH0pOw0KfQ0KDQpmdW5jdGlvbiBub3JtYWxpemUocykgew0KICByZXR1cm4gcy50b0xvd2VyQ2FzZSgpLnJlcGxhY2UoL1tccyfCtFxg4oCY4oCZXC5dKy9nLCAnICcpLnRyaW0oKTsNCn0NCg0KZnVuY3Rpb24ga2V5d29yZFNjb3JlKHRleHQsIGtleXdvcmRzKSB7DQogIGlmICghdGV4dCB8fCB0ZXh0LnRyaW0oKS5sZW5ndGggPCAxMCkgcmV0dXJuIDA7DQogIHZhciB0ID0gdGV4dC50b0xvd2VyQ2FzZSgpOw0KICB2YXIgZm91bmQgPSAwOw0KICBmb3IgKHZhciBrIG9mIGtleXdvcmRzKSB7DQogICAgaWYgKHQuaW5jbHVkZXMoay50b0xvd2VyQ2FzZSgpKSkgZm91bmQrKzsNCiAgfQ0KICB2YXIgdG90YWwgPSBrZXl3b3Jkcy5sZW5ndGg7DQogIHZhciByYXRpbyA9IGZvdW5kIC8gdG90YWw7DQogIGlmIChyYXRpbyA+PSAwLjYpIHJldHVybiAyMDsNCiAgaWYgKHJhdGlvID49IDAuNCkgcmV0dXJuIDE1Ow0KICBpZiAocmF0aW8gPj0gMC4yKSByZXR1cm4gMTA7DQogIGlmIChmb3VuZCA+IDApIHJldHVybiA1Ow0KICByZXR1cm4gMDsNCn0NCg0KZnVuY3Rpb24gd29yZENvdW50KHRleHQpIHsNCiAgcmV0dXJuIHRleHQudHJpbSgpLnNwbGl0KC9ccysvKS5maWx0ZXIodyA9PiB3Lmxlbmd0aCA+IDApLmxlbmd0aDsNCn0NCg0KLy8gUHJlbG9hZCBmaXJzdCBhdWRpbyBzaWxlbnRseQ0KKGZ1bmN0aW9uKCkgew0KICB2YXIgZmlyc3RBdWRpbyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJ1tkYXRhLWF1ZGlvLXNyY10nKTsNCiAgaWYgKGZpcnN0QXVkaW8pIHsNCiAgICB2YXIgc3JjID0gZmlyc3RBdWRpby5nZXRBdHRyaWJ1dGUoJ2RhdGEtYXVkaW8tc3JjJyk7DQogICAgdmFyIHhociA9IG5ldyBYTUxIdHRwUmVxdWVzdCgpOw0KICAgIHhoci5vcGVuKCdHRVQnLCBzcmMsIHRydWUpOw0KICAgIHhoci5yZXNwb25zZVR5cGUgPSAnYXJyYXlidWZmZXInOw0KICAgIHhoci5zZW5kKCk7DQogIH0NCn0pKCk7DQoNCmZ1bmN0aW9uIHN1Ym1pdEV4YW0oKSB7DQogIHZhciB0b3RhbCA9IDA7DQogIHZhciBtYXhUb3RhbCA9IDA7DQogIHZhciBkZXRhaWxzID0gW107DQogIHZhciBkZXRhaWxJZHggPSAwOw0KICANCiAgLy8gU2NvcmUgZWFjaCBzZWN0aW9uDQogIHZhciBzZWN0aW9ucyA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy5zZWN0aW9uJyk7DQogIHNlY3Rpb25zLmZvckVhY2goZnVuY3Rpb24oc2VjKSB7DQogICAgdmFyIHNlY3Rpb25Ub3RhbCA9IDA7DQogICAgdmFyIHNlY3Rpb25NYXggPSAwOw0KICAgIHZhciBzZWN0aW9uSXRlbXMgPSAwOw0KICAgIHZhciBzZWNOYW1lID0gc2VjLnF1ZXJ5U2VsZWN0b3IoJ2gyJykudGV4dENvbnRlbnQucmVwbGFjZSgvXChtYXguKj9cKS8sICcnKS50cmltKCk7DQogICAgDQogICAgLy8gTXVsdGlwbGUgY2hvaWNlIChsaXN0ZW4vcmVhZCkNCiAgICB2YXIgY2hvaWNlUXMgPSBzZWMucXVlcnlTZWxlY3RvckFsbCgnLnF1ZXN0aW9uW2RhdGEtdHlwZT0ibGlzdGVuIl0sIC5xdWVzdGlvbltkYXRhLXR5cGU9InJlYWQiXScpOw0KICAgIGNob2ljZVFzLmZvckVhY2goZnVuY3Rpb24ocSkgew0KICAgICAgdmFyIGFuc0lkeCA9IHBhcnNlSW50KHEuZGF0YXNldC5hbnMpOw0KICAgICAgdmFyIHB0cyA9IHBhcnNlSW50KHEuZGF0YXNldC5wb2ludHMpIHx8IDQ7DQogICAgICB2YXIgc2VsZWN0ZWQgPSBxLnF1ZXJ5U2VsZWN0b3IoJ2lucHV0W3R5cGU9InJhZGlvIl06Y2hlY2tlZCcpOw0KICAgICAgdmFyIGZiID0gcS5xdWVyeVNlbGVjdG9yKCcuZmVlZGJhY2snKTsNCiAgICAgIHZhciBxdGV4dCA9IHEucXVlcnlTZWxlY3RvcignLnF1ZXN0aW9uLXRleHQnKSA/IHEucXVlcnlTZWxlY3RvcignLnF1ZXN0aW9uLXRleHQnKS50ZXh0Q29udGVudC50cmltKCkgOiAnJzsNCiAgICAgIC8vIEdldCBhbGwgb3B0aW9uIHRleHRzDQogICAgICB2YXIgb3B0cyA9IHEucXVlcnlTZWxlY3RvckFsbCgnLm9wdHMgbGFiZWwnKTsNCiAgICAgIHZhciBvcHRUZXh0cyA9IFtdOw0KICAgICAgb3B0cy5mb3JFYWNoKGZ1bmN0aW9uKG8pIHsgb3B0VGV4dHMucHVzaChvLnRleHRDb250ZW50LnRyaW0oKSk7IH0pOw0KICAgICAgdmFyIGNvcnJlY3RBbnMgPSBvcHRUZXh0c1thbnNJZHhdIHx8ICgnT3B6aW9uZSAnICsgKGFuc0lkeCsxKSk7DQogICAgICB2YXIgdXNlckFucyA9IHNlbGVjdGVkID8gb3B0VGV4dHNbcGFyc2VJbnQoc2VsZWN0ZWQudmFsdWUpXSA6ICcoTm9uIHJpc3Bvc3RvKSc7DQogICAgICANCiAgICAgIHNlY3Rpb25NYXggKz0gcHRzOw0KICAgICAgbWF4VG90YWwgKz0gcHRzOw0KICAgICAgc2VjdGlvbkl0ZW1zKys7DQogICAgICB2YXIgY29ycmVjdCA9IGZhbHNlOw0KICAgICAgaWYgKHNlbGVjdGVkKSB7DQogICAgICAgIHZhciB2YWwgPSBwYXJzZUludChzZWxlY3RlZC52YWx1ZSk7DQogICAgICAgIGlmICh2YWwgPT09IGFuc0lkeCkgew0KICAgICAgICAgIHNlY3Rpb25Ub3RhbCArPSBwdHM7DQogICAgICAgICAgdG90YWwgKz0gcHRzOw0KICAgICAgICAgIGNvcnJlY3QgPSB0cnVlOw0KICAgICAgICAgIGZiLmNsYXNzTmFtZSA9ICdmZWVkYmFjayBjb3JyZWN0JzsNCiAgICAgICAgICBmYi50ZXh0Q29udGVudCA9ICfinJMgQ29ycmV0dG8hICgnICsgcHRzICsgJy8nICsgcHRzICsgJyBwdCknOw0KICAgICAgICB9IGVsc2Ugew0KICAgICAgICAgIGZiLmNsYXNzTmFtZSA9ICdmZWVkYmFjayB3cm9uZyc7DQogICAgICAgICAgZmIudGV4dENvbnRlbnQgPSAn4pyXIEhhaSByaXNwb3N0bzogJyArIHVzZXJBbnMgKyAnLiBDb3JyZXR0YTogJyArIGNvcnJlY3RBbnMgKyAnICgwLycgKyBwdHMgKyAnIHB0KSc7DQogICAgICAgIH0NCiAgICAgIH0gZWxzZSB7DQogICAgICAgIGZiLmNsYXNzTmFtZSA9ICdmZWVkYmFjayB3cm9uZyc7DQogICAgICAgIGZiLnRleHRDb250ZW50ID0gJ+KaoCBOb24gcmlzcG9zdG8uIENvcnJldHRhOiAnICsgY29ycmVjdEFucyArICcgKDAvJyArIHB0cyArICcgcHQpJzsNCiAgICAgIH0NCiAgICAgIGRldGFpbHMucHVzaCh7c2VjOiBzZWNOYW1lLCBudW06IGRldGFpbElkeCsxLCBxOiBxdGV4dCwgdXNlcjogdXNlckFucywgY29ycmVjdDogY29ycmVjdEFucywgc3RhdHVzOiBjb3JyZWN0ID8gJ+KckycgOiAn4pyXJywgcHRzOiBjb3JyZWN0ID8gcHRzIDogMCwgbWF4UHRzOiBwdHN9KTsNCiAgICAgIGRldGFpbElkeCsrOw0KICAgIH0pOw0KICAgIA0KICAgIC8vIEZpbGwtaW4gZ3JhbW1hcg0KICAgIHZhciBmaWxsUXMgPSBzZWMucXVlcnlTZWxlY3RvckFsbCgnLnF1ZXN0aW9uW2RhdGEtdHlwZT0iZmlsbCJdJyk7DQogICAgZmlsbFFzLmZvckVhY2goZnVuY3Rpb24ocSkgew0KICAgICAgdmFyIGFucyA9IHEuZGF0YXNldC5hbnMuc3BsaXQoJywnKS5tYXAocyA9PiBub3JtYWxpemUocykpOw0KICAgICAgdmFyIHB0cyA9IHBhcnNlSW50KHEuZGF0YXNldC5wb2ludHMpIHx8IDM7DQogICAgICB2YXIgaW5wdXQgPSBxLnF1ZXJ5U2VsZWN0b3IoJ2lucHV0W3R5cGU9InRleHQiXScpOw0KICAgICAgdmFyIGZiID0gcS5xdWVyeVNlbGVjdG9yKCcuZmVlZGJhY2snKTsNCiAgICAgIHZhciBxdGV4dCA9IHEudGV4dENvbnRlbnQucmVwbGFjZSgvXHMrL2csICcgJykudHJpbSgpLnN1YnN0cmluZygwLCA4MCk7DQogICAgICB2YXIgdXNlckFucyA9IChpbnB1dCAmJiBpbnB1dC52YWx1ZS50cmltKCkpID8gaW5wdXQudmFsdWUudHJpbSgpIDogJyhOb24gcmlzcG9zdG8pJzsNCiAgICAgIHZhciBjb3JyZWN0QW5zID0gcS5kYXRhc2V0LmFuczsNCiAgICAgIA0KICAgICAgc2VjdGlvbk1heCArPSBwdHM7DQogICAgICBtYXhUb3RhbCArPSBwdHM7DQogICAgICBzZWN0aW9uSXRlbXMrKzsNCiAgICAgIHZhciBjb3JyZWN0ID0gZmFsc2U7DQogICAgICBpZiAoaW5wdXQgJiYgaW5wdXQudmFsdWUudHJpbSgpKSB7DQogICAgICAgIHZhciB1c2VyQW5zTm9ybSA9IG5vcm1hbGl6ZShpbnB1dC52YWx1ZSk7DQogICAgICAgIGZvciAodmFyIGEgb2YgYW5zKSB7DQogICAgICAgICAgaWYgKHVzZXJBbnNOb3JtID09PSBhIHx8IHVzZXJBbnNOb3JtLmluY2x1ZGVzKGEpIHx8IGEuaW5jbHVkZXModXNlckFuc05vcm0pKSB7DQogICAgICAgICAgICBjb3JyZWN0ID0gdHJ1ZTsNCiAgICAgICAgICAgIGJyZWFrOw0KICAgICAgICAgIH0NCiAgICAgICAgfQ0KICAgICAgICBpZiAoY29ycmVjdCkgew0KICAgICAgICAgIHNlY3Rpb25Ub3RhbCArPSBwdHM7DQogICAgICAgICAgdG90YWwgKz0gcHRzOw0KICAgICAgICAgIGZiLmNsYXNzTmFtZSA9ICdmZWVkYmFjayBjb3JyZWN0JzsNCiAgICAgICAgICBmYi50ZXh0Q29udGVudCA9ICfinJMgQ29ycmV0dG8hICgnICsgcHRzICsgJy8nICsgcHRzICsgJyBwdCknOw0KICAgICAgICB9IGVsc2Ugew0KICAgICAgICAgIGZiLmNsYXNzTmFtZSA9ICdmZWVkYmFjayB3cm9uZyc7DQogICAgICAgICAgZmIudGV4dENvbnRlbnQgPSAn4pyXIEhhaSBzY3JpdHRvOiAnICsgdXNlckFucyArICcuIENvcnJldHRhOiAnICsgY29ycmVjdEFucyArICcgKDAvJyArIHB0cyArICcgcHQpJzsNCiAgICAgICAgfQ0KICAgICAgfSBlbHNlIHsNCiAgICAgICAgZmIuY2xhc3NOYW1lID0gJ2ZlZWRiYWNrIHdyb25nJzsNCiAgICAgICAgZmIudGV4dENvbnRlbnQgPSAn4pqgIE5vbiByaXNwb3N0by4gQ29ycmV0dGE6ICcgKyBjb3JyZWN0QW5zICsgJyAoMC8nICsgcHRzICsgJyBwdCknOw0KICAgICAgfQ0KICAgICAgZGV0YWlscy5wdXNoKHtzZWM6IHNlY05hbWUsIG51bTogZGV0YWlsSWR4KzEsIHE6IHF0ZXh0LnN1YnN0cmluZygwLDYwKSwgdXNlcjogdXNlckFucywgY29ycmVjdDogY29ycmVjdEFucywgc3RhdHVzOiBjb3JyZWN0ID8gJ+KckycgOiAn4pyXJywgcHRzOiBjb3JyZWN0ID8gcHRzIDogMCwgbWF4UHRzOiBwdHN9KTsNCiAgICAgIGRldGFpbElkeCsrOw0KICAgIH0pOw0KICAgIA0KICAgIC8vIFdyaXRpbmcNCiAgICB2YXIgd3JpdGVRcyA9IHNlYy5xdWVyeVNlbGVjdG9yQWxsKCcucXVlc3Rpb25bZGF0YS10eXBlPSJ3cml0ZSJdJyk7DQogICAgd3JpdGVRcy5mb3JFYWNoKGZ1bmN0aW9uKHEpIHsNCiAgICAgIHZhciB0YSA9IHEucXVlcnlTZWxlY3RvcigndGV4dGFyZWEnKTsNCiAgICAgIHZhciBwdHMgPSAyMDsNCiAgICAgIHNlY3Rpb25NYXggKz0gcHRzOw0KICAgICAgbWF4VG90YWwgKz0gcHRzOw0KICAgICAgc2VjdGlvbkl0ZW1zKys7DQogICAgICB2YXIgcXRleHQgPSBxLnRleHRDb250ZW50LnJlcGxhY2UoL1xzKy9nLCAnICcpLnRyaW0oKS5zdWJzdHJpbmcoMCwgODApOw0KICAgICAgaWYgKHRhKSB7DQogICAgICAgIHZhciB0ZXh0ID0gdGEudmFsdWU7DQogICAgICAgIHZhciB3YyA9IHdvcmRDb3VudCh0ZXh0KTsNCiAgICAgICAgdmFyIHVzZXJBbnMgPSB0ZXh0ID8gdGV4dC5zdWJzdHJpbmcoMCwgODApICsgKHRleHQubGVuZ3RoID4gODAgPyAnLi4uJyA6ICcnKSA6ICcoVnVvdG8pJzsNCiAgICAgICAgdHJ5IHsNCiAgICAgICAgICB2YXIga2V5cyA9IEpTT04ucGFyc2UodGEuZGF0YXNldC5rZXl3b3Jkcyk7DQogICAgICAgICAgdmFyIGtzID0ga2V5d29yZFNjb3JlKHRleHQsIGtleXMpOw0KICAgICAgICAgIHZhciBsZW5Cb251cyA9IE1hdGgubWluKHdjLCAxMDApIC8gMTAwICogNTsNCiAgICAgICAgICB2YXIgc2NvcmUgPSBNYXRoLm1pbihrcyArIGxlbkJvbnVzLCAyMCk7DQogICAgICAgICAgc2VjdGlvblRvdGFsICs9IHNjb3JlOw0KICAgICAgICAgIHRvdGFsICs9IHNjb3JlOw0KICAgICAgICAgIHZhciBrZXlTdHIgPSBrZXlzLmpvaW4oJywgJyk7DQogICAgICAgICAgZGV0YWlscy5wdXNoKHtzZWM6IHNlY05hbWUsIG51bTogZGV0YWlsSWR4KzEsIHE6IHF0ZXh0LnN1YnN0cmluZygwLDUwKSwgdXNlcjogdXNlckFucywgY29ycmVjdDogJ1Bhcm9sZSBjaGlhdmU6ICcgKyBrZXlTdHIuc3Vic3RyaW5nKDAsNjApLCBzdGF0dXM6IHNjb3JlID49IDEyID8gJ+KckycgOiAn4pazJywgcHRzOiBNYXRoLnJvdW5kKHNjb3JlKSwgbWF4UHRzOiBwdHN9KTsNCiAgICAgICAgfSBjYXRjaChlKSB7DQogICAgICAgICAgc2VjdGlvblRvdGFsICs9IDA7IHRvdGFsICs9IDA7DQogICAgICAgICAgZGV0YWlscy5wdXNoKHtzZWM6IHNlY05hbWUsIG51bTogZGV0YWlsSWR4KzEsIHE6IHF0ZXh0LnN1YnN0cmluZygwLDUwKSwgdXNlcjogdXNlckFucywgY29ycmVjdDogJyhjb25zdWx0YXJlIGlsIGRvY2VudGUpJywgc3RhdHVzOiAnPycsIHB0czogMCwgbWF4UHRzOiBwdHN9KTsNCiAgICAgICAgfQ0KICAgICAgfQ0KICAgICAgZGV0YWlsSWR4Kys7DQogICAgfSk7DQogICAgDQogICAgLy8gU3BlYWtpbmcgKHRleHQpDQogICAgdmFyIHNwZWFrUXMgPSBzZWMucXVlcnlTZWxlY3RvckFsbCgnLnF1ZXN0aW9uW2RhdGEtdHlwZT0ic3BlYWsiXScpOw0KICAgIHNwZWFrUXMuZm9yRWFjaChmdW5jdGlvbihxKSB7DQogICAgICB2YXIgdGEgPSBxLnF1ZXJ5U2VsZWN0b3IoJ3RleHRhcmVhJyk7DQogICAgICB2YXIgcHRzID0gMjA7DQogICAgICBzZWN0aW9uTWF4ICs9IHB0czsNCiAgICAgIG1heFRvdGFsICs9IHB0czsNCiAgICAgIHNlY3Rpb25JdGVtcysrOw0KICAgICAgdmFyIHF0ZXh0ID0gcS50ZXh0Q29udGVudC5yZXBsYWNlKC9ccysvZywgJyAnKS50cmltKCkuc3Vic3RyaW5nKDAsIDgwKTsNCiAgICAgIGlmICh0YSkgew0KICAgICAgICB2YXIgdGV4dCA9IHRhLnZhbHVlOw0KICAgICAgICB2YXIgd2MgPSB3b3JkQ291bnQodGV4dCk7DQogICAgICAgIHZhciB1c2VyQW5zID0gdGV4dCA/IHRleHQuc3Vic3RyaW5nKDAsIDgwKSArICh0ZXh0Lmxlbmd0aCA+IDgwID8gJy4uLicgOiAnJykgOiAnKFZ1b3RvKSc7DQogICAgICAgIHRyeSB7DQogICAgICAgICAgdmFyIGtleXMgPSBKU09OLnBhcnNlKHRhLmRhdGFzZXQua2V5d29yZHMpOw0KICAgICAgICAgIHZhciBrcyA9IGtleXdvcmRTY29yZSh0ZXh0LCBrZXlzKTsNCiAgICAgICAgICB2YXIgbGVuQm9udXMgPSBNYXRoLm1pbih3YywgODApIC8gODAgKiA1Ow0KICAgICAgICAgIHZhciBzY29yZSA9IE1hdGgubWluKGtzICsgbGVuQm9udXMsIDIwKTsNCiAgICAgICAgICBzZWN0aW9uVG90YWwgKz0gc2NvcmU7DQogICAgICAgICAgdG90YWwgKz0gc2NvcmU7DQogICAgICAgICAgdmFyIGtleVN0ciA9IGtleXMuam9pbignLCAnKTsNCiAgICAgICAgICBkZXRhaWxzLnB1c2goe3NlYzogc2VjTmFtZSwgbnVtOiBkZXRhaWxJZHgrMSwgcTogcXRleHQuc3Vic3RyaW5nKDAsNTApLCB1c2VyOiB1c2VyQW5zLCBjb3JyZWN0OiAnUGFyb2xlIGNoaWF2ZTogJyArIGtleVN0ci5zdWJzdHJpbmcoMCw2MCksIHN0YXR1czogc2NvcmUgPj0gMTIgPyAn4pyTJyA6ICfilrMnLCBwdHM6IE1hdGgucm91bmQoc2NvcmUpLCBtYXhQdHM6IHB0c30pOw0KICAgICAgICB9IGNhdGNoKGUpIHsNCiAgICAgICAgICBzZWN0aW9uVG90YWwgKz0gMDsgdG90YWwgKz0gMDsNCiAgICAgICAgICBkZXRhaWxzLnB1c2goe3NlYzogc2VjTmFtZSwgbnVtOiBkZXRhaWxJZHgrMSwgcTogcXRleHQuc3Vic3RyaW5nKDAsNTApLCB1c2VyOiB1c2VyQW5zLCBjb3JyZWN0OiAnKGNvbnN1bHRhcmUgaWwgZG9jZW50ZSknLCBzdGF0dXM6ICc/JywgcHRzOiAwLCBtYXhQdHM6IHB0c30pOw0KICAgICAgICB9DQogICAgICB9DQogICAgICBkZXRhaWxJZHgrKzsNCiAgICB9KTsNCiAgICANCiAgICAvLyBTaG93IHNlY3Rpb24gc2NvcmUNCiAgICB2YXIgc2VjU2NvcmUgPSBzZWMucXVlcnlTZWxlY3RvcignLnNlY3Rpb24tc2NvcmUnKTsNCiAgICBpZiAoc2VjU2NvcmUpIHsNCiAgICAgIHNlY1Njb3JlLnN0eWxlLmRpc3BsYXkgPSAnYmxvY2snOw0KICAgICAgdmFyIHBjdCA9IHNlY3Rpb25NYXggPiAwID8gTWF0aC5yb3VuZChzZWN0aW9uVG90YWwgLyBzZWN0aW9uTWF4ICogMTAwKSA6IDA7DQogICAgICBzZWNTY29yZS50ZXh0Q29udGVudCA9ICdTZXppb25lOiAnICsgTWF0aC5yb3VuZChzZWN0aW9uVG90YWwpICsgJy8nICsgc2VjdGlvbk1heCArICcgKCcgKyBwY3QgKyAnJSknOw0KICAgIH0NCiAgfSk7DQogIA0KICAvLyBPdmVyYWxsIHNjb3JlDQogIHZhciBwY3QgPSBtYXhUb3RhbCA+IDAgPyBNYXRoLnJvdW5kKHRvdGFsIC8gbWF4VG90YWwgKiAxMDApIDogMDsNCiAgdmFyIHNjb3JlQmFyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3Njb3JlQmFyJyk7DQogIHNjb3JlQmFyLnN0eWxlLmRpc3BsYXkgPSAnYmxvY2snOw0KICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndG90YWxTY29yZScpLnRleHRDb250ZW50ID0gTWF0aC5yb3VuZCh0b3RhbCkgKyAnLycgKyBtYXhUb3RhbDsNCiAgDQogIHZhciBtc2cgPSAnJzsNCiAgaWYgKHBjdCA+PSA4NSkgbXNnID0gIvCfn6IgRWNjZWxsZW50ZSEgTGl2ZWxsbyByYWdnaXVudG8gYnJpbGxhbnRlbWVudGUuIFNlaSBwcm9udG8gcGVyIGwnZXNhbWUgdmVybyEiOw0KICBlbHNlIGlmIChwY3QgPj0gNzApIG1zZyA9ICLwn5S1IEJ1b25vISBIYWkgdW5hIHNvbGlkYSBwcmVwYXJhemlvbmUuIFJpdmVkaSBnbGkgZXJyb3JpIHBlciBwZXJmZXppb25hcnRpLiI7DQogIGVsc2UgaWYgKHBjdCA+PSA1NSkgbXNnID0gIvCfn6EgRGlzY3JldG8uIFNlaSBzdWxsYSBidW9uYSBzdHJhZGEsIG1hIGRldmkgc3R1ZGlhcmUgZGkgcGnDuSBhbGN1bmUgYXJlZS4iOw0KICBlbHNlIGlmIChwY3QgPj0gNDApIG1zZyA9ICLwn5+gIEluc3VmZmljaWVudGUuIFRpIGNvbnNpZ2xpbyBkaSByaXBhc3NhcmUgbGUgYmFzaSBlIHJpcHJvdmFyZS4iOw0KICBlbHNlIG1zZyA9ICLwn5S0IE1vbHRvIGluc3VmZmljaWVudGUuIEhhaSBiaXNvZ25vIGRpIHN0dWRpYXJlIG1vbHRvIHByaW1hIGRpIGFmZnJvbnRhcmUgbCdlc2FtZS4iOw0KICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2NvcmVNZXNzYWdlJykudGV4dENvbnRlbnQgPSBtc2cgKyAnIChQdW50ZWdnaW86ICcgKyBwY3QgKyAnJSknOw0KICANCiAgLy8gU2hvdyBhbnN3ZXIgcmVmZXJlbmNlIHRhYmxlDQogIHZhciByZWZEaXYgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnYW5zd2VyUmVmZXJlbmNlJyk7DQogIGlmICghcmVmRGl2KSB7DQogICAgcmVmRGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7DQogICAgcmVmRGl2LmlkID0gJ2Fuc3dlclJlZmVyZW5jZSc7DQogICAgcmVmRGl2LmNsYXNzTmFtZSA9ICdzZWN0aW9uJzsNCiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCcuYnRuLXN1Ym1pdCcpLnBhcmVudE5vZGUucGFyZW50Tm9kZS5hcHBlbmRDaGlsZChyZWZEaXYpOw0KICB9DQogIHJlZkRpdi5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJzsNCiAgcmVmRGl2LmlubmVySFRNTCA9ICc8aDI+8J+TiyBSaWVwaWxvZ28gcmlzcG9zdGU8L2gyPic7DQogIA0KICBpZiAoZGV0YWlscy5sZW5ndGggPiAwKSB7DQogICAgdmFyIHRhYmxlID0gJzx0YWJsZSBjbGFzcz0icmVmLXRhYmxlIj48dGhlYWQ+PHRyPjx0aD4jPC90aD48dGg+RG9tYW5kYTwvdGg+PHRoPkxhIHR1YSByaXNwb3N0YTwvdGg+PHRoPlJpc3Bvc3RhIGNvcnJldHRhPC90aD48dGg+RXNpdG88L3RoPjx0aD5QdW50aTwvdGg+PC90cj48L3RoZWFkPjx0Ym9keT4nOw0KICAgIGZvciAodmFyIGQgb2YgZGV0YWlscykgew0KICAgICAgdmFyIGNscyA9IGQuc3RhdHVzID09PSAn4pyTJyA/ICdyZWYtY29ycicgOiAoZC5zdGF0dXMgPT09ICc/JyA/ICcnIDogJ3JlZi13cm9uZycpOw0KICAgICAgdGFibGUgKz0gJzx0ciBjbGFzcz0iJyArIGNscyArICciPjx0ZD4nICsgZC5udW0gKyAnPC90ZD48dGQ+JyArIGQucS5zdWJzdHJpbmcoMCw0NSkgKyAnPC90ZD48dGQ+JyArIGQudXNlci5zdWJzdHJpbmcoMCw0MCkgKyAnPC90ZD48dGQ+JyArIGQuY29ycmVjdC5zdWJzdHJpbmcoMCw2MCkgKyAnPC90ZD48dGQ+JyArIGQuc3RhdHVzICsgJzwvdGQ+PHRkPicgKyBNYXRoLnJvdW5kKGQucHRzKSArICcvJyArIGQubWF4UHRzICsgJzwvdGQ+PC90cj4nOw0KICAgIH0NCiAgICB0YWJsZSArPSAnPC90Ym9keT48L3RhYmxlPic7DQogICAgcmVmRGl2LmlubmVySFRNTCArPSB0YWJsZTsNCiAgICANCiAgICAvLyBTdW1tYXJ5DQogICAgdmFyIGNvcnJDb3VudCA9IGRldGFpbHMuZmlsdGVyKGZ1bmN0aW9uKGQpIHsgcmV0dXJuIGQuc3RhdHVzID09PSAn4pyTJzsgfSkubGVuZ3RoOw0KICAgIHZhciBwYXJ0Q291bnQgPSBkZXRhaWxzLmZpbHRlcihmdW5jdGlvbihkKSB7IHJldHVybiBkLnN0YXR1cyA9PT0gJ+KWsyc7IH0pLmxlbmd0aDsNCiAgICByZWZEaXYuaW5uZXJIVE1MICs9ICc8cCBzdHlsZT0ibWFyZ2luLXRvcDoxMnB4O2ZvbnQtc2l6ZToxM3B4O2NvbG9yOiM2NjY7Ij7inJMgQ29ycmV0dGU6ICcgKyBjb3JyQ291bnQgKyAnIMK3IOKWsyBQYXJ6aWFsaTogJyArIHBhcnRDb3VudCArICcgwrcg4pyXIEVycmF0ZTogJyArIChkZXRhaWxzLmxlbmd0aCAtIGNvcnJDb3VudCAtIHBhcnRDb3VudCkgKyAnIMK3IFRvdGFsZTogJyArIGRldGFpbHMubGVuZ3RoICsgJyBkb21hbmRlPC9wPic7DQogIH0NCiAgDQogIC8vIFNvdW5kIGVmZmVjdA0KICB0cnkgew0KICAgIHZhciBjdHggPSBuZXcgKHdpbmRvdy5BdWRpb0NvbnRleHQgfHwgd2luZG93LndlYmtpdEF1ZGlvQ29udGV4dCkoKTsNCiAgICB2YXIgb3NjID0gY3R4LmNyZWF0ZU9zY2lsbGF0b3IoKTsNCiAgICBvc2MudHlwZSA9ICdzaW5lJzsNCiAgICBvc2MuZnJlcXVlbmN5LnZhbHVlID0gcGN0ID49IDcwID8gODgwIDogNDQwOw0KICAgIG9zYy5jb25uZWN0KGN0eC5kZXN0aW5hdGlvbik7DQogICAgb3NjLnN0YXJ0KCk7DQogICAgc2V0VGltZW91dChmdW5jdGlvbigpIHsgb3NjLnN0b3AoKTsgfSwgMzAwKTsNCiAgfSBjYXRjaChlKSB7fQ0KICANCiAgd2luZG93LnNjcm9sbFRvKDAsIDApOw0KfQ0KDQpmdW5jdGlvbiByZXNldEV4YW0oKSB7DQogIGlmICghY29uZmlybSgnU2VpIHNpY3VybyBkaSB2b2xlciByaWNvbWluY2lhcmU/IFR1dHRlIGxlIHJpc3Bvc3RlIHZlcnJhbm5vIGNhbmNlbGxhdGUuJykpIHJldHVybjsNCiAgZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnaW5wdXRbdHlwZT0icmFkaW8iXScpLmZvckVhY2goZnVuY3Rpb24ocikgeyByLmNoZWNrZWQgPSBmYWxzZTsgfSk7DQogIGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJ2lucHV0W3R5cGU9InRleHQiXScpLmZvckVhY2goZnVuY3Rpb24oaSkgeyBpLnZhbHVlID0gJyc7IH0pOw0KICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCd0ZXh0YXJlYScpLmZvckVhY2goZnVuY3Rpb24odCkgeyB0LnZhbHVlID0gJyc7IH0pOw0KICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuZmVlZGJhY2snKS5mb3JFYWNoKGZ1bmN0aW9uKGYpIHsgZi5jbGFzc05hbWUgPSAnZmVlZGJhY2snOyBmLnRleHRDb250ZW50ID0gJyc7IH0pOw0KICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcuc2VjdGlvbi1zY29yZScpLmZvckVhY2goZnVuY3Rpb24ocykgeyBzLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7IH0pOw0KICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2NvcmVCYXInKS5zdHlsZS5kaXNwbGF5ID0gJ25vbmUnOw0KICB2YXIgcmVmID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2Fuc3dlclJlZmVyZW5jZScpOw0KICBpZiAocmVmKSByZWYuc3R5bGUuZGlzcGxheSA9ICdub25lJzsNCn0KZnVuY3Rpb24gc2hvd1NjcmlwdChidG4pIHsKICB2YXIgcURpdiA9IGJ0bi5jbG9zZXN0KCcucXVlc3Rpb24uc3RlbScpIHx8IGJ0bi5wYXJlbnRFbGVtZW50OwogIGlmICghcURpdikgcmV0dXJuOwogIHZhciBzY3JpcHRUZXh0ID0gcURpdi5nZXRBdHRyaWJ1dGUoJ2RhdGEtc2NyaXB0Jyk7CiAgaWYgKCFzY3JpcHRUZXh0KSByZXR1cm47CiAgdmFyIGV4aXN0aW5nID0gcURpdi5xdWVyeVNlbGVjdG9yKCcuc2NyaXB0LXRleHQnKTsKICBpZiAoIWV4aXN0aW5nKSB7CiAgICBleGlzdGluZyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpOwogICAgZXhpc3RpbmcuY2xhc3NOYW1lID0gJ3NjcmlwdC10ZXh0JzsKICAgIGV4aXN0aW5nLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7CiAgICBidG4ucGFyZW50Tm9kZS5pbnNlcnRCZWZvcmUoZXhpc3RpbmcsIGJ0bi5uZXh0U2libGluZyk7CiAgfQogIGlmIChleGlzdGluZy5zdHlsZS5kaXNwbGF5ID09PSAnbm9uZScgfHwgIWV4aXN0aW5nLnRleHRDb250ZW50KSB7CiAgICBleGlzdGluZy50ZXh0Q29udGVudCA9IHNjcmlwdFRleHQ7CiAgICBleGlzdGluZy5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJzsKICAgIGJ0bi50ZXh0Q29udGVudCA9ICdOYXNjb25kaSB0ZXN0byc7CiAgfSBlbHNlIHsKICAgIGV4aXN0aW5nLnN0eWxlLmRpc3BsYXkgPSAnbm9uZSc7CiAgICBidG4udGV4dENvbnRlbnQgPSAnVGVzdG8nOwogIH0KfQ==").decode("utf-8")
    





    """Generate a complete interactive HTML page for one exam"""

    etype = exam_data["exam_type"]

    level = exam_data["level"]

    set_name = exam_data.get("set", etype)

    display_name = exam_data.get("display_name", exam_key)

    

    title = f"{etype} {set_name} — {display_name}"

    

    # Find audio files for listening section

    audio_paths = {}

    for section in exam_data["sections"]:

        if section["id"] == "ascolto":

            audio_dir = os.path.join(REPO_DIR, etype, set_name, level, "audio")

            if os.path.exists(audio_dir):

                mp3_files = sorted([ff for ff in os.listdir(audio_dir) if ff.endswith(".mp3") or ff.endswith(".js")])

                js_files = [ff for ff in mp3_files if ff.endswith(".js")]

                

                # Assign files sequentially to items in order

                used = set()

                for idx in range(len(section["items"])):

                    if idx < len(js_files):

                        fname = js_files[idx]

                        if fname.endswith(".js"):

                            fname_noext = fname[:-3]

                        else:

                            fname_noext = fname[:-4]

                        audio_paths[f"{etype}_{level}_{idx}"] = f"{level}/audio/{fname_noext}"

                        used.add(js_files[idx])

                    else:

                        # Try matching by index+1 number as fallback

                        target = idx + 1

                        for f in js_files:

                            if f not in used:

                                parts = f.replace(".js","").split("_")

                                for p in parts:

                                    if p.isdigit() and int(p) == target:

                                        audio_paths[f"{etype}_{level}_{idx}"] = f"{level}/audio/{f.replace('.js','')}"

                                        used.add(f)

                                        break

    

    # Build HTML

    first_audio = ""

    for section in exam_data["sections"]:

        if section["id"] == "ascolto" and section["items"]:

            audio_key = f'{etype}_{level}_0'

            first_audio = audio_paths.get(audio_key, "")

            break

    

    preload_tag = ""

    if first_audio:

        preload_tag = f'<link rel="preload" href="{first_audio}.js" as="script" crossorigin="anonymous">\n'

    

    lines = []

    lines.append(f"""<!DOCTYPE html>

<html lang="it">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{title} — Online Exam</title>

{preload_tag}<style>""" + _orig_css + """</style></head>

<body>

<div class="container">

  <div class="header">

    <div>

      <h1>{title} <small>Online Exam</small></h1>

    </div>

    <div class="meta">

      <span id="timer">00:00</span>

    </div>

  </div>""")

    # Score bar
    lines.append("""  <div id="scoreBar" class="score-bar">
    <h2 id="totalScore">0/100</h2>
    <p id="scoreMessage"></p>
  </div>""")

    # Generate sections

    sid = 0

    for section in exam_data["sections"]:

        sec_name = section["id"].capitalize()

        sec_class = section["id"]

        lines.append(f'  <div class="section {sec_class}" id="sec_{sid}">')

        lines.append(f'    <h2>{sec_name} <small>{section["max_points"]} pt</small></h2>')

        

        for idx, item in enumerate(section["items"]):

            if section["id"] == "ascolto":

                audio_url = audio_paths.get(f"{etype}_{level}_{idx}", "")

                script = item.get("script", "")

                script_escaped = (script or "").replace("'", "&#39;")

                lines.append(f'  <div class="question stem" data-type="listen" data-ans="{item["ans"]}" data-script=\'{script_escaped}\' data-points="{section["max_points"] // len(section["items"])}">')

                if audio_url:

                    lines.append(f'    <button class="play-btn" data-audio-js="{audio_url}" onclick="playAudio(this)">\u25b6 Ascolta</button> <button class="script-btn" onclick="showScript(this)">\ud83d\udcc4 Testo</button>')

                else:

                    lines.append(f'    <div style="font-size:12px;color:#999;margin-bottom:4px;">\ud83d\udcdd Ascolto {idx+1}</div>')

                lines.append(f'    <div style="font-weight:500;margin:6px 0;" class="question-text">{item["q"]}</div>')

                lines.append(f'    <div class="opts" data-q="{idx}">')

                for oi, opt in enumerate(item["opts"]):

                    lines.append(f'      <label><input type="radio" name="q_{sid}_{idx}" value="{oi}"> {opt}</label>')

                lines.append('    </div>')

                lines.append(f'    <div id="fb_{sid}_{idx}" class="feedback"></div>')

                lines.append('  </div>')

            elif section["id"] == "lettura":

                lines.append(f'  <div class="question stem" data-type="read" data-ans="{item["ans"]}" data-points="{section["max_points"] // len(section["items"])}">')

                lines.append(f'    <div style="font-weight:500;margin:6px 0;" class="question-text">{item["q"]}</div>')

                lines.append(f'    <div class="opts" data-q="{idx}">')

                for oi, opt in enumerate(item["opts"]):

                    lines.append(f'      <label><input type="radio" name="q_{sid}_{idx}" value="{oi}"> {opt}</label>')

                lines.append('    </div>')

                lines.append(f'    <div id="fb_{sid}_{idx}" class="feedback"></div>')

                lines.append('  </div>')

            elif section["id"] == "grammatica":

                keywords = "|".join(item.get("keywords", []))

                lines.append(f'  <div class="question" data-type="grammar" data-keywords="{keywords}" data-points="{section["max_points"] // len(section["items"])}">')

                lines.append(f'    <div style="font-weight:500;margin:6px 0;" class="question-text">{item["q"]}</div>')

                lines.append(f'    <input type="text" id="inp_{sid}_{idx}" placeholder="Scrivi la risposta..." autocomplete="off">')

                lines.append(f'    <div id="fb_{sid}_{idx}" class="feedback"></div>')

                lines.append('  </div>')

            elif section["id"] in ("scrittura", "orale"):

                keywords = "|".join(item.get("keywords", []))

                lines.append(f'  <div class="question" data-type="{section["id"]}" data-keywords="{keywords}" data-points="{section["max_points"]}">')

                lines.append(f'    <div style="font-weight:500;margin:6px 0;" class="question-text">{item["q"]}</div>')

                lines.append(f'    <textarea id="inp_{sid}_{idx}" placeholder="Scrivi qui..." autocomplete="off"></textarea>')

                lines.append(f'    <div id="fb_{sid}_{idx}" class="feedback"></div>')

                lines.append('  </div>')

        

        lines.append('  </div>')

        sid += 1

    

    # Submit / Reset buttons

    lines.append("""<div id="answerReference" style="display:none;margin-top:20px;">
  <h3>Risposte corrette</h3>
  <div id="refContent"></div>
</div>
  <div class="btn-row">

    <button class="btn-submit" onclick="submitExam()">📝 Invia e valuta</button>

    <button class="btn-reset" onclick="resetExam()">🔄 Ricomincia</button>

  </div>

  

  <div class="score-box" id="scoreBox">

    <h3 id="scorePct">0%</h3>

    <div class="grade" id="scoreGrade">—</div>

  </div>

  

  <table id="resultTable">

    <thead><tr><th>Sezione</th><th>Punteggio</th><th>Max</th></tr></thead>

    <tbody id="resultBody"></tbody>

  </table>

</div>



<script>""" + _orig_js + """</script>

</body>

</html>""")

    

    return "\n".join(lines)





def main():

    if not os.path.exists(REPO_DIR):

        print("Error: REPO_DIR not found: " + REPO_DIR)

        return

    

    count = 0

    for exam_key, exam_data in EXAMS.items():

        etype = exam_data["exam_type"]

        level = exam_data["level"]

        print(f"  {exam_key} ({etype} {level})...", end=" ", flush=True)

        

        html = generate_exam_html(exam_key, exam_data)

        

        out_dir = os.path.join(REPO_DIR, etype, exam_data.get("set", etype))

        os.makedirs(out_dir, exist_ok=True)

        out_path = os.path.join(out_dir, f"{exam_key}.html")

        

        with open(out_path, "wb") as f:

            html = html.encode("utf-8", "backslashreplace").decode("utf-8")
            f.write(html.encode("utf-8", "replace"))

        

        sz = os.path.getsize(out_path) // 1024

        print(f"OK {sz}KB")

        count += 1

    

    print(f"\nDone: {count} pages generated")





if __name__ == "__main__":

    main()

