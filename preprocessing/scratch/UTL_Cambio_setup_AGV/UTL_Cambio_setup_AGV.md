## Summary

|   1. | Introduzione cambio setup degli AGV.....................................................................................1   |
|------|-----------------------------------------------------------------------------------------------------------------------------|
|    2 | Quando cambiare il setup degli AGV.......................................................................................1  |
|    3 | Comecambiare il setup degli AGV..........................................................................................1  |

Last revision date: 26.11.2025

Author: Bortolotti Francesco

## 1. Introduzione cambio setup degli AGV

La procedura logistica per modificare il setup degli AGV serve per cambiare le modalità secondo le quali i due diversi tipi di AGV compiono le missioni. Preferendo una modalità rispetto ad un'altra, utilizzerà in maniera diversa i robot a disposizione del magazzino, ottimizzando i percorsi di un tipo piuttosto che dell'altro, o ottimizzando la ricarica di un tipo piuttosto che dell'altro. I setup disponibili sono il setup as-is, il setup 1 e il setup 2. È una procedura di cui se ne può far carico solo l'ufficio tecnico logistico.

## 2. Quando cambiare il setup degli AGV

Il  bisogno  di  modificare  il  setup  degli  AGV,  nasce da  un  insieme  di  esigenze  generali  tra  l'ufficio tecnico, l'ufficio approntamento e la manutenzione .  Normalmente, il setup impostato è il2, che è stato ideato per servire meglio le uscite, e quindi i clienti. Possono sorgere situazioni, però, in cui ci sia necessità di utilizzare un altro settaggio degli AGV per ottimizzare meglio la ricarica dei tali (es: durante i turni notturni dove le uscite non devono essere servite in maniera ottimizzate).

## 3. Come cambiare il setup degli AGV

Concretamente, per cambiare il setup degli AGV bisogna seguire i seguenti step:

- -Avere accesso tramite VNC alla control room della manutenzione
- -Accedere a CWAY
- -Selezionare in alto la voce 'Ordine', successivamente 'Inizia ordine'

<!-- image -->

## PROCEDURA CAMBIO SETUP degli AGV

## Procedura specifica UTL

<!-- image -->

L'interfaccia di controllo CWay 2.2.1 visualizza uno schema di impianto industriale, probabilmente un sistema di trasporto o logistica, con numerose stazioni e percorsi contrassegnati da colori (verde, rosso, giallo) e numeri identificativi. È aperto il menu "manutenzione" sotto la voce "Ordine", con l'opzione "Inizia ordine" selezionata, indicando un'azione di avvio di un processo di manutenzione o gestione. La mappa mostra anche elementi come "Atlas Concorde" e "SetUp 2", suggerendo un contesto di gestione di un'infrastruttura specifica, con un'area di controllo in basso che elenca i vari punti di interesse o stati operativi.

<!-- image -->

- -Nella  finestra  che  si  apre,  selezionare  dalla  tendina  'Struttura  trasporto',  l'opzione  'Split activities ART vs ATX'

L'interfaccia 'Inizia ordine' permette di selezionare la struttura di trasporto, con 'Split activities ART vs A' evidenziata come opzione attuale. Sotto, sono presenti campi per parametri locali 'Fetch' e 'Deliver', attualmente vuoti, e pulsanti 'Avvio', 'Chiudi', e 'Guida' per gestire l'ordine.

<!-- image -->

<!-- image -->

- -Nella  sezione  'AGV  Mission  Mode  Selection',  selezionare  il  setup  che  si  vuole  impostare , inserire il Security Code e premere 'Avvio'.

L'interfaccia "Inizia ordine" permette di selezionare la struttura di trasporto "Split activities ART vs ATX" e di configurare parametri locali, tra cui la priorità e il codice di sicurezza. L'opzione "AGV Mission Mode Selection" mostra un menu a discesa con tre modalità di missione: "1_SetUp as is (Normal)", "2_SetUp 1" e "3_SetUp 2", con la terza selezionata. I pulsanti "Avvio", "Chiudi" e "Guida" sono disponibili per eseguire, chiudere o ottenere assistenza sull'ordine.

<!-- image -->

A questo la punto la procedura è terminata, il setup è stato impostato ed è possibile verificarlo nella schermata principale di CWAY; infatti, verrà visualizzato in alto a sinistra il nome del setup impostato attualmente.

L'immagine mostra una schermata del software CWay 2.2.1, che visualizza un diagramma di controllo per un sistema di gestione della sicurezza o di automazione, identificato come "3537SSI - Atlas Concorde". Sono evidenziati lo stato "Selected ACV Mode" e "Setup 2", indicando il contesto operativo corrente. Il diagramma presenta una griglia di componenti (probabilmente sensori o attuatori) con indicatori colorati (verdi, rossi, gialli) che mostrano lo stato di ogni elemento, con alcune aree segnalate da frecce o simboli di allarme.

<!-- image -->