## Summary

| 1.   | Breve descrizione..................................................................................................................1     |
|------|------------------------------------------------------------------------------------------------------------------------------------------|
| 2.   | Quando................................................................................................................................1  |
| 3.   | Come...................................................................................................................................2 |
| 3.1. | Modalità automatica...................................................................................................... 2              |
| 3.2. | Modalità manuale.......................................................................................................... 2             |

3.3.

Schiavizzazione ............................................................................................................. 3

Last revision date: 13.11.2025

Author: Bortolotti Francesco

## 1. Breve descrizione

La procedura logistica per il cambio pinza delle baie di picking nasce dal fatto che a disposizione degli operatori ci sono due tipi di pinze: una per i grandi formati (in totale 5 pinze) e una più piccola per i formati  standard  (12  pinze  in  totale,  idealmente  una  per  baia). Quando  l'operatore  di  baia  ha necessità di dover cambiare la pinza, questa può avvenire in modalità automatica o manuale. La pagina WAMAS da cui si esegue il cambio è la WH083.

## 2. Quando

Il cambio pinza viene richiesto dall'operatore di baia che ha bisogno che venga utilizzata una pinza diversa da quella al momento montata per eseguire la propria mansione. Avverte il capoturno della necessità, che a sua volta avvisa la Manutenzione o l'Ufficio Tecnico che interviene per portare a termine l'attività.

<!-- image -->

## PROCEDURA CAMBIO PINZA ALLE BAIE DI PICKING

## Specifiche

## 3. Come

Le modalità per effettuare il cambio pinza sono principalmente due: automatica e manuale .

In  entrambe  le  modalità,  il  primo  step  di  ognuna  delle  due  procedure  è  sempre  e  solo  quello  di accertarsi è che la baia in oggetto sia arrestat a (vedi procedura sull'arresto di una baia).

## 3.1. Modalità automatica

La modalità automatica presuppone una precedente associazione di ogni pinza (standard) con una baia.  Come  già  detto  precedentemente,  sono  presenti  12  pinze  standard;  idealmente,  ogni  pinza sarebbe associata alla propria baia di riferimento (la pinza 1 con la baia 1, la pinza 2 con la baia 2). In questa situazione ideale, l'operatore dovrebbe semplicemente controllare che la propria pi nza di riferimento sia disponibile dentro il MAV, dopodiché dal terminale della baia è possibile chiamare l'operazione di cam bio pinza.

Così facendo, un manutentore giunge alla baia e assiste l'operatore l'operazione. Il sistema manda fuori dal MAV in maniera automatica due pallet: uno con il supporto vuoto in cui riporre la pinza da cambiare, e un altro pallet con il supporto della pinza e l'organo stesso da montare. Portata a termine l'attività di cambio pinza, a seguito di una serie di domande di conferma del sistema che vengono mostrate  a  terminale  a  cui  il  manutentore  deve  rispondere  correttamente,  i  due  pallet  vengono rimandati dentro al magazzino.

## 3.2. Modalità manuale

La situazione ideale in cui ogni pinza è associata alla propria baia di riferimento rimane, appunto, quasi impossibile da realizzare. A causa di continui problemi, è molto difficile che si riesca ad avere sempre per ogni baia una e una sola pinza associata. Infatti, se si verificano problemi in una pinza standard di una specifica baia, per ovviare al problema ne viene 'presa in prestito' una di un'altra che in quel momento ne sta usando un altro tipo.

In questo caso, quando un operatore deve chiamare il cambio pinza in modalità manuale, ci sono i seguenti step da seguire:

1. Accertarsi che la baia sia in stato di arresto
2. Da  WAMAS,  creare  gli  ordini  di  trasporto  verso  le  sorgenti  della  baia  per  i  due  pallet necessari  per  l'attività  (uno  contenente  il  supporto  vuoto  della  pinza  da  riporre  in magazzino, e l'altro con il pallet contenente la pinza da montare)
3. Eseguire fisicamente il cambio pinza con l'aiuto del manutentore
4. Gestire il fatto che togliendo dal pallet la pinza chiamata fuori dal MAV, il sistema eliminerà l'UDC perché considerata come vuota. Serve invece che l'UDC con il supporto vuoto venga stivata nel magazzino per poi essere chiamata fuori in futuro in caso di nuovo cambio pinza. L'operazione da fare per risolvere questo problema è quindi ri creare manualmente l'UDC:
- Numero di UDC
- Posto di stoccaggio: la sorgente della baia in cui si trova
- Base di carico e cubatura
- Grafo flusso merci: InHBW
- Spuntare la voce 'Riservato ad attrezzo manipolatore'

<!-- image -->

<!-- image -->

5. Creare un nuovo stock object per l'UDC sulla quale riponiamo la pinza appena smontata. Le  pinze  standard  hanno  come  nome  articolo  'CLAMP\_NOR MA L\_[#  PINZA]',  mentre  le pinze  grandi  sono  chiamate  'CLAMP\_EXTRA \_ SIZE'.  In  questo  caso  c'è  da  fare  una distinzione del pallet da usare per la creazione dei due diversi stock object:
- Per le pinze normali, il pallet da usare è l'E, con cubatura 1550.
- Per le pinze grandi, c'è bisogno di schiavizzare un pallet D su un pallet B (vedere sotto capitolo 3.3.)
6. Creare manualmente gli ordini di trasporto per rispedire i due pallet appena gestiti dentro il MAV.

Una volta gestito il cambio pinza, riattivare la baia per ricominciare a ricevere ordini.

## 3.3. Schiavizzazione

La creazione manuale del pallet delle pinze grandi formati da rimandare all'interno del MAV dopo aver effettuato un cambio pinza deve avvenire nel seguente modo:

1. Creo l'UDC primaria (il 'master') come vuoto (senza stock object) nel seguente modo:
- Posto di stoccaggio:
3. o Posto di stoccaggio: la sorgente della baia in cui si trova
4. o Magazzino: WH1
- Base di carico: solitamente il pallet master è il B
- Cubatura: 350
- Grafo flusso di merci: InHBW

IMPORTANTE: flaggare la spunta 'Riservato per attrezzo manipolatore'

2. Creo l'UDC secondaria (lo 'schiavo') come pieno (con stock object) nel seguente modo:
- Posto di stoccaggio:
3. o Posto di stoccaggio: la sorgente della baia in cui si trova
4. o Magazzino: WH1
- Base di carico: D
- Cubatura: 1550
- Grafo flusso di merci: InHBW

Stock object → 'crea record di dati'

- Versione di imballaggio articolo:
- o Numero dell'articolo: CLAMP\_EXTRA\_SIZE
- o Cliente: 1
- o Versione: 1
- Classificazione della scorta: Normal
- Proprietario della merce: 1
- •
- Tipo UDC: 001
- Quantità: 1

Per schiavizzare le UDC bisognerà aprire WAMAS Mobile Client me seguire le seguenti istruzioni:

1. Effettuare il login
2. Selezionare un muletto sopra al 200

<!-- image -->

3. Selezionare [3] Gestione delle scorte
4. Selezionare [6] Unità di carico gerarchica
5. Selezionare [1] Crea UdC gerarchica
6. Nella  casella  di  testo  per  l'unità  secondaria  inserire  lo  'schiavo'  precedentemente  creato (l'UDC con lo stock object annesso)
7. Nella casella di testo per l'unità di carico primaria inserire il 'master' precedentemente creato (l'UDC senza stock object e riservato ad attrezzo manipolatore)

Fatto ciò, avremmo creato una UDC schiavizzata e la procedura potrà essere completata.

<!-- image -->