#!/usr/bin/env python3
"""
Add answer display for grammar (show correct answer) and reference answers for scrittura/orale.
Also demonstrates keyboard shortcuts and improves scrolling on submission.
"""
import os, re, base64, json, urllib.request, time, sys

REPO = r"D:\workbuddy工作区\2026-06-10-13-51-52\italiano-esami"
LEVELS = ["A1","A2","B1","B2","C1","C2"]
TOKEN = '${GITHUB_TOKEN}'

# Reference answers for scrittura and orale (generated from keywords)
# Format: {level: {section: [(keywords, reference), ...]}}
# These match the order in cils_data.py and celi_data.py

REFERENCES = {
    "CILS": {
        "scrittura": {
            # A1: 5 items
            "A1": [
                "Mi chiamo Marco, ho 22 anni e vengo dall'Italia. Studio lingue all'università. Mi piace leggere e viaggiare.",
                "La mia giornata tipica: mi sveglio alle 7, faccio colazione con cappuccino e cornetto, poi vado all'università. Pranzo alle 13 e studio al pomeriggio. La sera ceno e guardo la TV.",
                "Ieri sono andato al cinema con gli amici. Abbiamo visto un film divertente e poi siamo andati a cena in pizzeria. È stata una bella giornata.",
                "La mia famiglia è composta da 4 persone: mio padre, mia madre, mio fratello e io. Abitiamo in una casa con giardino in periferia.",
                "La mia città è Roma, una città bellissima piena di storia. Ci sono molti musei e monumenti famosi come il Colosseo. Mi piace molto passeggiare per il centro."
            ],
            "A2": [
                "Sabato sono andato al mare con gli amici. Abbiamo fatto il bagno e preso il sole. La domenica sono rimasto a casa a riposare. È stato un bel fine settimana.",
                "L'anno scorso sono andato a Parigi con la mia famiglia. Abbiamo visitato la Tour Eiffel, il Louvre e Montmartre. È stato un viaggio bellissimo, ho visto tantissime cose interessanti.",
                "Quest'anno ho studiato molto all'università. Ho dato 5 esami e li ho passati tutti. I professori sono stati bravi e ho imparato molte cose nuove.",
                "Ciao amico mio, sabato prossimo farò una festa a casa mia. Inizierà alle 20. Porta qualcosa da mangiare o da bere. Ti aspetto!",
                "Recentemente ho visto il film 'La vita è bella'. È un film italiano molto commovente. La storia parla di un padre che protegge suo figlio durante la guerra. Mi è piaciuto molto."
            ],
            "B1": [
                "Gentile Responsabile, mi candido per la posizione di assistente amministrativo. Ho esperienza nel settore e buone competenze informatiche. Sono disponibile per un colloquio. Cordiali saluti.",
                "Imparare le lingue è molto importante perché offre opportunità di lavoro all'estero e permette di conoscere nuove culture. Personalmente, studiare l'italiano mi ha aperto molte porte.",
                "Il mio viaggio più bello è stato in Giappone. Ho visitato Tokyo e Kyoto, ho incontrato persone meravigliose e ho assaggiato cibi deliziosi. È stata un'esperienza indimenticabile.",
                "Ho cenato al Ristorante Da Mario. Il servizio è stato eccellente e la qualità dei piatti ottima. Consiglio vivamente la pasta alla carbonara. Il rapporto qualità-prezzo è buono.",
                "Tra dieci anni mi vedo con un buon lavoro, una famiglia e una casa mia. Spero di aver viaggiato molto e di essere realizzato professionalmente e personalmente."
            ],
            "B2": [
                "Il cambiamento climatico è una delle sfide più urgenti del nostro tempo. È necessario agire subito per ridurre le emissioni e proteggere l'ambiente. Ogni individuo ha la responsabilità di fare la propria parte per un futuro sostenibile.",
                "La globalizzazione ha portato benefici economici e opportunità culturali, ma ha anche creato disuguaglianze e omologazione. È importante trovare un equilibrio tra apertura internazionale e tutela delle identità locali.",
                "La settimana scorsa ho partecipato a una mostra d'arte contemporanea molto interessante. Le opere esposte erano innovative e stimolanti. L'evento era ben organizzato e il pubblico numeroso.",
                "L'intelligenza artificiale sta rivoluzionando il mondo del lavoro. Alcuni lavori scompariranno ma ne nasceranno di nuovi. È fondamentale investire nella formazione per prepararsi a questo cambiamento.",
                "Egregio Sindaco, le scrivo per segnalare il problema del traffico nel mio quartiere. Chiedo l'installazione di dossi rallentatori e più controlli. Una soluzione potrebbe essere la creazione di zone pedonali."
            ],
            "C1": [
                "Il rapporto tra etica e tecnologia è complesso: l'innovazione tecnologica offre possibilità straordinarie ma solleva anche questioni etiche profonde. È necessario stabilire limiti chiari per garantire che la tecnologia serva l'umanità e non la danneggi.",
                "La post-verità rappresenta una sfida per la comunicazione contemporanea. Nell'era dei social media, l'informazione è spesso manipolata e la verità diventa relativa. I media hanno la responsabilità di garantire informazioni accurate.",
                "I cambiamenti climatici richiedono politiche ambientali coraggiose a livello globale. Il futuro del pianeta dipende dalle nostre scelte di oggi. È urgente ridurre le emissioni e investire nelle energie rinnovabili.",
                "La cultura nell'era globale deve bilanciare identità locale e dialogo interculturale. La diversità culturale è una ricchezza che va preservata, mentre il dialogo tra culture diverse promuove comprensione e pace.",
                "Il rapporto tra individuo e collettività è in continua evoluzione. La società contemporanea oscilla tra la valorizzazione dell'individuo e la necessità di solidarietà collettiva. Trovare un equilibrio è fondamentale."
            ],
            "C2": [
                "Il concetto di verità nell'era della post-verità è problematico. La conoscenza è frammentata e l'interpretazione dei fatti è spesso influenzata da interessi particolari. È necessario recuperare un'etica della verità basata sul dialogo e sulla trasparenza.",
                "Il potere e il sapere sono strettamente intrecciati nella società contemporanea. Foucault ha mostrato come le istituzioni disciplinari producono conoscenza che a sua volta rafforza il potere. Oggi questo rapporto si manifesta nelle tecnologie di sorveglianza.",
                "La crisi della rappresentanza politica è evidente nel calo della partecipazione elettorale e nella sfiducia dei cittadini verso le istituzioni. La democrazia ha bisogno di nuovi spazi di partecipazione e di un rinnovamento delle élite politiche.",
                "L'arte nella società dello spettacolo rischia di diventare puro intrattenimento. Tuttavia, l'arte contemporanea conserva una funzione critica fondamentale, capace di interrogare la realtà e proporre nuove prospettive di senso.",
                "Il populismo è un fenomeno complesso che va analizzato storicamente e politicamente. Nasce dalla crisi della rappresentanza e dalla disillusione verso le élite tradizionali, ma rischia di minare le istituzioni democratiche."
            ],
        },
        "orale": {
            "A1": [
                "Mi chiamo Luca, ho 25 anni e vengo dalla Sicilia. Vivo a Bologna dove studio ingegneria. Mi piace la musica italiana.",
                "La mia routine: mi alzo alle 7, faccio colazione, vado all'università o al lavoro. La sera ceno e guardo film.",
                "La mia casa ha tre stanze: un salotto, una camera da letto e una cucina. È piccola ma accogliente. C'è anche un balcone.",
                "Nel tempo libero mi piace leggere libri, andare al cinema e fare sport. Ogni settimana gioco a calcio con gli amici.",
                "Sabato sono uscito con gli amici. Siamo andati al ristorante e poi al cinema. Ho visto un film molto divertente."
            ],
            "A2": [
                "Recentemente ho visitato Firenze con la mia ragazza. Abbiamo visto il Duomo e Ponte Vecchio. È stata un'esperienza molto interessante e romantica.",
                "La mia città preferita è Venezia perché è unica al mondo. I canali, le gondole e Piazza San Marco la rendono speciale. Ogni visita è magica.",
                "Il mio progetto per il futuro è trovare un buon lavoro e magari trasferirmi all'estero per qualche anno. Spero di realizzare questo sogno presto.",
                "La persona più importante per me è mia madre. Mi ha sempre sostenuto e aiutato in ogni momento. È una persona forte e generosa.",
                "Di solito nel fine settimana mi rilasso: dormo fino a tardi, esco con gli amici, vado al cinema o faccio sport. La domenica ceno con la famiglia."
            ],
            "B1": [
                "Vivere in una grande città offre molti vantaggi come trasporti efficienti, offerta culturale e opportunità di lavoro. Tuttavia, ci sono anche svantaggi come il costo della vita elevato, l'inquinamento e lo stress quotidiano.",
                "I social media hanno rivoluzionato la comunicazione, permettendo di restare in contatto con persone lontane. Tuttavia, un uso eccessivo può causare dipendenza e isolamento sociale. È importante usarli con moderazione.",
                "Il libro che mi ha colpito di più è 'Il nome della rosa' di Umberto Eco. La trama è avvincente, i personaggi sono ben sviluppati e lo stile è affascinante. Lo consiglio a tutti gli amanti della letteratura.",
                "La tutela dell'ambiente è fondamentale per il nostro futuro. Dobbiamo ridurre l'inquinamento, riciclare i rifiuti e proteggere la biodiversità. Ogni piccolo gesto quotidiano può fare la differenza.",
                "L'immigrazione in Italia è un fenomeno complesso. Da un lato, l'integrazione è necessaria per una società multiculturale; dall'altro, ci sono sfide legate al lavoro e all'accoglienza. Serve equilibrio."
            ],
            "B2": [
                "I social media influenzano la democrazia in modi contraddittori: da un lato facilitano la partecipazione e la diffusione delle informazioni, dall'altro favoriscono la disinformazione e la polarizzazione. È fondamentale educare all'uso critico dei media.",
                "La tecnologia sta trasformando il mercato del lavoro. L'automazione elimina alcuni lavori ma ne crea di nuovi. La formazione continua è essenziale per adattarsi a questi cambiamenti e acquisire nuove competenze.",
                "Il turismo di massa ha effetti negativi sull'ambiente e sulle comunità locali. L'overtourism danneggia gli ecosistemi e la qualità della vita. Serve un turismo sostenibile che rispetti i territori e le culture.",
                "L'integrazione europea ha portato pace e prosperità, ma oggi affronta sfide come la crisi migratoria e il ritorno dei sovranismi. La solidarietà tra stati membri è essenziale per superare queste difficoltà.",
                "L'università ha un ruolo fondamentale nella società: forma i professionisti di domani, promuove la ricerca e il pensiero critico. Investire nell'istruzione superiore è investire nel futuro del paese."
            ],
            "C1": [
                "La libertà nella filosofia politica contemporanea è un concetto complesso che spazia dalla libertà negativa come non-interferenza alla libertà positiva come autodeterminazione. L'autonomia individuale va bilanciata con la responsabilità sociale per una convivenza democratica.",
                "L'intellettuale oggi ha il compito di interpretare criticamente la realtà, smascherare le ideologie e promuovere un pensiero indipendente. In un'epoca di disinformazione, il ruolo critico dell'intellettuale è più importante che mai.",
                "Il modello di sviluppo attuale basato sulla crescita illimitata non è sostenibile. L'economia deve rispettare i limiti del pianeta. La transizione ecologica richiede un cambiamento radicale del nostro modo di produrre e consumare.",
                "La memoria storica è fondamentale per costruire l'identità nazionale. Ricordare il passato, anche nelle sue pagine più oscure, aiuta a comprendere il presente e a progettare un futuro migliore, senza ripetere gli errori.",
                "L'intelligenza artificiale sta ridefinendo i confini della creatività umana. Mentre l'AI può generare arte e musica, la vera creatività rimane un tratto distintamente umano. La tecnologia deve essere uno strumento, non un sostituto."
            ],
            "C2": [
                "Il riconoscimento nella filosofia politica contemporanea è un tema centrale. Honneth e Taylor sostengono che il riconoscimento dell'identità e delle differenze è fondamentale per la giustizia sociale. Senza riconoscimento non c'è vera uguaglianza.",
                "Il concetto di progresso va criticato: non tutto ciò che è nuovo è meglio. La modernità ha promesso liberazione ma ha prodotto nuove forme di dominio. Serve una riflessione critica sul significato stesso del progresso.",
                "Nel capitalismo contemporaneo, l'etica sembra subordinata all'economia. La ricerca del profitto a ogni costo genera disuguaglianze e crisi. Un nuovo modello economico deve mettere al centro la giustizia sociale e il bene comune.",
                "La memoria collettiva costruisce l'identità nazionale attraverso la narrazione condivisa del passato. Tuttavia, questa memoria è spesso selettiva e strumentalizzata politicamente. È necessario un confronto aperto e critico con la storia.",
                "La tensione tra universalismo e particolarismo è al centro del dibattito culturale contemporaneo. I diritti universali devono essere conciliati con il rispetto delle differenze culturali in una società sempre più globalizzata."
            ],
        }
    },
    "CELI": {
        "scrittura": {
            "A1": [
                "Caro amico, mi presento: sono Sara, ho 23 anni e vivo a Milano. Studio architettura e mi piace viaggiare. In questo momento sto imparando l'italiano. Ciao!",
                "La mia stanza è color crema con una scrivania vicino alla finestra. C'è un letto comodo, una libreria piena di libri e un armadio. Mi piace molto la mia stanza perché è luminosa.",
                "Il mio cibo preferito è la pizza margherita. È buonissima con il formaggio filante e il pomodoro fresco. Di solito la mangio al ristorante con gli amici il sabato sera.",
                "La domenica mi alzo tardi, faccio una bella colazione e poi esco a passeggiare. Pranzo con la famiglia e il pomeriggio leggo o guardo un film. La sera ceno presto.",
                "Il mio migliore amico si chiama Marco. È alto, simpatico e gentile. Ci conosciamo da quando avevamo 5 anni. Insieme andiamo spesso al cinema e facciamo sport."
            ],
            "A2": [
                "Cari mamma e papà, sto visitando Firenze e mi sto divertendo moltissimo. La città è bellissima, ho visto il Duomo e Ponte Vecchio. Il tempo è bello. Un abbraccio, Maria.",
                "Ieri sera sono andato al ristorante con la mia famiglia. Ho mangiato gli spaghetti alle vongole come primo e una grigliata mista come secondo. Per dolce ho preso un tiramisù. Ottimo!",
                "Per il mio ultimo compleanno ho ricevuto un bel regalo dai miei amici: una chitarra acustica. Sono stato molto contento perché suonare la chitarra è il mio hobby preferito.",
                "Ciao Luca, andiamo al cinema sabato sera? Vorrei vedere il nuovo film di animazione. Ci troviamo alle 20 davanti al cinema. Fammi sapere se puoi. A presto!",
                "L'estate scorsa sono andata in vacanza al mare in Sardegna. L'acqua era limpida e la spiaggia bellissima. Mi sono divertita tantissimo e ho fatto nuove amicizie."
            ],
            "B1": [
                "Fare volontariato è stata un'esperienza meravigliosa. Ho aiutato persone bisognose e ho dedicato il mio tempo agli altri. Mi ha insegnato l'importanza della solidarietà e mi ha fatto crescere come persona.",
                "La dieta mediterranea è un patrimonio culturale italiano. È basata su cibi sani come olio d'oliva, pesce, frutta e verdura. Fa bene alla salute ed è riconosciuta come modello alimentare equilibrato.",
                "Una festa tradizionale italiana che conosco è il Carnevale di Venezia. Si celebra con maschere e costumi meravigliosi. Le persone si riuniscono in piazza San Marco per festeggiare.",
                "Gentile Professore, voglio ringraziarla per avermi insegnato tanto quest'anno. Le sue lezioni sono state stimolanti e mi hanno fatto crescere culturalmente. La ringrazio per la sua passione e dedizione.",
                "Ho soggiornato al B&B 'Il Girasole' ed è stato piacevole. La posizione è centrale, la camera pulita e la colazione abbondante. Lo consiglio per un soggiorno economico ma di qualità."
            ],
            "B2": [
                "Lo smart working offre flessibilità e autonomia, permettendo di conciliare lavoro e vita privata. Tuttavia, comporta anche isolamento sociale e difficoltà di concentrazione. Un modello ibrido sarebbe la soluzione ideale.",
                "Il patrimonio culturale italiano è unico al mondo e va valorizzato attraverso la conservazione dei monumenti, la promozione dell'arte e l'educazione delle nuove generazioni. La cultura è la nostra più grande risorsa.",
                "L'energia nucleare è un tema controverso. Da un lato, produce energia pulita senza emissioni di CO2; dall'altro, comporta rischi di incidenti e la gestione delle scorie. La decisione richiede un dibattito informato.",
                "Ho assistito a una conferenza TED sulla creatività molto stimolante. Il relatore ha parlato di come l'innovazione nasca dalla combinazione di idee diverse. L'intervento mi ha ispirato profondamente.",
                "Gentile Direttore, le scrivo per segnalare il problema del rumore nel mio quartiere. Propongo l'installazione di barriere acustiche e maggiori controlli notturni. Una soluzione possibile è la creazione di zone silenziose."
            ],
            "C1": [
                "I social media hanno un impatto profondo sulla democrazia: da un lato facilitano la partecipazione politica e la circolazione delle idee, dall'altro favoriscono la disinformazione e la polarizzazione del dibattito pubblico. È necessaria un'educazione critica ai media.",
                "Il turismo sostenibile è essenziale per preservare l'ambiente e le comunità locali. Un turismo responsabile riduce l'impatto ecologico, rispetta le culture locali e promuove uno sviluppo economico equilibrato del territorio.",
                "L'università ha il compito di formare non solo professionisti competenti ma anche cittadini critici. La formazione superiore deve promuovere il pensiero autonomo, la ricerca libera e la consapevolezza sociale per preparare al futuro.",
                "Il patrimonio culturale italiano è fondamentale per l'identità nazionale. Preservare e valorizzare questo patrimonio significa proteggere la memoria storica e la tradizione, ma anche innovare per trasmetterlo alle nuove generazioni.",
                "L'innovazione tecnologica sta trasformando il mondo del lavoro, creando nuove professioni e rendendone obsolete altre. La formazione continua e l'adattabilità sono le chiavi per affrontare con successo questa trasformazione."
            ],
            "C2": [
                "Il concetto di identità nell'era globale è caratterizzato dal meticciato culturale. Le identità non sono più fisse ma ibride, influenzate da flussi migratori e comunicazione globale. Il dialogo tra culture diverse arricchisce e trasforma.",
                "Abbiamo una responsabilità etica verso le generazioni future: le nostre scelte di oggi determineranno il mondo di domani. La sostenibilità ambientale e la giustizia sociale sono imperativi morali per un futuro vivibile.",
                "La crisi della democrazia contemporanea si manifesta nella sfiducia verso le istituzioni e nella caduta della partecipazione. Per rinnovare la democrazia servono nuovi spazi di partecipazione e una maggiore trasparenza decisionale.",
                "La filosofia nella società tecnologica ha il compito di interrogare il senso dell'umano in un'epoca di macchine intelligenti. L'umanesimo critico può guidare lo sviluppo tecnologico senza perdere di vista i valori fondamentali.",
                "La memoria storica e la riconciliazione sono processi complementari: ricordare le ingiustizie del passato è necessario per costruire un futuro di pace. Senza verità e giustizia non può esserci vera riconciliazione."
            ],
        },
        "orale": {
            "A1": [
                "La mia giornata tipo: mi sveglio alle 7, vado a scuola o al lavoro, pranzo alle 13, studio al pomeriggio e la sera mi rilasso guardando la TV.",
                "La mia famiglia è composta da tre persone: mia madre insegnante, mio padre ingegnere e io. Abbiamo un cane di nome Balù.",
                "Nel tempo libero mi piace ascoltare musica, fare sport e uscire con gli amici. Il mio sport preferito è il nuoto.",
                "Il mio paese è piccolo ma accogliente. C'è una piazza centrale con una chiesa antica e diversi negozi. La comunità è molto unita.",
                "La mia scuola è grande e moderna. I professori sono bravi e i compagni simpatici. Studio lingue straniere e informatica."
            ],
            "A2": [
                "La mia casa ideale sarebbe in campagna con un grande giardino, una cucina spaziosa e tante stanze luminose. Vicino alla natura, silenziosa e tranquilla.",
                "Il mio piatto preferito è la pasta alla carbonara. Si prepara con uova, guanciale, pecorino e pepe. È semplice ma deliziosa. La cucino spesso per i miei amici.",
                "Quando ero piccolo andavo sempre al mare con i miei genitori. Giocavo sulla spiaggia e facevo castelli di sabbia. È un ricordo bellissimo.",
                "La settimana scorsa sono andato in gita al lago. È stata una bellissima giornata di sole. Abbiamo fatto un picnic e una passeggiata nel bosco.",
                "Il mio sport preferito è il calcio. Gioco in una squadra locale e mi alleno due volte a settimana. La partita la domenica è il momento più bello."
            ],
            "B1": [
                "Il volontariato è importante nella società perché aiuta le persone in difficoltà e crea comunità più solidali. Dedicare tempo agli altri arricchisce anche chi aiuta.",
                "Conosco diverse tradizioni italiane: il Carnevale con le maschere, la Pasqua con la colomba, il Natale con il presepe. Ogni regione ha le sue usanze particolari.",
                "Il sistema scolastico italiano prevede 5 anni di elementari, 3 di medie e 5 di superiori. Poi c'è l'università. Gli esami di maturità sono molto importanti.",
                "Il turismo sostenibile rispetta l'ambiente e le comunità locali. Preferisco viaggiare in modo responsabile, evitando il turismo di massa e scegliendo strutture ecologiche.",
                "Il nord Italia è più industrializzato e ricco, mentre il sud ha un costo della vita più basso ma meno opportunità. Le differenze culturali sono affascinanti."
            ],
            "B2": [
                "L'intelligenza artificiale sta trasformando la società in modo profondo. Da un lato offre strumenti potenti per la medicina e la ricerca, dall'altro solleva questioni etiche sul controllo e la privacy. È necessario un approccio equilibrato.",
                "Lo sviluppo sostenibile integra crescita economica e rispetto ambientale. La green economy crea nuovi posti di lavoro e promuove l'innovazione. È la strada giusta per il futuro del pianeta.",
                "Le migrazioni sono un fenomeno complesso che richiede politiche di accoglienza e integrazione efficaci. L'integrazione passa attraverso il lavoro, l'istruzione e la partecipazione sociale dei migranti.",
                "La donna nella società contemporanea ha conquistato molti diritti ma persiste una disparità salariale e una sotto-rappresentazione nei ruoli di potere. La parità di genere è ancora un obiettivo da raggiungere.",
                "La crisi climatica richiede azioni urgenti a livello globale. Governi, imprese e cittadini devono collaborare per ridurre le emissioni e adottare stili di vita sostenibili. Il tempo per agire è ora."
            ],
            "C1": [
                "La globalizzazione culturale crea un dialogo tra culture diverse ma rischia anche di omologare le identità particolari. Preservare la diversità culturale è fondamentale per arricchire l'esperienza umana e promuovere la comprensione reciproca.",
                "Il rapporto tra scienza e politica è complesso: la scienza fornisce evidenze, ma la politica deve prendere decisioni considerando anche fattori sociali ed economici. Durante la pandemia, questo rapporto è stato messo alla prova.",
                "I diritti umani e l'immigrazione sono temi intrecciati. Ogni persona ha diritto a cercare una vita migliore. L'accoglienza e l'integrazione sono doveri morali oltre che obblighi giuridici internazionali.",
                "L'educazione nell'era digitale deve preparare gli studenti a un mondo in continuo cambiamento. La tecnologia è uno strumento potente, ma non deve sostituire il pensiero critico e la relazione educativa.",
                "La sostenibilità e la giustizia sociale sono due facce della stessa medaglia. Non può esserci vera sostenibilità ambientale senza equità sociale. Le politiche verdi devono tenere conto delle disuguaglianze."
            ],
            "C2": [
                "L'antropocentrismo va superato per un'etica ambientale che riconosca il valore intrinseco della natura. La crisi ecologica richiede un nuovo paradigma che superi la separazione tra umano e natura.",
                "Il concetto di verità nell'epistemologia contemporanea è problematico. Tra realismo scientifico e costruttivismo sociale, la verità appare come un orizzonte regolativo più che come una corrispondenza oggettiva.",
                "La giustizia distributiva deve affrontare le disuguaglianze globali in modo strutturale. La distribuzione ineguale delle risorse non è solo ingiusta ma anche inefficiente per lo sviluppo umano globale.",
                "Il rapporto tra tecnica e destino umano è stato analizzato da Heidegger: la tecnica non è solo uno strumento ma un modo di disvelamento che può diventare pericolo se riduce l'essere a pura disponibilità.",
                "Il pluralismo culturale e l'universalità dei diritti sono in tensione. I diritti umani devono essere universali ma anche rispettosi delle differenze culturali, in un equilibrio delicato ma necessario."
            ],
        }
    }
}

