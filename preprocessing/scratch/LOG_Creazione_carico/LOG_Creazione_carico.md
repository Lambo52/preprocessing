## Summary

| 1.   | Introduzione creazione, modifica ed eliminazione di un carico .................................................1                 |
|------|----------------------------------------------------------------------------------------------------------------------------------|
| 2.   | Quando creare, modificare o eliminare un carico ....................................................................1            |
| 3.   | Comegestire un carico..........................................................................................................2 |
| 3.1. | Creazione di un carico.................................................................................................... 2     |
| 3.2. | Lancio di un carico......................................................................................................... 2   |
| 3.3. | Modifica di un carico...................................................................................................... 4    |
| 3.4. | Eliminazione di un carico................................................................................................        |

Last revision date: 28.11.2025

Author: Bortolotti Francesco

## 1. Introduzione creazione, modifica ed eliminazione di un carico

Le procedure logistiche per la creazione e la modifica dei carichi vengono effettuate quotidianamente dall'ufficio addetto al carico. La creazione del carico consiste nel selezionare gli ordini relativi ad un certo camion/container e 'lanciarli' fuori del MAV nel caso si trovino all'interno, o comunque andarli a  prendere  per  portarli  vicino  alle  piazzole  nel  caso  siano  sparsi  per  le  zone  di  stoccaggio dell'impianto.

Per  quanto  riguarda  la  modifica  invece,  permette  di  gestire  i  carichi  già  esistenti,  sia  che  abbia necessità  di  rimuovere  alcune  palette  dal  carico  di  un  camion/container  in  programma,  sia  che magari debba spostare delle UDS un carico ad un altro già esistente.

## 2. Quando creare, modificare o eliminare un carico

I carichi vengono creati e lanciati dall'ufficio addetto ai carichi prima che arrivi il camion/container relativo ad un certo ordine in modo il carico del mezzo possa avvenire in maniere fluida e corretta. Devo modificare un carico quando per un qualsiasi motivo ho bisogno di togliere delle palette da un carico o magari spostarle su un altro. Devo invece eliminare un carico quando per qualsiasi ragione il camion/container è stato annullato e devo liberare il materiale impegnato per quel viaggio.

<!-- image -->

## PROCEDURA CREAZIONE, MODIFICA ED ELIMINAZIONE DI UN CARICO

## Procedura logistica

## 3. Come gestire un carico

## 3.1. Creazione di un carico

La creazione di un carico avviene principalmente  tramite la registrazione dei camionisti al totem: quando il mezzo arriva in Atlas Concorde, tramite il check-in effettuato in ufficio spedizioni, il sistema crea in automatico il carico su WAMAS con le palette associate.

Più  raro  è  il  caso  in  cui,  per  qualsiasi  ragione,  il  carico  debba  essere  creato  manualmente  dal dipartimento di Logistica. In questo caso, la procedura per la creazione è la seguente:

- -Accedo alla pagina LD011
- -Seleziono in 'Origine' la vista 'Unità di carico camion'
- -Premo 'Crea' per creare un nuovo carico
- -A tentativi, inserisco le ultime 3 cifre del camion/container fittizio da creare finché non trovo una combinazione libera
- -Premo 'Applica' per creare il camion/container
- -Il camion/container creato compare nella vista 'Destinazione'

L'interfaccia LD012 "Crea carico" permette di configurare un nuovo carico con dettagli come numero camion, ora di partenza (impostata su "oggi" alle 17:45), tipo di spedizione (P), e modello di camion. La sezione "Veicolo di trasporto" è vuota e attualmente non mostra alcun veicolo selezionato, con un campo di ricerca e una griglia di risultati vuota. I pulsanti "Applica" e "Annulla" sono evidenziati, indicando che l'utente può confermare o annullare le impostazioni fatte.

<!-- image -->

A questo punto, il camion nuovo sarà stato creato e potrò spostarci sopra i pallet di materiale che servono.

## 3.2. Lancio di un carico

Per lanciare un carico, i passaggi sono i seguenti:

