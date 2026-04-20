## Summary

|   1. | Introduzione alla gestione dei deploy......................................................................................1           |
|------|----------------------------------------------------------------------------------------------------------------------------------------|
|    2 | Lista delle modifiche nei deploy .............................................................................................1        |
|    3 | Autorizzazione al deploy ........................................................................................................2     |
|    4 | Giorno del deploy..................................................................................................................2   |
|    5 | Fine del deploy......................................................................................................................3 |

Last revision date: 16.12.2025

Author: Bortolotti Francesco

## 1. Introduzione alla gestione dei deploy

La procedura per la gestione dei deploy mira ad essere una guida per gli step da seguire per il corretto funzionamento dei tali.

## 2. Lista delle modifiche nei deploy

Confrontarsi con i tecnici INCAS per ottenere una lista che andranno implementate nell ' incombente deploy. Per un ' ulteriore  conferma,  la  mattina  stessa  del  giorno  del  deploy,  inviare  un ' ultima mail chiedendo conferma di tutte le modifiche che dovranno essere apportate.

Ottenuta la lista, creare un nuovo file di testo nella cartella G:\Logistica\MAV\WAMAS\Deploy dove inserire le modifiche che quel determinato deploy vanno ad implementare.

L'immagine mostra una cartella di archiviazione denominata "Deploy" all'interno di una struttura di directory "Logistica > MAV > WAMAS", contenente una serie di file di testo (.txt) che documentano elenchi di deploy per ogni mese del 2025, con nomi che includono la data di creazione. Ogni file è di piccola dimensione (1-2 KB) e risale a diverse date, indicando una cronologia mensile delle attività di deploy. L'interfaccia visualizza le informazioni di nome, data di ultima modifica, tipo e dimensione dei file, con opzioni per ordinare e visualizzare i contenuti.

<!-- image -->

<!-- image -->

## PROCEDURA DEPLOY

## Procedura specifica UTL

<!-- image -->

L'immagine mostra una lista di deployment del 15 dicembre 2025, visualizzata in un editor di testo o un'applicazione di gestione documenti, con un elenco puntato di modifiche tecniche, tra cui aggiornamenti al buffer MAV1, miglioramenti all'inizializzazione MFS, un problema K97 relativo alla mancanza di dock per ordini express e l'aggiunta di nuove posizioni. Il documento è contrassegnato da un nome file e un timestamp, suggerendo un contesto operativo o di pianificazione.

<!-- image -->

## 3. Autorizzazione al deploy

Una  settimana  prima  chiedere  via  mail  a  Carlo  autorizzazione  a  procedere  con  il  deploy  in  quel determinato giorno. Sotto un esempio di mail da inviare:

Ciao Carlo, chiedo un tuo okay per fissare l'aggiornamento di WAMAS dalle ore 12:40 alle ore 13:10 di Lunedì 21/07.

Proporrei la solita organizzazione:

- @'Stefano Dall'Asta' Per quanto riguarda i turni degli operatori delle cooperative (MAV ed esterno):
- Far iniziare il turno del mattino alle ore 05:00 fino alle ore 12:30; Fa iniziare il turno del pomeriggio alle ore 13:30 fino alle ore 21:00; Il turno della notte non subisce variazioni (21:10 -04:40).
- @'Andrea Mazzoli' /@'Martina Casolari' / @Laura Spadoni Per quanto riguarda l'agenda: Tenere liberi gli slot di prenotazione del carico dalle ore 12:30 alle ore 13:30/13:45, così da non generare disservizi/ritardi durante l'aggiornamento di WAMAS. Questo per CA CT -C/L -Intergruppo.
- @Federico Campedelli Bloccare il TOTEM durante il deploy per evitare errori nella trasmissione dei record.

## 4. Giorno del deploy

Alla  mattina inviare una mail per ricordare a tutti i colleghi che in paura pranzo verrà effettuato il deploy. Di seguito un esempio:

Buongiorno a tutti, la presente per informarvi che alle 12.40 verrà eseguito un aggiornamento WAMAS.

Potete continuare a lavorare (e la stessa cosa possono fare i carrellisti) finché non verrete disconnessi in automatico dal sistema.

Non appena l'aggiornamento sarà concluso e avremo fatto i controlli necessari, sarà mia cura comunicarvi che potete riprendere a lavorare.

Grazie a tutti per la collaborazione!

<!-- image -->

All ' orario indicato per il deploy (solitamente alle 12:30), settare il parametro agvDisable da false a true. Il parametro si trova nella pagina WAMAS FW028 accessibile solo a superutenti. A questo punto, la generazione di nuove missioni verrà bloccate, gli AGV termineranno le missioni già assegnate e procederanno ad andare verso le postazioni di carica.

Una volta che tutti gli AGV sono in carica si può ai tecnici di WAMAS tramite Whatsapp che possono iniziare a fare il deploy.

## 5. Fine del deploy

Una volta che su Whatsapp ci è stato comunicato che il deploy è stato implementato con successo, bisogna controllare che tutto funzioni:

1. Dalla WH085 controllare che ci si riesca a connettere alla baie di picking e che funzionino tutte
2. Controllare che in FW028 il parametro agvDisable sia di nuovo true
3. Test delle CR successivamente (metter ok su issues ad ok)

Infine, inviare una mail per avvisare che il deploy è terminato ed è possibile tornare regolarmente a lavorare:

Aggiornamento terminato! Potete riprendere a lavorare.