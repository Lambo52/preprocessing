## Summary

| 1.   | Introduzione procedura refresh e reset degli ordini di trasporto ................................................1        |
|------|---------------------------------------------------------------------------------------------------------------------------|
| 2.   | Quando usare il refresh - reset degli ordini di trasporto............................................................1    |
| 3.   | Comeusare il refresh - reset degli ordini di trasporto...............................................................2    |
| 3.1. | Ordine di trasporto bloccato........................................................................................... 2 |
| 3.2. | UDCbloccata in buffer sorgente all'interno dell'anello ..................................................... 2            |
| 3.3. | Mancanza di rotta dell'UDC ............................................................................................ 3 |
| 3.4. | Incongruenza logica tra WAMASeLighthouse.................................................................. 3              |

Last revision date: 12.11.2025

Author: Bortolotti Francesco

## 1. Introduzione procedura refresh e reset degli ordini di trasporto

La procedura logistica per il refresh e il reset degli ordini di trasporto ha l'obiettivo di sbloccare degli ordini di trasporto che per qualche motivo si sono bloccati. Le ragioni non sempre sono conosciute, ma quando un ordine di trasporto non presenta apparenti problemi, ma comunque non parte o non si attiva, spesso un refresh e un reset riesce nello sbloccarlo e rifarlo partire.

Inoltre, ci sono altri casi nella che verranno spiegati nel capitolo 'Quando' dove il refresh/reset torna utile.

## 2. Quando usare il refresh -reset degli ordini di trasporto

Le funzioni refresh e reset vengono utilizzati principalmente in quattro casi differenti:

1. Quando su WAMAS ho un ordine di trasporto in stato 'Nuovo' o 'Attivo' da tanto tempo, ma il pallet non si muove.
2. Quando  ho  un  pallet  bloccato  in  uno  dei  buffer  sorgenti  delle  baie  di  picking all'interno dell'anello .
3. Se su WAMAS nella pagina MF200 non riesco a vedere la rotta associata ad una certa UDC con ordine di trasporto ' attivo ' .
4. Quando su WAMAS vedo una UDC in una certa locazione  che  però  non  risulta  essere  su Lighthouse e quindi è presente un disallineamento logico tra i due sistemi.

<!-- image -->

## PROCEDURA REFRESH E RESET DEGLI ORDINI DI TRASPORTO

## Procedura specifica UTL

<!-- image -->

Generalmente,  quindi,  la  procedura  del  refresh/reset  di  un  ordine  di  trasporto  viene  utilizzata ogniqualvolta  esistono  TPO  (transport  order)  bloccati  per  ragioni  sconosciuti  o  disallineamenti fisici/logici tra la reale posizione di una paletta e la posizione rilevata dal sistema. Riassumendo, il refresh/reset, è il primo tentativo per qualsiasi tipo di problema con gli ordini di trasporto.

## 3. Come usare il refresh -reset degli ordini di trasporto

Per  attivare  il  refresh  e  il  reset  degli  ordini  di  trasporto  si  accede  alla  pagina  MF200  di  WAMAS. Dopodiché selezionare l'unica opzione disponibile nel campo 'Servizio MFS in esecuzione': 'mfsPal' e  nella  vista  'Ricerca  avanzata'  inserire  il  numero  di  UDC  sul  quale  l'ordine  di  trasporto  non  sta funzionando a dovere.

L'immagine mostra l'interfaccia di gestione delle unità di carico nel sistema MF200, con un'unità di carico identificata come 70805545 selezionata. Da un menu contestuale aperto, sono evidenziate le azioni "Refresh From Database" e "Reset Transport Order", indicando funzionalità per aggiornare o ripristinare lo stato dell'ordine di trasporto. L'interfaccia include campi di ricerca avanzata e una tabella che visualizza i dettagli dell'unità di carico, inclusi l'ID, la base di carico e il nodo.

<!-- image -->

Cliccando il tasto destro del mouse sulla riga dell'UDC visualizzata, compaiono i comandi 'Refresh From Database' e 'Reset Transport Order', insieme ad un'altra serie di opzioni che vedremo più avanti.