def update_html(cert, lv, s):
    """Update a single HTML file with data-answer and data-reference attributes and enhanced JS"""
    fp = os.path.join(REPO, cert, lv, f"Set_{s}", f"{cert}_{lv}_Set_{s}.html")
    if not os.path.exists(fp):
        return False
    
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()
    
    lines = html.split("\n")
    new_lines = []
    
    # Parse which grammar items this set uses
    import cils_data as cd, celi_data as ced
    data = cd.CILS if cert == "CILS" else ced.CELI
    
    grammar_items = data[lv].get("grammatica", [])
    write_items = data[lv].get("scrittura", [])
    orale_items = data[lv].get("orale", [])
    
    grammar_idx = 0
    write_idx = 0
    orale_idx = 0
    
    for line in lines:
        # Add data-answer to grammar questions
        if 'data-type="grammar"' in line and 'data-keywords=' in line:
            di = (s - 1) * 3 + grammar_idx
            if di >= len(grammar_items):
                di = grammar_idx % len(grammar_items)
            item = grammar_items[di]
            answer = item[1]  # e.g. "sono" or "sono andato|sono andata"
            # Use the first keyword as the display answer
            first_ans = answer.split("|")[0]
            # Add data-answer attribute
            if 'data-answer=' not in line:
                line = line.replace('data-type="grammar"', f'data-type="grammar" data-answer="{first_ans}"')
            grammar_idx += 1
        
        # Add data-reference to scrittura questions
        elif 'data-type="scrittura"' in line:
            wi = (s - 1) * 1 + write_idx
            if wi >= len(write_items):
                wi = write_idx % len(write_items)
            ref = ""
            try:
                ref = REFERENCES[cert]["scrittura"][lv][wi]
            except:
                # Use keywords as fallback
                kws = write_items[wi][1] if wi < len(write_items) else ""
                ref = f"Rispondi usando le parole chiave: {kws}"
            if 'data-reference=' not in line:
                ref_esc = ref.replace("'", "&#39;").replace('"', "&quot;")
                line = line.replace('data-type="scrittura"', f'data-type="scrittura" data-reference="{ref_esc}"')
            write_idx += 1
        
        # Add data-reference to orale questions
        elif 'data-type="orale"' in line:
            oi = (s - 1) * 1 + orale_idx
            if oi >= len(orale_items):
                oi = orale_idx % len(orale_items)
            ref = ""
            try:
                ref = REFERENCES[cert]["orale"][lv][oi]
            except:
                kws = orale_items[oi][1] if oi < len(orale_items) else ""
                ref = f"Rispondi usando le parole chiave: {kws}"
            if 'data-reference=' not in line:
                ref_esc = ref.replace("'", "&#39;").replace('"', "&quot;")
                line = line.replace('data-type="orale"', f'data-type="orale" data-reference="{ref_esc}"')
            orale_idx += 1
        
        new_lines.append(line)
    
    new_html = "\n".join(new_lines)
    
    # Replace the JS function sub() with enhanced version
    old_sub = """function sub(){var T=0,M=0,D=[];document.querySelectorAll('.section').forEach(function(s){var t=0,m=0;s.querySelectorAll('.question').forEach(function(q){var tp=q.getAttribute('data-type'),pt=parseInt(q.getAttribute('data-points'))||4;m+=pt;M+=pt;
if(tp==='listen'||tp==='read'){var a=parseInt(q.getAttribute('data-ans')),sl=q.querySelector('input[type="radio"]:checked'),o=q.querySelectorAll('.opts label'),u=sl?o[parseInt(sl.value)].textContent.trim():'-',c=o[a]?o[a].textContent.trim():'-';if(sl&&parseInt(sl.value)===a){t+=pt;T+=pt;q.querySelector('.feedback').className='feedback correct';q.querySelector('.feedback').innerHTML='Corretto! ('+pt+'/'+pt+')'}else{q.querySelector('.feedback').className='feedback wrong';q.querySelector('.feedback').innerHTML='Risposta: '+u+' | Corretta: '+c+' (0/'+pt+')'}var st=q.getAttribute('data-script');if(st)q.querySelector('.feedback').innerHTML+='<br><span style="font-size:12px;color:#666;">'+st+'</span>'}
else if(tp==='grammar'){var inp=q.querySelector('input[type="text"]'),ut=inp?inp.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w});var sc=kws(ut,kws);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Corretto':'Parziale')+' ('+sc+'/'+pt+')'}
else if(tp==='scrittura'||tp==='orale'){var ta=q.querySelector('textarea'),ut=ta?ta.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),base=kws(ut,kws),bonus=Math.min(5,Math.floor(wc(ut)/10)),sc=Math.min(pt,base+bonus);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Buono':'Da migliorare')+' ('+sc+'/'+pt+')'}});D.push({name:s.querySelector('h2').textContent.replace(/<span.*/,'').trim(),score:t,max:m})});"""

    new_sub = """function sub(){var T=0,M=0,D=[];document.querySelectorAll('.section').forEach(function(s){var t=0,m=0;s.querySelectorAll('.question').forEach(function(q){var tp=q.getAttribute('data-type'),pt=parseInt(q.getAttribute('data-points'))||4;m+=pt;M+=pt;
if(tp==='listen'||tp==='read'){var a=parseInt(q.getAttribute('data-ans')),sl=q.querySelector('input[type="radio"]:checked'),o=q.querySelectorAll('.opts label'),u=sl?o[parseInt(sl.value)].textContent.trim():'-',c=o[a]?o[a].textContent.trim():'-';if(sl&&parseInt(sl.value)===a){t+=pt;T+=pt;q.querySelector('.feedback').className='feedback correct';q.querySelector('.feedback').innerHTML='Corretto! ('+pt+'/'+pt+')'}else{q.querySelector('.feedback').className='feedback wrong';q.querySelector('.feedback').innerHTML='Risposta: '+u+' | Corretta: '+c+' (0/'+pt+')'}var st=q.getAttribute('data-script');if(st)q.querySelector('.feedback').innerHTML+='<br><span style="font-size:12px;color:#666;">'+st+'</span>'}
else if(tp==='grammar'){var inp=q.querySelector('input[type="text"]'),ut=inp?inp.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ans=q.getAttribute('data-answer')||kws[0]||'';var sc=kws(ut,kws);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Corretto':'Parziale')+' ('+sc+'/'+pt+')<br><span style="font-size:12px;color:#1565C0;">Risposta corretta: '+ans+'</span>'}
else if(tp==='scrittura'||tp==='orale'){var ta=q.querySelector('textarea'),ut=ta?ta.value.trim():'',kws=(q.getAttribute('data-keywords')||'').split('|').filter(function(w){return w}),ref=q.getAttribute('data-reference')||'';var base=kws(ut,kws),bonus=Math.min(5,Math.floor(wc(ut)/10)),sc=Math.min(pt,base+bonus);t+=sc;T+=sc;q.querySelector('.feedback').className='feedback '+(sc>=pt*0.6?'correct':'wrong');q.querySelector('.feedback').innerHTML=(sc>=pt*0.6?'Buono':'Da migliorare')+' ('+sc+'/'+pt+')'+(ref?'<br><span style="font-size:12px;color:#1565C0;">Risposta di riferimento: '+ref+'</span>':'')}
});D.push({name:s.querySelector('h2').textContent.replace(/<span.*/,'').trim(),score:t,max:m})});"""
    
    if old_sub in new_html:
        new_html = new_html.replace(old_sub, new_sub)
    
    with open(fp, "wb") as f:
        f.write(new_html.encode("utf-8"))
    return True

# Main
import cils_data as cd, celi_data as ced

count = 0
for cert in ["CILS", "CELI"]:
    for lv in LEVELS:
        for s in range(1, 6):
            if update_html(cert, lv, s):
                count += 1
                print(f"  Updated {cert}/{lv}/Set_{s}")

print(f"Done: {count} HTML files updated")

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
                
                data = json.dumps({"message": "Show correct answers + reference answers", "content": content, "branch": "master", "sha": sha} if sha else {"message": "Show correct answers + reference answers", "content": content, "branch": "master"})
                r2 = urllib.request.Request(url, method="PUT", data=data.encode(), headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github.v3+json", "Content-Type": "application/json"})
                try:
                    json.loads(urllib.request.urlopen(r2, timeout=30).read())
                    pushed += 1
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 409 and attempt < 2:
                        time.sleep(2)
                        continue
                    break
            time.sleep(0.3)

print(f"Pushed: {pushed}/{count}")
