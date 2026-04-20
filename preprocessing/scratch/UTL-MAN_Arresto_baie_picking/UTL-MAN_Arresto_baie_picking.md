<!-- image -->

## PROCEDURA ARRESTO BAIE PICKING

## Procedura specifica UTL e Manutenzione

## Summary

| 1.   | Introduzione procedura per l'arresto dalle baie di picking ........................................................1              |
|------|-----------------------------------------------------------------------------------------------------------------------------------|
| 2.   | Quando si arresta una baia di picking .....................................................................................1      |
| 3.   | Comesi arresta una baia di picking ........................................................................................2      |
| 4.   | Accelerazione dell'arresto .....................................................................................................3 |
| 4.1. | Cancellazione ordine ..................................................................................................... 3      |
| 4.2. | Ripristino ordine cancellato............................................................................................ 5        |

Last revision date: 20.11.2025

Author: Bortolotti Francesco

## 1. Introduzione procedura per l'arresto dalle baie di picking

La procedura per l'arresto delle baie di picking ha lo scopo di permettere il regolare svolgimento delle attività che andranno svolte direttamente sulla stazione stessa. Infatti, molteplici sono le tasks che possono essere svolte solo quando la baia è in stato di arresto. Gli esempi più comuni sono il cambio pinza, la creazione, modifica o eliminazione di un terminale dalla baia, ecc…

In questa procedura verrà spiegato anche come accelerare l'arresto di una baia in caso un'urgenza.

## 2. Quando si arresta una baia di picking

Ogniqualvolta si voglia eseguire un ' attività sulla baia di picking, questa deve essere in stato di arresto.

## 3. Come si arresta una baia di picking

Prima di eseguire un'operazione sulla baia di picking , bisogna assicurarsi che questa sia in stato di ARRESTO. Se così non fosse, non sarebbe possibile eseguire nessuna attività sulla suddetta baia.

Per arrestare una baia, ci si connette alla pagina di WAMAS WH083 e si preme 'cerca' senza inserire nessun parametro di ricerca per mostrare l'elenco completo delle baie.

L'immagine mostra l'interfaccia di un sistema di gestione delle postazioni di lavoro, con un'area di ricerca per filtri come magazzino, tipo di attrezzo e stato della postazione. Il risultato della ricerca elenca 16 postazioni, tra cui alcune in stato di "Arresta" e altre attive con processi come "Picking MVU" o "Controllo unità di...". È possibile identificare i nomi delle postazioni (es. HBW01, Manual01) e i loro tipi di attrezzo e di postazione, con una colonna di controllo per ogni riga.

<!-- image -->

Premere tasto destro sulla stazione desiderata ,  poi 'Attiva processo' per mostrare una finestra di WH086 dove la prima opzione dell'elenco è 'Arresta'. Cliccarci sopra per mandare in arresto la baia.

L'interfaccia mostra un elenco di bay di picking (HWB01-HWB16) con lo stato "STANDARD" o "GRANDI DIMENS..." e il bay HWB03 selezionato. Un pannello a destra, intitolato "WH086 | Seleziona processo", offre opzioni operative come "Arresta", "Consolidamento MvU personalizzato", "Controllo MvU", "Picking MvU", e comandi di disconnessione. L'utente può avviare un processo specifico o disconnettersi dal sistema.

<!-- image -->

<!-- image -->

<!-- image -->

Premendo  'Arresta',  la  baia  non  si bloccherà  istantaneamente,  ma  solo  dopo  aver  finito  di processare  tutti  gli  ordini  già  precedentemente  associati  ad  essa  prima  del  click  sull'opzione 'Arresta'.

## 4. Accelerazione dell'arresto

Per velocizzare l'attivazione dello stato di arresto di una baia , si possono cancellare alcuni degli ordini in coda alla stessa, in maniera tale che non appena venga processato l'ordine corrente, la stazione verrà immediatamente bloccata. Ci sono però delle considerazioni da tenere conto.

## 4.1. Cancellazione ordine

Per prima cosa, dopo aver messo la baia in stato di arresto, ci si connette alla pagina di WAMAS OG039; si preme poi ' Cerca ' senza filtri e viene mostrata la lista di tutti gli ordini di picking associati alle stazioni. Il numero della baia è visibile alla colonna ' Baia di picking ' .  Per velocizzare il blocco della baia si possono eliminare gli ordini in coda a quella stazione le cui righe sono tutte in stato di 'Nuovo'. Se è presente anche solo una riga in stato 'Attivo', allora non sarà possibile eliminare quella riga  per  velocizzare  l'arresto  e  bisognerà  attendere  che  venga  processata. Per  verificare  lo  stato dell ' ordine, selezionare la riga associata alla baia desiderata e aprire la vista ' Dettagli ' in basso.