## 3.1. Ordine di trasporto bloccato

Il primo caso che descriviamo in cui si deve usare il refresh/reset è quando un ordine di trasporto è apparentemente 'impallato': quando lo stato dell'ordine di trasporto è in 'Nuovo' da tanto tempo, oppure lo stato è in 'Attivo' ma comunque non parte, allora il primo tentativo per sbloccarlo deve essere  il  refresh  e  il  reset  dell'OT  in  questione  dalla  pagin a  MF200  di  WAMAS.  Spesso  questa procedura sblocca l'ordine di trasporto senza bisogno di dover intervenire con metodi più ortodossi. Premere  quindi  'Refresh  From  Database'  e  successivamente  'Reset  Transport  Order'  in  questo ordine per effettuare la procedura.

## 3.2. UDC bloccata in buffer sorgente all'interno dell'anello

Quando capita che per qualche motivo l'UDC risulta bloccata all'interno di uno dei buffer sorgente all'interno dell'anello, l'operazione dalla MF200 da eseguire è 'CancelRequestEMS' per cancellare la richiesta e farla rielaborare dal sistema. Dopodiché, di nuovo refresh e reset e l'UDC dovrebbe essere sbloccata.

<!-- image -->

L'immagine mostra un menu contestuale di un'applicazione di gestione logistica, con l'opzione "CancelRequestEMS" evidenziata da un cerchio rosso, indicando un'azione per annullare una richiesta di trasporto EMS. Il menu è aperto su un record con ID Udc "70805545" visualizzato in una tabella di risultati di ricerca. La finestra include anche altre funzioni come "Refresh From Database", "Replanning Route", e "Reset Transport Order", suggerendo un contesto operativo di pianificazione e gestione delle consegne.

<!-- image -->

## 3.3. Mancanza di rotta dell'UDC

Può capitare che andando nella vista dettagli, nella vista 'Rotta' della pagina MF200 questa non sia presente.

L'immagine mostra un'interfaccia di sistema che visualizza i dettagli di un'unità di carico (UdC) con ID 70805545, indicando che è stata inizializzata e che la sua posizione attuale è TPSF01C1521. La sezione "Rotta", evidenziata in rosso, contiene informazioni sulla traccia della sua ultima posizione di stoccaggio, specificando TPSF01C1511, AISLE-HRA07, PalletRack071.

<!-- image -->

In questo caso l'opzione da selezionare è 'Replanning Route' e poi refresh e reset per riavviare la rotta dell'ordine di trasporto bloccato.

L'immagine mostra un menu contestuale aperto su un risultato di ricerca, con l'opzione "Replanning Route" evidenziata da un cerchio rosso, indicando un'azione di pianificazione alternativa della rotta. Il risultato selezionato ha l'ID UdC 70805545 e si riferisce a un nodo TPSF01C1511. Il contesto suggerisce un sistema di gestione logistica o di trasporto, dove l'utente può modificare la pianificazione di un ordine di trasporto.

<!-- image -->

## 3.4. Incongruenza logica tra WAMAS e Lighthouse

Può  verificarsi  la  situazione  in  cui  su  WAMAS  vedo  un  UDC  in  una  certa  locazione  che  però  su Lighthouse non viene visto. Questo causa un disallineamento dei sistemi a gestire.

Per ovviare a questo problema bisogna selezionare l'opzione 'Forza' e poi refresh e reset per forza il sistema a rilevare l'UDC e sistemare la questione.

<!-- image -->

L'immagine mostra un menu contestuale aperto su un record di trasporto con ID Udc 70805545, dove l'opzione "Forza" è evidenziata da un cerchio rosso, indicando un'azione di forzatura del processo. Il menu include funzioni come "Refresh From Database", "Replan Route", "Reset Transport Order" e "CancelRequestEMS", suggerendo un'interfaccia di gestione logistica o di trasporto. La tabella in background elenca dettagli come "Base di carico", "Location label" e "Nodo", confermando il contesto operativo di un sistema di gestione dei trasporti.

<!-- image -->