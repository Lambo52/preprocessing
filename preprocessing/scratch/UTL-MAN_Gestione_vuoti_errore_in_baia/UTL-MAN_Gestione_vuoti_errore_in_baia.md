## Summary

|   1. | Introduzione gestione vuoti in errore in baia ............................................................................1    |
|------|--------------------------------------------------------------------------------------------------------------------------------|
|    2 | Quando gestire i vuoti in errore in baia ....................................................................................1 |
|    3 | Quando gestire i vuoti in errore in baia ....................................................................................2 |

Last revision date: 17.11.2025

Author: Bortolotti Francesco

## 1. Introduzione gestione vuoti in errore in baia

La  procedura  logistica  per  gestire  i  vuoti  in  errore  nelle  baie  di  picking  ha  lo  scopo  di  risolvere  il problema della mancata consegna dei pallet in baia.

Può capitare, infatti, che gli AGV, per qualche motivo non del tutto definito, non portino la base di carico  vuota  alla  locazione  di  destinazione  di  una  baia.  Questo  non  permette  all'operatore  di effettuare l'attività di picking data la mancanza di pallet su cui comporre il pallet in uscita.

Questa procedura viene gestita via WAMAS dalle pagine OG039 e OG525.

## 2. Quando gestire i vuoti in errore in baia

Questa procedura viene gestita su segnalazione dell'operatore che avvisa il capo turno o qualcuno della manutenzione che non gli sta arrivando il vuoto per il picking successivo. Successivamente, vengono avvisati i colleghi dell'ufficio tecnico che si occu pano dei primi tentativi (spesso funzionanti) per risolvere la questione

<!-- image -->

## PROCEDURA GESTIONE VUOTI IN ERRORE IN BAIA

## Specifiche

## 3. Quando gestire i vuoti in errore in baia

Quando viene effettuata la segnalazione del vuoto che non arriva in baia, ci si connette alla pagina OG039 di WAMAS.

Per prima cosa si seleziona come filtro di ricerca 'pStations' nella casella di testo 'Area di picking' per selezionare solo le righe di picking eseguite nelle baie, dopodiché si copia il numero dell'ordine di picking per il quale l'operatore ha segnalato la mancanza di vuoto in baia.

L'immagine mostra una schermata di un sistema di gestione logistica che elenca ordini di picking, con filtri attivi per "pStations" e "Ordine di picking" 6085664 evidenziato. Il risultato della ricerca visualizza dettagli degli ordini, tra cui il destinatario, il numero d'ordine, lo stato principale (con alcuni segnalati come "Finito"), e l'area di picking "pStations" associata. L'interfaccia include anche campi per la data e l'ora di appuntamento e una colonna per l'addetto, indicando un contesto operativo di gestione delle consegne.

<!-- image -->

Acquisito il numero d'ordine, si passa alla pagina OG525.

Qui per prima cosa si va ad inserire il numero d'ordine per cercare la riga relativa al problema. A questo punto, ci si accerta che nella colonna 'Id UdC vuota' sia vuota (nell'immagine sottostante è presente il codice temporaneo TEMP8148 solo d'esempio perché al momento della stesura di questa procedura non era presente un errore di questo tipo da poter mostrare nelle figure) e quindi in errore perché nessun pallet vuoto è stato assegnato alla baia di picking.

L'immagine mostra l'interfaccia di un sistema di gestione logistica che visualizza una richiesta di UDC vuota con ID 6085664 e un'identificazione UDC vuota TEMP8148. È evidenziata l'opzione "Invia richiesta di cancellazione al MFS..." nel menu contestuale di un record selezionato, indicando una funzione per annullare una richiesta di picking. La schermata include campi di ricerca per filtri come ordine di picking, partner, magazzino e posti di stoccaggio.

<!-- image -->

<!-- image -->

<!-- image -->

Si  clicca  il  tasto  destro  del  mouse  sulla  riga  selezionata  e  si  preme  l'opzione  'Invia  richiesta  di cancellazione al MFS…'. In questo modo la riga viene eliminata e ricalcolata automaticamente. Il più delle volte questa soluzione risolve il problema.

Nel caso in cui questa procedura non bastasse, allora bisogna passare ad 'un'investigazione' più approfondita  andando  a  verificare  che  non  ci  siano  problemi  ai  destacker  dei  pallet  vuoti,  per esempio, o qualche altra causa che può far scaturire la nascita di questo problema.