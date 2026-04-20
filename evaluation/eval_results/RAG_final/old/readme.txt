Valutato l'intero RAG con le tecniche di retrieve e chunking migliori in base ai benchmark precedenti
Se le informazioni a contesto non sono necessarie la risposta è sbagliata, se le informazioni sono necessarie ma il llm sbaglia la risposta è sbagliata
(Il hierarchical chunking è eseguito sempre con topk = 3 (altro lower bound) in heatmap_RAG_Performance mentre ad esaurimento dei 6k token/top10 in h_eval)