Se per errore viene eliminato un ordine che ha una riga in stato 'Attivo', la baia si pianterà e per farla ripartire sarà necessario chiamare l'assistenza che effettuerà un intervento per risolvere con spese a carico dell'azienda.

Come esempio, supponiamo di aver messo in stato di arresto la baia 7:

L'immagine mostra un elenco di ordini di picking attivi, con dettagli come numero ordine, destinatario, area di picking e stato di avanzamento, evidenziando un ordine specifico (n. 6085996) in stato "Attivo" e associato all'area HW07. Nella sezione "Dettagli", è visibile l'attività di picking corrente, con tre sequenze attive, tutte in stato "Attivo" o "Nuovo", e l'articolo ATLA1A in fase di prelievo. L'interfaccia include anche campi per l'addetto al picking (es. fd1108) e informazioni sulla quantità pianificata e prelevata.

<!-- image -->

In  questa stazione sono presenti al momento due ordini. Come mostrato sopra in figura, il primo ordine presenta 3 righe, di cui la prima in stato di attivo:  questa non potrà essere cancellata per velocizzare l'arresto della stazione.

<!-- image -->

L'immagine mostra una schermata di un sistema di gestione logistica, con una tabella che elenca ordini di picking in corso, evidenziando un ordine specifico (riga 24) con destinatario "F. BERGMANN KG - CENTRUM GRAZ" e area di picking "pStations HW07". In basso, la sezione "Dettagli" indica che è stata selezionata l'attività "Nuovo" per il prelievo di un articolo, con codice "ATLAMP" e descrizione "BOOST PEARL 60X120RT", pronto per essere gestito.

<!-- image -->

Il secondo ordine relativo alla baia 7 invece, presenta solo una riga ed in stato di 'Nuovo'. Possiamo quindi eliminarla e fare in modo che la baia si arresti senza aver processato anche questo ordine guadagnando del tempo.

Bisogna tenere in mente che dopo aver eliminato un ordine di picking, questo dovrà essere ripristinato manualmente. Prima di cancellarlo, quindi, è buona regola salvarsi tra gli appunto l'OBD associato all'ordine che stiamo  cancellando dalla colonna ' Consegna  in uscita ' , per poi riattivarlo manualmente  una  volta  terminata  l'attività  per  la  quale  abbiamo  dovuto  bloccare  la  stazione  di lavoro.

Dopodiché, tasto destro sull'ordine da cancellare in OG039 e selezionare l'opzione 'Termina ordine di picking…'. Verrà una mostrata una finestra di conferma. Premere 'OK' e l'ordine verrà eliminato. A questo punto l'arresto della baia sarà stato accelerato grazie al minor numero di ordini presenti in coda.

L'immagine mostra una schermata di un sistema di gestione logistica con una lista di ordini di picking, dove l'ordine numero 6086010 è selezionato e mostra un menu contestuale con opzioni come "Termina ordine di picking" e "Visualizza...". Il campo "Consegna in uscita" per l'ordine selezionato contiene il codice OBD0001190513, e lo stato è "Attivo". In basso, la sezione "Dettagli" visualizza l'attività di picking, con la prima riga indicante lo stato "Attivo" e una sequenza di 0.

<!-- image -->

## 4.2. Ripristino ordine cancellato

Come già accennato, una volta eliminato un ordine dovrà essere ripristinato manualmente. Per fare ciò, dopo aver salvato l'OBD (come detto sopra), bisogna andare in OG002 e cercare l'OBD salvato per filtrare il nostro ordine. Inserire quindi il codice OBD nella cella di testo ' Numero della consegna in uscita ' .

In  sequenza  selezionare  le  opzioni  'Approva  per  pianificazione  di  picking…'  e  poi  'Approva  per picking…'. Fatto ciò, in base alle priorità prima o poi l'ordine tornerà in coda ad una baia adibita per processarlo.

L'immagine mostra un'interfaccia di gestione ordini di consegna, con un menu contestuale aperto su un record specifico (numero di consegna OBD0001190513). Il menu offre opzioni per modificare, duplicare o approvare vari passaggi logistici, tra cui pianificazione della spedizione, picking e caricamento diretto. In basso a destra, un campo visualizza lo stato dell'ordine come "Attivo" con un'avanzamento del 90%.

<!-- image -->

<!-- image -->