## Summary

|   1. | Introduzioneprocedura per la gestione dei pallet vuoti nelMAV ...........................................         |
|------|-------------------------------------------------------------------------------------------------------------------|
|    2 | Quando ènecessario gestire pallet vuoti nelMAV ..............................................................     |
|    3 | Comesi gestiscono i pallet vuoti nel MAV......................................................................... |

Last revision date: 12.11.2025

Author: Bortolotti Francesco

## 1. Introduzione procedura per la gestione dei pallet vuoti nel MAV

La procedura logistica per la gestione dei pallet vuoti all'interno del MAV si basa su alcuni parametri settati nella pagina FW028 (accessibile solo a ' Superuser '  WAMAS ). In particolare, il valore di questi parametri viene variato in base al bisogno dell'ufficio approntamento ordini per consentire il corretto funzionamento del flusso dei vuoti.

È importante specificare che questa procedura gestisce solo il flusso automatico dei pallet vuoti che si generano durante l'attività di picking, e non quelli inseriti all'interno del MAV in modalità manuale.

Inoltre, ulteriore  disclaimer, i pallet di tipo Z e E non sono presenti  tra i parametri che vedremo nei prossimi capitoli perché  sono pallet  che  non vengono mai gestiti al picking. Al  massimo possono essere inseriti nel MAV1 manualmente e una volta svuotati escono subito dall'anello

## 2. Quando è necessario gestire pallet vuoti nel MAV

Il bisogno di intervenire  sui parametri che gestiscono le quantità di pallet vuoti che possono essere stoccati dentro il MAV, può nascere da diversi fattori. Uno su tutti, potrebbe essere dato dal fatto che nel weekend non è presente  il carrellista che si occupa di svuotare la rulliera  del Controllo Qualità (CQ) in uscita dal MAV. In questa uscita vengono mandate pile di pallet vuoti quando la capienza del magazzino relativa a quello specifico tipo pallet ha raggiunto la soglia settata nei parametri.

```
49 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeAF -1 Numeroi...MFS Optimum number of stacks of emptypallets A. 50 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeB 28 Numeroi...MFS Numero ottimodipile dipalletvuotiB S 51 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeD -1 Numero i...MFS Numero ottimo di pile di pallet vuoti D S 52 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeF 30 Numero i...MFS Numero ottimodipiledipalletvuoti F S 53 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeH -1 Numero i...MFS Numero ottimodipiledipalletvuotiH S 54 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeU -1 Numero i...MFS Numeroottimodipile dipallet vuotiU S 55 com.wamas.mfs.core.common.OptimumEmptyPalletStackTypeX -1 Numeroi...MFS Numero ottimo dipile di pallet vuotiX .S. 56 com.wamas.mfs.core.common.OptimumEmptyPalletTypeD 35 Numero i...MFS Numero ottimo dipallet vuotiD .Seilval 57 com.wamas.mfs. .Core.common.OptimumEmptyPalletTypeH 40 Numeroi...MFS Numero ottimodipallet vuoti H Se ilval 58 com.wamas.mfs.core.common.OptimumEmptyPalletTypeU 50 Numero i...MFS Numero ottimo di pallet vuoti U.Se il val. 59 com.wamas.mfs.core.common.OptimumEmptyPalletTypeX 60 Numero i...MFS NumeroottimodipalletvuotiX.Seilval..
```

<!-- image -->

## PROCEDURA GESTIONE PALLET VUOTI

## Procedura specifica  UTL

<!-- image -->

I parametri '*OptimumEmptyPalletStackType*' indica no il numero massimo di pile di uno specifico tipo pallet che possono stare dentro  al MAV; i parametri '*OptimumEmptyPalletType*'  indica no il numero massimo di pallet vuoti di uno specifico tipo che possono stare dentro al MAV. Se il valore è pari a -1, la funzione non è attiva.

Per  evitare  che  troppe  pile  di  pallet  vuoti  escano  dal CQ  il  sabato,  intasando la  rulliera  data  la mancanza di  qualcuno  addetto  a  svuotarla,  i  parametri  vengono  modificati  e  settati  con  valori esageratamente alti, non raggiungibili in una singola giornata di picking (a maggior ragione perché si tratta del sabato, giorno nel quale spesso viene svolta mezza giornata o in cui comunque i volumi sono più bassi della media).

## 3. Come si gestiscono i pallet vuoti nel MAV

Per  intervenire  sui  parametri  da  incrementare  nel  weekend  per  la  gestione  dei  vuoti,  bisogna, innanzitutto, accedere  alla pagina FW028 di WAMAS. Nella barra di ricerca  della pagina ricercare  i parametri  sopracitati  ( '*OptimumEmptyPalletStackType*' e '*OptimumEmptyPalletType*' ). In questa pagina sono presenti  tutti i parametri di gestione del sistema fino ad ora creati: per questo motivo non è accessibile a tutti gli utenti.

A questo punto modificare i valori dei due parametri (es: 200). In questo modo, la quantità di pile o di pallet singoli all'interno del MAV non raggiungerà mai il limite settato da questi parametri e, quindi, nessun tipo pallet verrà fatto uscire dal CQ, ma verranno mandate tutte all'interno del magazzino.

Importante: non cambiare assolutamente i valori delle pile già impostati a -1. Le pile dei tipi pallet con questo valore non vengono gestiti in maniera automatica dal sistema perciò non vanno considerati in questa procedura.

Importante accortezza è ricordarsi, al rientro a lavoro dopo il weekend, di ripristinare i valori originali dei parametri modificati. Infatti, troppi pallet vuoti all'interno del MAV creano due problemi principali:

1. Occupano tanto spazio inutilmente
2. Aumentano il carico d'incendio

Una volta settati i valori  normali dei vuoti la procedura è terminata e il sistema piano piano tornerà alla sua condizione ottimale nel rispetto dei valori dei parametri settati.

## Valori ottimi da reimpostare:

- -OptimumEmptyPalletStackTypeAF: -1
- -OptimumEmptyPalletStackTypeB: 28
- -OptimumEmptyPalletStackTypeD: -1
- -OptimumEmptyPalletStackTypeF: 30
- -OptimumEmptyPalletStackTypeH: -1
- -OptimumEmptyPalletStackTypeU: -1
- -OptimumEmptyPalletStackTypeX: -1
- -OptimumEmptyPalletTypeD: 35
- -OptimumEmptyPalletTypeH: 40
- -OptimumEmptyPalletTypeU: 50
- -OptimumEmptyPalletTypeX: 60