- -Accedo alla pagina LD001 di WAMAS
- -Nei filtri ricerco il camion/container di cui voglio lanciare il carico
- -Clicco tasto destro sulla riga del camion/container ricercato
- -Seleziono 'Modifica punto di carico…'

<!-- image -->

<!-- image -->

L'immagine mostra l'interfaccia di un sistema di gestione dei camion, con una lista di camion in attesa di caricamento o spostamento, identificati da numeri di spedizione e tipi di camion. Un menu contestuale è aperto su un camion selezionato, evidenziando l'opzione "Modifica punto di carico" come azione principale disponibile. La schermata include filtri di ricerca, campi per l'ora di partenza e partner, e una tabella con dettagli di appuntamenti e priorità per ogni camion.

<!-- image -->

- -Viene visualizzata una finestra LD501
- -Ricerco e seleziono il varco (la piazzola di carico) in cui voglio caricare il mezzo
- -Mi sposto sulla pagina OG002 di WAMAS
- -In 'Ricerca avanzata' nella vista 'Camion' inserisco il numero del camion/container
- -Seleziono tutte le righe relative a quel camion/container e clicco tasto destro
- -Seleziono 'Approva buffer uscita merci'

L'interfaccia mostra la modifica di un punto di carico (LD501) per una consegna in uscita, con codice OBD0001197434 e sistema WAMAS. È attivo un campo di ricerca per selezionare un varco di uscita, con una lista di dock disponibili come Dock CA-ATL-002, Dock CA-ATL-004, ecc. Sotto la lista, sono visibili record storici di consegne con date e orari, tra cui una consegna di oggi alle 08:00 e una del giorno precedente alle 16:44.

<!-- image -->

<!-- image -->

L'interfaccia mostra la schermata "Panoramica consegne in uscita" di un sistema logistico, con un menu contestuale aperto che elenca azioni come "Approva buffer uscita merci" e "Analizza approntamento scorte". Un record selezionato indica il tipo di carico "Camion" e il numero di ordine "S20251128123", con un'elenco di consegne in basso. La schermata include campi per lo stato, l'ora di partenza e il fornitore, con un'indicazione di avanzamento per ogni consegna.

<!-- image -->

## 3.3. Modifica di un carico

Quando devo spostare alcune palette già associate ad un camion/container in un altro viaggio già esistente, i passaggi da seguire sono:

- -Accedo alla pagina LD001 di WAMAS
- -Nei filtri ricerco il camion/container di cui voglio lanciare il carico
- -Clicco tasto destro sulla riga del camion/container ricercato
- -Seleziono 'Gestisci carico'
- -Viene visualizzata la pagina LD011
- -Seleziono in 'Origine' la vista 'Unità di carico camion'
- -Premo la lente in alto a destra del pannello in basso 'Destinazione' per visualizzare i carichi
- -Seleziono quello su cui voglio spostare le palette e si evidenzierà di verde

L'immagine mostra l'interfaccia di un sistema di gestione logistica, specificamente la schermata "Panoramica camion" per il camion identificato come S20251128001. È evidenziata la voce "Gestisci carico" nel menu contestuale, indicando l'azione disponibile per la gestione del carico associato a quel camion. La lista dei risultati mostra altri camion con i relativi numeri di identificazione, lo stato di carico (Dock CA), e date di partenza o termine di applicazione.

<!-- image -->

<!-- image -->

- -Nella  vista  origine  seleziono  la  o  le  palette  che  voglio  spostare  sul  carico  selezionato  in 'Destinazione'
- -Clicco la freccia verso il basso posta tra i due pannelli 'Origine' e 'Destinazione'
- -Termino cliccando 'Esegui consolidamento'

L'interfaccia mostra due sezioni principali: 'Origine' per la gestione dei carichi di camion in partenza e 'Destinazione' per il monitoraggio dei carichi in transito, con colonne che indicano stato, partner, date e avanzamento. Un'area evidenziata in rosso nella sezione 'Destinazione' segnala un carico con stato 'In corso' e peso zero, mentre un'altra riga evidenziata in verde mostra un carico 'Attivo' con avanzamento 'Fucking' e peso zero. In basso, una barra di stato riassume i dati aggregati: peso lordo, volume, merci pericolose e superficie normalizzata, tutti con valori zero, indicando un carico non ancora attivo o completato.

