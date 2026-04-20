## Summary

|   1. | Introduzionecambio priorità per i pallet in uscita da MAV2 eS46..........................................   |
|------|-------------------------------------------------------------------------------------------------------------|
|    2 | Quando cambiarelepriorità dei pallet in uscita da MAV2 eS46 ...........................................     |
|    3 | Comecambiarelepriorità dei pallet in uscita da MAV2 e S46...............................................    |

Last revision date: 28.10.2025

Author: Bortolotti Francesco

## 1. Introduzione cambio priorità per i pallet in uscita da MAV2 e S46

La procedura logistica per il cambio di priorità di uscita dei pallet dal magazzino automatico verticale dei pronti MAV2 ha lo scopo di garantire una gestione dinamica e flessibile dei flussi di materiale, in funzione delle urgenze produttive e delle necessità operative.

Quando c'è  la necessità di modificare la priorità delle  unità di spedizione  UDS (pallet pronti per  la spedizione) di uscita dal MAV2 o la priorità dei trasporti dalle locazioni S46 alle locazioni S48 per le spedizioni, un  collega  dell'ufficio  tecnico accede  alla  pagina FW028  di  WAMAS  dove  modifica i parametri associati alla priorità. Questi parametri includono il numero di pallet in coda alla prima UDS sulla rulliera, prima che quest'ultim a assuma la priorità indicata nel secondo parametro su cui  si interviene.  Una volta aggiornati questi dati, il WMS  ricalcola automaticamente i valori di priorità e trasmette  agli AGV  le  nuove missioni. Il sistema esegue  poi le movimentazioni secondo la priorità aggiornata, ottimizzando i tempi di uscita e riducendo i tempi di attesa.

## 2. Quando cambiare le priorità dei pallet in uscita da MAV2  e S46

Il bisogno di modificare la priorità dei pallet in uscita dal MAV2, o degli ordini di trasporto di UDS dalle S46  alle  S48,  nasce solo  su  richiesta dell'ufficio  carico  strettamente  in  accord o con  l'ufficio approntamento  ordini  per  specifiche  esigenze  riguardanti  i  suddetti  uffici.  Non  si  verificano assolutamente altri casi in cui questo tipo di cambio di priorità viene assecondato.

<!-- image -->

## PROCEDURA CAMBIO PRIORITÀ PALLET IN USCITA MAV2 o S46

Procedura specifica  UTL

## 3. Come cambiare le priorità dei pallet in uscita da MAV2 e S46

Dopo aver descritto il quando è necessario intervenire sulle priorità dei pallet in uscita dal MAV2. Per intervenire  concretamente, bisogna andare ad agire sui seguenti 4 parametri dalla pagina FW028 su WAMAS:

- -agvPrioUpdateBlockingSide379 : indica  il  numero  di  pallet  dietro  al primo sulla  rulliera  di uscita dal MAV2 prima che il pallet con trasporto più vecchio assuma priorità.
- -agvPrioUpdateBlockingS46 : indica il numero di ordini di trasporto TPO attivi (quindi presenti su CWay) oltre al primo dopo il quale l'ordine più vecchio assume la priorità.
- -agvPrioUpdateBlockingSide379Priority : priorità del TPO su CWay associata al corrispettivo parametro. Se il valore è -1 non si ha priorità.
- -agvPrioUpdateBlockingS46Priority :  priorità  dei  TPO  su  CWay  associata  al  corrispettivo parametro. Se il valore è -1 non si ha priorità.

Gli ultimi due parametri in lista intervengono, quindi, sulla priorità del transport order  associato ai primi  due  parametri:  agvPrioUpdateBlockingSide379Priority  interviene  sulla  priorità  del  TPO  del parametro  agvPrioUpdateBlockingSide379,  mentre agvPrioUpdateBlockingS46Priority  interviene sulla priorità del TPO del parametro agvPrioUpdateBlockingS46.

<!-- image -->

Prendendo come esempio l'immagine sopra, i valori indicati possono essere cos ì spiegati: il valore 1 del parametro agvPrioUpdateBlockingS46 è quello minimo, e indica che appena viene assegnato un TPO in coda al primo attuale, a quest'ultimo viene assegnata priorità 10 (seconda riga dell'immagine, parametro agvPrioUpdateBlockingS46Priority). Per  quanto riguarda invece  i parametri specifici  del MAV2, quando in coda alla prima UDS in uscita sulla rulliera ci sono 4 pallet (agvPrioUpdateBlockingSide379), in quel momento al primo in uscita viene assegnata priorità 10 in maniera tale che un AGV venga a prendere quella UDS il prima possibile e acceleri il processo di uscita dei pallet dal MAV2.

Quando si ha bisogno di andare ad anticipare l'uscita di una UD S dal MAV2, per prima cosa intervengo sul  parametro agvPrioUpdateBlockingSide379 andando a  diminuire il  numero  di pallet  in coda  al primo in uscita in maniera tale che il pallet desiderato esca prima, e contestualmente intervengo sul parametro agvPrioUpdateBlockingSide379Priority per aumentare la priorità della del TPO associato alla UDS.

In particolare, quest'ultimo parametro può avere come valori:

- --1 , per non settare nessun valore di priorità
- -10 , per settare un valore medio di priorità
- -100 , per settare un valore alto di priorità

La stessa cosa avviene se invece di MAV2, l'UD S è stoccata nelle locazioni S46: innanzitutto si modica il valore del parametro agvPrioUpdateBlockingS46 per poi andare ad aumentare il valore di priorità del TPO associato dal parametro agvPrioUpdateBlockingS46Priority.

<!-- image -->

<!-- image -->

Una volta modificati i valori, è di vitale importanza avvisare i manutentori della modifica ai parametri per metterli a conoscenza del cambio effettuato. Altrettanto importante è di ricordarsi di ripristinare i valori ottimi dei  parametri una volta  termina ta l'urgenza che  ha fatto scaturire  la richiesta. Valori ottimi:

- -agvPrioUpdateBlockingS46 : 1
- -agvPrioUpdateBlockingS46Priority : 10
- -agvPrioUpdateBlockingSide379 : 4
- -agvPrioUpdateBlockingSide379Priority : 10

Se  non sono  gli stessi  colleghi  del  carico  ad avvisare  del  termine  della  situazione, è  importante sollecitarli per riportare i parametri alla normalità.