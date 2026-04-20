## Summary

|   1. | Introduzioneprocedura per la creazione di nuoveunità di carico .......................................... 1         |
|------|---------------------------------------------------------------------------------------------------------------------|
|    2 | Quando crearenuoveunità di carico ............................................................................... 1 |
|    3 | Comecrearenuove unità di carico ..................................................................................  |

Last revision date: 28.10.2025

Author: Bortolotti Francesco

## 1. Introduzione procedura per la creazione di nuove unità di carico

La procedura logistica la creazione di una nuova UDC è necessaria appunto quando bisogna creare una nuova unità di carico logica. L'unità di carico fisica esiste ed è pronta, ma su WAMAS per qualche ragione non esiste ancora e c'è necessità di movimentarla. Per farlo è però prima necessario creare l'UDC logica sul WMS per poterla gestire.

## 2. Quando creare nuove unità di carico

Creare  delle  nuove UDC logiche  è un'operazione  rara che viene  fatta per  gestire  pallet speciali di materiale  che  non  esce  dal  reparto  produttivo.  Esempi  possono essere  delle  UDC  contenenti  i supporti per le pinze da picking, oppure, caso più comune, pallet pieni di documenti amministrativi che vengono stoccati nel MAV1 per liberare spazio dagli uffici. Questi pallet hanno bisogno della loro UDC logica sul WMS per essere movimentati e gestiti (es: stoccati nel MAV).

Può  anche  capitare  il  caso  in  cui  sia  necessario  ricreare  un  pallet  per  motivazione  riguardanti l'inventario o per la ricezione di pallet non gestiti.

<!-- image -->

## PROCEDURA CREAZIONE NUOVA UDC

## Procedura pubblica

## 3. Come creare nuove unità di carico

Per creare  una nuova UDC si parte dalla pagina SM023 su WAMAS. Si clicca tasto destro in un'area vuota e cliccare 'Nuova'

L'immagine mostra l'interfaccia del modulo SM023 per la gestione delle unità di carico in un sistema ERP, con un campo di ricerca e filtri per ID UDC, base di carico, magazzino e posto di stoccaggio. È evidenziato il menu contestuale "Nuova..." che offre opzioni per creare nuove unità di carico, modificare, annullare ordini di trasporto, stampare etichette o eseguire prelievi spontanei. La sezione "Risultato di ricerca" è vuota, indicando che nessun record è stato trovato con i criteri attuali.

<!-- image -->

Si aprirà così la finestra SM028 ; nella vista 'Unità di carico' andranno compilati i seguenti campi:

- -Unità di carico : inserire il codice della UDC che si vuole creare
- -Posto di stoccaggio :
- o 'Magazzino' :  cliccare sulla lente di ricerca e selezionare l'unica opzione disponibil e
- o 'Posto di stoccaggio' : selezionare il posto di stoccaggio in cui si trova l'UDC fisica
- -Identificazione del posto di stoccaggio : si compilerà automaticamente compilando la cella 'Posto di stoccaggio'
- -Base di carico : selezionare il tipo di pallet utilizzato per l'UDC
- -Cubatura della base di carico : selezionare l'altezza dell'UDC
- -Grafo  flusso  merci : selezionare  l'opzione  desiderata  (es:  se  l'UDC  deve  essere  stoccata all'interno del MAV, scegliere 'InHBW' )

<!-- image -->

<!-- image -->

L'immagine mostra la schermata SAP SM028 per la modifica di un'unità di carico (Udc), con l'ID Udc "WH1" selezionato. L'interfaccia evidenzia campi come il posto di stoccaggio, la base di carico, le dimensioni e il peso lordo, tutti ancora vuoti o con valori zero, e include un pulsante per visualizzare il "Grafo flusso di merci". Il tab attivo è "Unità di carico", indicando che si sta configurando la definizione base dell'unità di carico stessa.

<!-- image -->

Completata questa prima fase, bisognerà passare alla vista Stock Object, cliccare tasto destro in uno spazio vuoto e selezionare 'Crea record di dati' e compilare i seguenti campi:

- -Versione di imballaggio articolo :
- o ' Cliente ' : cliccare sulla lente di ricerca e selezionare l'unica opzione disponibile
- o ' Numero dell'articolo' :  selezione  l'opzione  desiderata  (es:  in  caso  di  documenti amministrativi selezionare ATLDOCU)
- o ' Variante ' : si compilerà automaticamente compilando la cella 'Numero dell'articolo'
- o ' Versione ' : cliccare sulla lente di ricerca e selezionare l'unica opzione disponibile
- -Descrizione  dell'articolo : si  compilerà  automaticamente  compilando  la  cella  'Numero dell'articolo'
- -Classificazione della scorta : generalmente selezionare 'Normal'
- -Proprietario  della  merce :  cliccare sulla  lente  di  ricerca  e  selezionare  l'unica  opzione disponibile
- -Tipo UDC : cliccare sulla lente di ricerca e selezionare l'unica opzione disponibile
- -Scelta : selezionare la scelta desiderata
- -Tono : selezionare il tono desiderato
- -Calibro : selezionare il calibro desiderato
- -Quantità : selezionare la quantità desiderata

<!-- image -->

L'immagine mostra la schermata di modifica di un oggetto di stock (SM031) in un sistema ERP, con il codice 66663333 e la posizione WH1, dove sono visibili i campi per la descrizione dell'articolo ('ARCHIVIO AMMINISTRAZIONE'), la classificazione ('Normal'), il lotto ('2019'), e i dati personalizzati quali 'TipoUdc 001', 'Tono 2019', e 'Calibro 9'. La quantità è impostata a 1 pezzo, e la sezione inferiore evidenzia il pulsante 'Salva' come azione principale per confermare le modifiche.

<!-- image -->

Compilati questi  campi, cliccare  su ' salva '.  Si  aprirà  un'ultima  finestra  SM035 in cui  bisognerà inserire la chiave di registrazione e il numero documento. La chiave di registrazione è il motivo per cui si sta creando il nuovo pallet. In base alle chiave di registrazione inserita, il nuovo stock object creato (il  materiale sopra alla base di carico) viene registrato o meno all'interno del  gestionale aziendal e (AS400). Ad esempio, RG+ è la chiave di registrazione che genere giacenza solo su WAMAS, mentre PV crea giacenza anche sul gestionale. ' Numero di documento ' solitamente si imposta come valore 1.

L'immagine mostra la finestra di conferma delle modifiche (SM035) per un oggetto di stock, con il campo "Chiave registrazione" evidenziato e pronto per l'inserimento. È visibile il prefisso utente "FB" e un campo vuoto per il numero del documento, impostato sulla data "oggi". La finestra include pulsanti "OK" e "Annulla" per confermare o annullare le azioni.

<!-- image -->

<!-- image -->

Una volta cliccato su 'OK' verrà visualizzata a schermo un'ultima finestra di avviso su cui bisognerà cliccare 'OK' nuovamente.

L'immagine mostra una finestra di errore del sistema FW016 che segnala l'insuccesso dell'aggiornamento del grafo del flusso di merci. Il messaggio specifica che non è stato trovato alcun grafo del flusso di merci per l'unità di cui si sta cercando di aggiornare i dati. La finestra presenta un'icona di avviso gialla e un pulsante OK per chiudere la notifica.

<!-- image -->

La nuova UDC è stata così creata e può essere gestita logicamente.