## Summary

|   1. | Introduzione gestione vuoti in errore in baia ............................................................................1    |
|------|--------------------------------------------------------------------------------------------------------------------------------|
|    2 | Quando gestire i vuoti in errore in baia ....................................................................................1 |
|    3 | Quando gestire i vuoti in errore in baia ....................................................................................2 |

Last revision date: 27.11.2025

Author: Bortolotti Francesco

## 1. Introduzione assegnazione ordini di picking ad un utente

La procedura logistica per l ' assegnazione di specifici ordini ad un utente particolare è utile nel caso in cui si voglia che determinati ordini di picking con caratteristiche comuni vengono gestite in una specifica baia da uno specifico utente. È una procedura delicata, che non tutti gli utenti di WAMAS possono portare avanti. È infatti accessibile solo ai Superuser (UTL, ufficio approntamento ordini … )

## 2. Quando assegnare ordini di picking ad un utente

Questa procedura viene gestita in generale dall ' ufficio tecnico e dall ' ufficio approntamento ordini e nasce dall ' accordo comune di questi soggetti. La procedura torna utile, per esempio, in fase di test: se  si  vuole  che  determinati  ordini  che  vanno  gestiti  su  determinati  tipi  pallet,  allora  si  possono assegnare manualmente tutti gli ordini di picking che devono essere gestiti tramite uno specifico tipo pallet ad una specifica baia dove sta lavorando un determinato utente.

<!-- image -->

## PROCEDURA ASSEGNAZIONE ORDINI DI PICKING AD UN UTENTE

Procedura specifica per Superuser

## 3. Quando assegnare gli ordini di picking ad un utente

## 3.1. Assegnazione ordine ad un utente

Per assegnare un ordine di picking ad un utente, si accede alla pagina OG039 di WAMAS e si cercano tramite i filtri iniziali gli ordini di picking desiderati.

A questo punto si preme tasto destro sull ' ordine scelto e si seleziona ' Assegna utente …' :

L'immagine mostra una finestra di risultati di ricerca di un sistema gestionale, con una lista di ordini in corso o completati, ciascuno identificato da numero, destinatario e stato. È evidenziata una voce di menu contestuale che offre l'opzione "Assegna vendente", indicando la possibilità di assegnare un rappresentante commerciale all'ordine selezionato. La tabella include colonne con dettagli come data, destinatario, numero di ordine, stato, progresso e area di picking.

<!-- image -->

Si aprirà una finestra UM012 dove nella cella di testo ' Utente ' si deve inserire il codice dell ' utente a cui si vuole assegnare l ' ordine di picking selezionato. Inoltre, se si sta assegnando l ' ordine ad una baia allora si selezionare ' Desktop ' , altrimenti ' Mobile ' . Infine, premere ' Assegna ' per concludere la procedura.

L'interfaccia permette di assegnare un utente a un'applicazione mobile, con un campo per inserire il nome dell'utente e una selezione tra Desktop e Mobile (attualmente selezionato Mobile). È stato selezionato un singolo record di dati, come indicato dal messaggio in alto, e sono disponibili i pulsanti 'Assegna' e 'Annulla' per confermare o annullare l'azione.

<!-- image -->

Terminato  ciò,  nella  pagina  OG039  nella  colonna ' Addetto  al  picking ' verrà  visualizzato  l ' utente inserito.

## 3.2. Rimozione ordine ad un utente

Al contrario, se si vuole eliminare l ' assegnazione di un ordine ad un utente specifico, si esegue la stessa identica procedura fino alla compilazione della finestra UM012. In questo caso, si selezionerà

<!-- image -->

<!-- image -->

l ' opzione desiderata tra ' Desktop ' e ' Mobile ' lasciando vuota la casella di testo ' Utente ' . Premendo ' Assegna ' per ultimare la procedura, se c ' era già u utente assegnato a quell ' ordine verrà rimosso.