<!-- image -->

## 3.4. Eliminazione di un carico

Per eliminare totalmente o parzialmente un carico ho due possibilità. La prima la utilizzo quando devo eliminare una paletta singola, oppure più pallette associate allo stesso OBD. Introducendo la logica dietro a questa prima possibilità, posso annullare alcune palette dal carico di un mezzo direttamente dalla pagina LD001, in vista 'Dettagli', solo se il materiale appartiene allo stesso OBD :

- -Accedo alla pagina LD001 di WAMAS
- -Nei filtri ricerco il camion/container di cui voglio lanciare il carico
- -Accedo alla vista 'Dettagli' per visualizzare le UDS relative a quel carico
- -Seleziono la paletta singola da eliminare dal carico o più palette ma relative allo stesso OBD
- -Clicco tasto destro
- -Seleziono l'opzione 'Annullamento spedizione in corso'

<!-- image -->

L'immagine mostra una schermata di un sistema di gestione logistica che elenca camion in attesa di consegna, con dettagli come peso lordo, ora di partenza e partner di sistema (WAMAS). In basso, un menu contestuale è aperto su una spedizione, evidenziando l'opzione "Annullamento spedizione in corso..." come azione principale disponibile. L'interfaccia include anche un'area "Dettagli" con informazioni sulle unità di carico e le consegne in uscita, indicando lo stato attivo delle spedizioni.

<!-- image -->

La seconda opzione viene utilizzata quando devo eliminare dei pallet appartenenti ad OBD diversi. In questo caso la logica consiste nel creare un nuovo mezzo fittizio dove caricare le pallette da annullare per poi cancellare il mezzo stesso:

- -Accedo alla pagina LD001 di WAMAS
- -Nei filtri ricerco il camion/container di cui voglio eliminare parte del carico
- -Clicco tasto destro sulla riga del camion/container ricercato
- -Seleziono 'Gestisci carico'
- -Viene visualizzata la pagina LD011
- -Seleziono in 'Origine' la vista 'Unità di carico camion'
- -Premo 'Crea' per creare un nuovo carico
- -A tentativi, inserisco le ultime 3 cifre del camion/container fittizio da creare finché non trovo una combinazione libera
- -Premo 'Applica' per creare il camion/container

<!-- image -->

L'interfaccia LD012 "Crea carico" permette di immettere dati per un nuovo carico, come il numero del camion, l'ora di partenza (impostata a oggi alle 17:45), il tipo di spedizione (P) e il modello del camion. Nella sezione "Veicolo di trasporto" è presente una tabella vuota per l'associazione dei veicoli, con un campo di ricerca e vari strumenti di filtro e gestione. In basso sono presenti i pulsanti "Applica" e "Annulla" per confermare o cancellare le modifiche.

<!-- image -->

- -Il camion/container creato compare nella vista 'Destinazione' e lo seleziono
- -Seleziono nel pannello origine le palette da annullare
- -Premo la freccia verso il basso per spostare le palette desiderate
- -Termino cliccando 'Esegui consolidamento'
- -Torno nella pagina LD001
- -Ricerco il camion/container fittizio appena creato
- -Clicco tasto destro e lo annullo selezionando 'Annulla camion'

L'immagine mostra una schermata di un sistema di gestione logistica con una lista di camion e i loro pesi lordi, dove l'opzione "Annulla camion..." è evidenziata in rosso, indicando un'azione disponibile per annullare un camion selezionato. A destra, un menu contestuale elenca diverse operazioni di pianificazione e gestione, tra cui approvazioni, creazione di ordini e modifiche specifiche per la consegna. La tabella evidenzia i dati dei camion, inclusi i codici, i varchi e i pesi, con una riga selezionata (S20251128004) che mostra un peso lordo di 11.659.

<!-- image -->