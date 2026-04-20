<!-- image -->

## PROCEDURA CREAZIONE, MODIFICA ED ELIMINAZIONE TERMINALE BAIE

Procedura specifica UTL e Manutenzione

## Summary

| 1.   | Introduzione procedura per la creazione, modifica, eliminazione di terminali dalle baie.............1                         |
|------|-------------------------------------------------------------------------------------------------------------------------------|
| 2.   | Quando si creano, modificano, eliminano terminali dalle baie .................................................1               |
| 3.   | Comesi creano, modificano, eliminano terminali dalle baie ....................................................2               |
| 3.1. | Creazione nuovo terminale............................................................................................. 2      |
| 3.2. | Modifica terminale......................................................................................................... 3 |
| 3.3. | Eliminazione terminale già esistente ............................................................................... 4        |

Last revision date: 11.11.2025

Author: Bortolotti Francesco

## 1. Introduzione procedura per la creazione, modifica, eliminazione di terminali dalle baie

La procedura logistica per la modifica del terminale delle baie di picking ha lo scopo di permettere la creazione di un nuovo terminale che si potrà collegare alla baia, di modificare il terminale principale di una baia scegliendolo da una lista già esistente, o di eliminare un terminale dall'elenco di quelli che potevano connettersi alla baia.

Per operare queste funzioni ci si dovrà connettere alla pagina WH083 di WAMAS.

## 2. Quando si creano, modificano, eliminano terminali dalle baie

I casi in cui si rendono necessarie le operazioni di creazione, modifica o eliminazione di un terminale da una baia di picking sono i più disparati. Di seguito alcuni:

- -CREAZIONE:  un  nuovo  utente  (magari  un  nuovo  assunto  o  un  collega  che  ha  cambiato computer)  ha  necessità  di  connettersi  alle  baie  per  verificare  e  intervenire  in  caso  di malfunzionamenti o in caso di test.
- -MODIFICA: per esempio, in fase di deploy capita che qualche collega dagli uffici abbia bisogno di connettersi alle baie per controllare e confermare che dopo l'aggiornamento del sistema tutto stia funzionando e non ci siano problemi.
- -ELIMINAZIONE: banalamente, se si ha la completa certezza che un terminale non avrà mai più bisogno di connettersi alle baie di picking, si può eliminare dall'elenco.

## 3. Come si creano, modificano, eliminano terminali dalle baie

