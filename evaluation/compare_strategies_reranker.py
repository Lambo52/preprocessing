import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carica i CSV dei reranker
df_docling = pd.read_csv("risultati_reranker_docling_eval.csv")
df_hierarchical = pd.read_csv("risultati_reranker_hierarchical_eval.csv")
df_overlap = pd.read_csv("risultati_reranker_overlap_eval.csv")

# Raggruppa per numero di chunk e calcola media recall e media token
docling_grouped = df_docling.groupby('Num_Chunks_Retrieved').agg({
    'Recall': 'mean',
    'Tokens_Cumulative': 'mean'
}).reset_index()

hierarchical_grouped = df_hierarchical.groupby('Num_Chunks_Retrieved').agg({
    'Recall': 'mean',
    'Tokens_Cumulative': 'mean'
}).reset_index()

overlap_grouped = df_overlap.groupby('Num_Chunks_Retrieved').agg({
    'Recall': 'mean',
    'Tokens_Cumulative': 'mean'
}).reset_index()

# Crea il grafico
fig, ax = plt.subplots(figsize=(16, 10))

# Plotta le tre strategie dopo reranking
ax.plot(docling_grouped['Tokens_Cumulative'], docling_grouped['Recall'], 
        label='Docling + Rerank', linewidth=2, 
        color='#1f77b4', linestyle='-', alpha=0.9)

ax.plot(hierarchical_grouped['Tokens_Cumulative'], hierarchical_grouped['Recall'], 
        label='Hierarchical + Rerank', linewidth=2, 
        color='#ff7f0e', linestyle='--', alpha=0.9)

ax.plot(overlap_grouped['Tokens_Cumulative'], overlap_grouped['Recall'], 
        label='Overlap + Rerank', linewidth=2, 
        color='#2ca02c', linestyle='-.', alpha=0.9)

# Calcola valore massimo per i limiti degli assi
all_tokens = pd.concat([docling_grouped['Tokens_Cumulative'], 
                        hierarchical_grouped['Tokens_Cumulative'], 
                        overlap_grouped['Tokens_Cumulative']])
max_token_total = int(all_tokens.max())

# Imposta etichette e titolo
ax.set_xlabel('Token Cumulativi', fontsize=14, fontweight='bold')
ax.set_ylabel('Recall (%)', fontsize=14, fontweight='bold')
ax.set_title('Confronto Strategie di Chunking - Reranker', 
            fontsize=16, fontweight='bold', pad=30)
ax.legend(fontsize=11, loc='lower right', framealpha=0.9)

# Griglia
ax.grid(True, which='major', alpha=0.3, linestyle='-')

# Limiti degli assi
ax.set_xlim(left=0, right=max_token_total)
ax.set_ylim(bottom=15, top=100)

# Tick degli assi
ax.set_yticks(range(20, 101, 10))
x_ticks = list(range(0, max_token_total + 1, 1000))
ax.set_xticks(x_ticks)

# Ruota tutte le etichette in obliquo
labels = ax.get_xticklabels()
for label in labels:
    label.set_rotation(45)
    label.set_ha('right')

plt.tight_layout()

# Salva il grafico
plt.savefig('confronto_strategie_chunking_reranker.png', dpi=300, bbox_inches='tight')
print(f"Grafico salvato come: confronto_strategie_chunking_reranker.png")

# Stampa statistiche
print(f"\nStatistiche per strategia (con Reranking):")
print(f"\nDocling + Rerank:")
print(f"  - Recall finale: {docling_grouped['Recall'].iloc[-1]:.2f}%")
recall_100_doc = docling_grouped[docling_grouped['Recall'] >= 99.9]
if not recall_100_doc.empty:
    print(f"  - Token per 100%: {int(recall_100_doc['Tokens_Cumulative'].iloc[0])}")
else:
    print(f"  - Token per 100%: Non raggiunto")

print(f"\nHierarchical + Rerank:")
print(f"  - Recall finale: {hierarchical_grouped['Recall'].iloc[-1]:.2f}%")
recall_100_hier = hierarchical_grouped[hierarchical_grouped['Recall'] >= 99.9]
if not recall_100_hier.empty:
    print(f"  - Token per 100%: {int(recall_100_hier['Tokens_Cumulative'].iloc[0])}")
else:
    print(f"  - Token per 100%: Non raggiunto")

print(f"\nOverlap + Rerank:")
print(f"  - Recall finale: {overlap_grouped['Recall'].iloc[-1]:.2f}%")
recall_100_over = overlap_grouped[overlap_grouped['Recall'] >= 99.9]
if not recall_100_over.empty:
    print(f"  - Token per 100%: {int(recall_100_over['Tokens_Cumulative'].iloc[0])}")
else:
    print(f"  - Token per 100%: Non raggiunto")

plt.show()
