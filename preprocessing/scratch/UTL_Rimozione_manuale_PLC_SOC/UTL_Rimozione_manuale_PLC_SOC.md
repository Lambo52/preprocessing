## Summary

|   1. | Introduzione spostamento manuale dei pallet dal PLC - Gestione SOC....................................1              |
|------|----------------------------------------------------------------------------------------------------------------------|
|    2 | Quando gestire manualmente i SOCdei pallet ........................................................................1 |
|    3 | Comegestire lo spostamento manuale dei pallet dal PLC........................................................2       |

Last revision date: 04.12.2025

Author: Bortolotti Francesco

## 1. Introduzione spostamento manuale dei pallet dal PLC -Gestione SOC

La  procedura  logistica  per  lo  spostamento  manuale  dei  pallet  dalle  rulliera,  dalle  catenarie,  o comunque da qualsiasi locazione fisica collegata al PLC del sistema, serve per gestire via WAMAS questa  situazione  in  cui  il  SOC  (il  numero  del  PLC  associato  al  pallet)  deve  essere  eliminato contestualmente allo spostamento manuale del pallet dalla rulliera.

## 2. Quando gestire manualmente i SOC dei pallet

I  SOC dei pallet vanno gestiti manualmente ogni qualvolta nasca il bisogno di gestire a loro volta manualmente dei pallet.  Per  diverse  ragioni  un  pallet  si  può  bloccare  su  una  delle  rulliere,  sulle catenarie,  ecc.,  creando  disagi  al  flusso  del  magazzino.  Ci  sono  quindi  casi  in  cui  è  necessario l'intervento fisico dei manutentori che entrano in giuoco rimuovendo manualmente il materiale dal sistema con lo scopo di eliminare il blocco e ripristinare il normale flusso del magazzino. In questi casi è necessario supportare l'azione dei manutentori con la procedura via WAMAS per rimuovere anche a livello logico il pallet dal PLC.

<!-- image -->

## PROCEDURA  SPOSTAMENTO  MANUALE dei PALLET dal PLC - GESTIONE SOC

Procedura specifica UTL

## 3. Come gestire lo spostamento manuale dei pallet dal PLC

A livello pratico, una volta che i manutentori hanno confermato lo spostamento manuale di una certa unità di carico dal sistema, si seguono i seguenti passi:

- -Si accede alla pagina SM023 di WAMAS
- -Si ricerca il codice dell'UDC del pallet rimosso
- -Tasto destro → 'Modifica…'
- -Eliminare l'UDC selezionata tramite l'icona in alto a destra con la 'X' rossa
- -Premere 'Salva' in basso a destra della finestra per confermare l'eliminazione
- -Dopodiché, connettersi alla pagina MF266 di WAMAS
- -Nel filtro 'Servizio MFS' si inserisce ' mfsPal '
- -Nella ricerca avanzata inserire il codice dell'UDC eliminato
- -Tasto destro → 'Annulla la richiesta'

L'immagine mostra la schermata di modifica di un'unità di carico (UDC) nel sistema SAP, con dati specifici come il posto di stoccaggio (W01), le dimensioni e il peso lordo, e opzioni per la gestione del movimento e dell'inventario. Sono visibili campi per l'orientamento UDC, il volume merci, e impostazioni di stampa come etichette di spedizione e distinta dei colli. In basso, i pulsanti 'Aggiorna', 'Salva' e 'Ripristina' indicano le azioni principali disponibili per salvare o annullare le modifiche effettuate.

<!-- image -->

L'immagine mostra una schermata di un sistema di gestione delle richieste di ordine PCS (MF266), con un elenco di ordini in corso, ciascuno identificato da un Device Controller, un ID SOC e uno stato. È evidenziata una riga con ID SOC 8888888, sul cui pulsante è attivato il menu contestuale "Consulta la richiesta" e "Cancel SOC Order". La schermata include campi di ricerca avanzata e colonne che mostrano lo stato, la posizione corrente e le destinazioni degli ordini.

<!-- image -->

A questo punto, il SOC sarà stato disassociato dall'UDC e il sistema è stato gestito correttamente.

<!-- image -->