Prima di eseguire qualsiasi delle operazioni indicate sotto, bisogna assicurarsi che la baia sia in stato di ARRESTO (vedi procedura sull'arresto di una baia).

Una volta arrestata la baia, sarà possibile eseguire l'operazione desiderata di creazione, modifica o eliminazione di un terminale.

## 3.1. Creazione nuovo terminale

Per  creare  un  nuovo  terminale  accedere  alla  pagina  WH083  di  WAMAS,  cercare  senza  filtri  per mostrare tutte le baie , cliccare il tasto destro del mouse sulla baia desiderata e premere 'modifica':

L'immagine mostra un elenco di bai di picking in un sistema di gestione logistica, con righe numerate e colonne che indicano lo stato, il nome della baia, il tipo di indirizzo e di postazione, e i processi correnti e successivi. È stato selezionato il record HBW03, attivando un menu contestuale con opzioni come "Modifica..." (Ctrl+E), "Attiva processo", "Blocca postazione di lavoro", e "Riferimenti". Il menu suggerisce interazioni dirette con il sistema per modificare o controllare lo stato operativo della baia selezionata.

<!-- image -->

Si  aprirà  la  pagina  WH084  con  la  lista  di  terminali  associati  alla  baia.  Posizionarsi  sulla  vista 'Terminale' e c liccare tasto destro in uno spazio vuoto per selezionare l'opzione 'Crea record di dati':

L'immagine mostra l'interfaccia di gestione delle postazioni di lavoro WH084, in modalità sola lettura, con la postazione WH1 selezionata. È visualizzata una tabella che elenca sette terminali associati, ognuno con uno stato di rilevamento (3.907, 6.027, ecc.) e un indicatore di terminale principale, con il terminale 6.027 contrassegnato come principale. Un menu contestuale aperto offre opzioni per creare, eliminare record o visualizzare modifiche e cronologia dei dati.

<!-- image -->

<!-- image -->

<!-- image -->

Nella finestra che si aprirà, inserire il numero di terminale indicato tra le parentesi in fondo alla riga 'Terminale' (non  il  nome)  che  si  vuole  associare  e  indicare  se  si  sta  associando  un  terminale principale o meno. Il numero del terminale lo si trova nella finestra 'Preferenze utente' cliccando sull'icona del mondo con la rotella delle impostazioni, a fianco della barra di ricerca delle pagine WAMAS.

L'immagine mostra la finestra delle "Preferenze utente" di un sistema gestionale, dove è visualizzato il profilo dell'utente Francesco Bortolotti con ruolo "Superuser" e terminale "COSPLP30.atlasad.gruppoconcorde.it (11807)". In background, è aperta la schermata "Gestisci postazione di lavoro" con una lista di postazioni di lavoro e il campo di ricerca "Cerca nel risultato". La finestra delle preferenze include anche campi per preimpostazioni di cliente e magazzino, con un pulsante "Salva come predefinito" per memorizzare le scelte.

<!-- image -->

## 3.2. Modifica terminale

Per  modificare  il  terminale  principale  e  'prendere  il  comando'  di  una  baia  da  remoto,  basta selezionare la spunta nella colonna 'Terminale principale' nella lista dei computer già esistenti.

Per fare ciò, cliccare su una delle baie e aprire la vista 'Dettagli' in basso. Infine cambiare la spunta.

L'immagine mostra una schermata di un sistema di gestione logistica che elenca bai di picking (HBW01-HBW11) con i loro stati, tipi di attrezzo e processi correnti, evidenziando HBW03. In basso, una sezione "Dettagli" visualizza i terminali di lavoro (es. 3.907, 6.027) con il nome del terminale e un campo "Terminale principale" che indica il terminale attivo (6.027, DESKTOP-AAEDIH1) con una spunta verde. L'interfaccia include una barra di ricerca e filtri per navigare i dati.

<!-- image -->

## 3.3. Eliminazione terminale già esistente

Per eliminare un terminale associato ad una baia, cliccare 'Modifica' sulla baia desiderata, poi nella vista 'Terminale' della pagina WH084 automaticamente aperta premere tasto destro sul terminale che si vuole cancellare e selezionare 'Elimina record di dati'.

L'immagine mostra l'interfaccia del modulo WH084 per la gestione delle postazioni di lavoro in modalità sola lettura, con la postazione WH1 e il terminale HBW03 selezionati. È evidenziata la riga 4 della tabella dei terminali, dove è attivo il menu contestuale che permette di creare, eliminare record o visualizzare modifiche e cronologia. Il terminale 6.027 è contrassegnato come terminale principale, mentre il terminale 7.647 è selezionato ma non è principale.

<!-- image -->

## 4. Caso particolare: sostituire un PC in baia di picking/area automatica

1. Inserire il corretto IP ADDRESS nel nuovo pc della baia interessata. Gli indirizzi IP si trovano nel file excel 20250516\_018031H\_AtlasConcorde\_NetworkAddresses-V2.28 al percorso G:\Logistica\MAV\AtlasConcorde\_NetworkAddresses .
2. Esempio baia 1 (controllare gateway predefinito, server DNS preferito e server DNS alternativo dalla baia vicina):

L'immagine mostra l'interfaccia di configurazione di rete di un sistema operativo, con l'opzione "Utilizza il seguente indirizzo IP" selezionata, assegnando l'indirizzo 10.32.0.31, la subnet mask 255.255.254.0 e il gateway predefinito 0.0.0.0. Inoltre, è selezionata l'opzione per utilizzare server DNS specificati, entrambi impostati su 0.0.0.0, indicando che non sono configurati. La casella per "Convalida impostazioni all'uscita" è disattivata, e c'è un pulsante "Avanzate..." per ulteriori opzioni.

<!-- image -->

<!-- image -->

<!-- image -->

2. Installare WAMAS seguendo la procedura presente nel file Procedura installazione WAMAS (percorso G:\Logistica\MAV\Utilities )
3. Una volta installato WAMAS, controllare il nuovo nome del terminale. Il numero del terminale lo si trova nella finestra 'Preferenze utente' cliccando sull'icona del mondo con la rotella delle impostazioni, a fianco della barra di ricerca delle pagine WAMAS.
4. Accedere a WH083, ricercare senza filtri, cliccare sul nome della baia di picking che interessa, vista ' Dettagli ' , pagina ' Terminale ' per visualizzare i nomi dei terminali che possono accedere alla baia di picking
5. A questo punto bisogna modificare/aggiungere il nuovo nome del terminale. Procedere a fare click destro sul nome della baia interessata (ad esempio HBW01) e cliccare su modifica:

L'immagine mostra le preferenze utente di un sistema gestionale, con l'utente Francesco Bortolotti (login fbortolotti1) identificato come Superuser con profilo regionale italiano. È evidenziato il terminale di connessione COSPPL30.atlasad.gruppoconcorde.it (11807), indicando il punto di accesso attivo. La finestra permette di impostare predefinizioni per cliente e magazzino, con un pulsante per salvare le impostazioni come predefinite.

<!-- image -->

L'interfaccia visualizza una panoramica delle posizioni di lavoro, con un elenco di record che include ID, terminali, utenti attivi e stato dei dati. Un menu contestuale aperto permette di modificare o disconnettere una posizione di lavoro selezionata. In basso, una sezione "Dettagli" mostra informazioni aggiuntive come lo stato, il terminale e l'ultimo utente per ciascuna posizione.

<!-- image -->

<!-- image -->

6. Si aprirà la pagina di dialogo WH084 &gt; Terminale &gt; tasto destro &gt; crea record di dati. Si creerà una nuova riga dove indicare il nuovo numero di terminale e se è da considerarsi terminale principale o no:
7. Se alla baia di picking è associata una stampante, bisogna modificare il nome del terminale collegato  alla  stampante.  La  pagina  di  dialogo  di  riferimento  è  RM017.  Selezionare  la stampante interessata, doppio click sul numero del terminale e procedere ad inserire quello corretto &gt; ' Salva ' .
8. Se dovesse venire fuori un messaggio di errore quando si salva, andare in MD022 e cercare in terminale il numero che vorreste inserire. I nserire il valore nel 'sito di magazzino predefinito':

L'immagine mostra l'interfaccia del modulo "Gestisci postazione di lavoro" in modalità lettura, con una lista di postazioni di lavoro elencate in una tabella. Un menu contestuale è aperto su una riga selezionata (postazione 5.1.647), mostrando le opzioni "Crea record di dati", "Elimina record di dati", "Visualizza modifiche..." e "Visualizza cronologia...". In basso sono presenti i pulsanti "Aggiorna", "Salva", "Ripristina" e "Altro...".

<!-- image -->

L'immagine mostra una schermata di gestione delle assegnazioni dei posti di stampante in un sistema di magazzino, con una tabella che elenca vari posti di stoccaggio, terminali e stampanti associati, ognuno con un numero progressivo e uno stato di verifica. È evidente un'interfaccia di tipo ERP o WMS, con colonne che indicano il magazzino, le aree di gestione (trasporto, picking, uscita merci), il gruppo di compartimenti e i dispositivi di stampa. In basso a destra è presente un pulsante 'Aggiorna' e un campo di ricerca 'Cerca nel risultato', indicando che l'utente può filtrare o aggiornare i dati visualizzati.

<!-- image -->

<!-- image -->

L'immagine mostra l'interfaccia di gestione dei terminali di un sistema, con una lista di dispositivi desktop e il dettaglio di un terminale selezionato (ID 11647). In basso, un campo etichettato "Sito di magazzino predefinito" è evidenziato da un cerchio rosso, indicando una possibile azione o un punto di interesse per l'utente. La schermata include filtri, campi di ricerca e pulsanti per cercare, cancellare campi o esportare dati.

<!-- image -->

9. Reinserire il numero di terminale in RM017 e salvare
10. La baia dovrebbe funzionare correttamente.