import sqlite3
from llama_index.core.schema import TextNode
import os
import qdrant_client
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter, FilterOperator
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core import QueryBundle
import json
from pydantic import BaseModel, Field
from llama_index.core import PromptTemplate
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import itertools
from rerank import reranka
import seaborn as sns
import sys
import numpy as np
from transformers import AutoTokenizer
from dotenv import load_dotenv
import gc
load_dotenv()

VLLM_API_BASE_URL = os.getenv("VLLM_API_BASE_URL")
QDRANT_URL = os.getenv("QDRANT_URL")

#MODIFICARE

#NOMI POSSIBILI:
# docling_eval
# WAMASRAGBASE
# topk = 200 


# overlap_eval
# WAMASRAGOVERLAP
# topk = 37 

# hierarchical_eval
# WAMASHIERARCHICAL
# topk = 347


#MODIFICARE
nome_db = "hierarchical_eval"  # Nome del database
collectionname = "WAMASHIERARCHICAL"  # Nome della collezione Qdrant
topk = 347  # Numero massimo di chunk presenti in qdrant

# Mappa nome_db al tipo di chunking per il titolo del grafico
chunking_type_map = {
    "docling_eval": "Docling",
    "overlap_eval": "Overlap",
    "hierarchical_eval": "Hierarchical"
}
chunking_type = chunking_type_map.get(nome_db, "Unknown")

dense_opts = [True, False]
sparse_opts = [True,False]
hyde_opts = [False, True]

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-32B-Instruct")


# rows_dataframe_miss_retriever = []

# rows_dataframe_miss_reranker = []


client = qdrant_client.QdrantClient(url=QDRANT_URL)


embed_model = OpenAIEmbedding(
    api_base=VLLM_API_BASE_URL,
    model_name="BAAI/bge-m3",
    api_key="null",
)
Settings.embed_model = embed_model

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collectionname,
    enable_hybrid=True,
    dense_vector_name="bge_m3",
    sparse_vector_name="bm25",
    fastembed_sparse_model="Qdrant/bm25"
)


index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

risultati_benchmark = []

conn = sqlite3.connect(f"./{nome_db}.db", check_same_thread=False)
    
df = pd.read_sql_query("SELECT * FROM evaluation_table", conn)


def evaluate(dense, sparse, hyde): #qua hyde e aug sono booleani
    

    print(f"  Configurazione retriever: dense={dense}, sparse={sparse}, hyde={hyde}")

    if dense and not sparse:
        retriever = index.as_retriever(
            vector_store_query_mode=VectorStoreQueryMode.DEFAULT, 
            similarity_top_k=topk,
            filters=None
        )
        print(f"  Usando: SOLO Dense, topk={topk}")
    elif sparse and not dense:
        retriever = index.as_retriever(
            vector_store_query_mode=VectorStoreQueryMode.SPARSE,
            sparse_top_k=topk,
            filters=None
        )
        print(f"  Usando: SOLO Sparse, topk={topk}")
    else:
        # Hybrid nativo di Qdrant che è meglio di fare mode simple...
        retriever = index.as_retriever(
            vector_store_query_mode=VectorStoreQueryMode.HYBRID,
            similarity_top_k=topk,
            sparse_top_k=topk,
            filters=None
        )
        print(f"  Usando: HYBRID, topk={topk}")


    def check_chunk_in_retrieval(ground_truth_chunk_index, ground_thruth_filename, query, hd):
        hydeaug = None
        if hyde:
            try: #qua fatto un paciugo incredibile ma funziona
                doc_generato = hd
                if doc_generato:
                    hydeaug = [doc_generato] #IMPORTANTISSIMO: deve essere una lista di stringhe
                else:
                    hydeaug = None
            except Exception as e:
                print(f"Errore nella lettura di hyde per la query '{query}': {e}")
                hydeaug = None
        
        query_bundle = QueryBundle(
            query_str=query,
            custom_embedding_strs=hydeaug
            )
        nodi = retriever.retrieve(query_bundle)
        
        # DEBUG: stampa il numero di nodi recuperati per la prima query
        if idx == 0:
            print(f"  DEBUG prima query: recuperati {len(nodi)} nodi")

        #BLOCCO DI EVALUATION VERO E PROPRIO
        if "," in str(ground_truth_chunk_index):
            ground_truth_chunk_index = [fn.strip() for fn in ground_truth_chunk_index.split(",")]
            ground_truth_chunk_index = [int(idx) for idx in ground_truth_chunk_index]
        else:
            ground_truth_chunk_index = [int(ground_truth_chunk_index)]

        # Lista per memorizzare i risultati per ogni chunk
        results_per_chunk = []
        
        # Accumula chunk e calcola recall per ogni chunk aggiunto
        token_sum = 0
        retrieved_chunks = []
        
        # Pre-estrai tutti i testi per batch encoding (più efficiente)
        chunk_texts = [nodo.node.text if hasattr(nodo.node, 'text') else "" for nodo in nodi]
        
        # Batch encoding più efficiente - limita lunghezza max per evitare memory overflow
        chunk_tokens_list = [len(tokenizer.encode(text, truncation=True, max_length=8192, add_special_tokens=False)) for text in chunk_texts]
        
        for idx_nodo, nodo in enumerate(nodi):
            # Usa i token pre-calcolati
            chunk_tokens = chunk_tokens_list[idx_nodo]
            
            token_sum += chunk_tokens
            
            # Estrai metadata per il check del ground truth
            metadata = nodo.node.metadata
            if metadata:
                fname = metadata.get("origin_filename", "niente filename")
                cindex = metadata.get("chunk_index", -1)
                
                # Aggiungi alla lista dei chunk retrieved solo se è del documento corretto
                if fname == ground_thruth_filename and cindex != -1:
                    retrieved_chunks.append(int(cindex))
            
            # Calcola recall dopo ogni chunk aggiunto (anche se non del documento corretto)
            chunk_gt_trovati = set(ground_truth_chunk_index).intersection(set(retrieved_chunks))
            recall = len(chunk_gt_trovati) / len(ground_truth_chunk_index) if len(ground_truth_chunk_index) > 0 else 0
            
            results_per_chunk.append({
                'num_chunks': idx_nodo + 1,  # Usa l'indice direttamente invece di cercare
                'recall': recall,
                'tokens_cumulative': token_sum
            })
            
        return results_per_chunk



    # Labels per la configurazione
    label_hyde = "HyDE" if hyde else "Base"
    label_tipo = "Dense" if dense and not sparse else "Sparse" if sparse and not dense else "Hybrid"

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="evaluating", unit="query", dynamic_ncols=True):
        results = check_chunk_in_retrieval(
            ground_truth_chunk_index=row["chunk_index"], 
            ground_thruth_filename=row["filename"], 
            query=row["question"], 
            hd=row["hypothetical_doc"]
        )
        
        # Aggiungi ogni chunk come una riga separata nel dataframe
        for result in results:
            risultati_benchmark.append({
                'Configurazione': f"{label_tipo} + {label_hyde}",
                'Tipo': label_tipo,
                'Query': row["question"],
                'Filename': row["filename"],
                'Num_Chunks_Retrieved': result['num_chunks'],
                'Tokens_Cumulative': result['tokens_cumulative'],
                'Recall': result['recall'] * 100  # In percentuale
            })
        
        # senza questa riga il server muore
        if idx % 10 == 0:
            gc.collect()


combinazioni = list(itertools.product(dense_opts, sparse_opts, hyde_opts))

for dense_val, sparse_val, hyde_val in tqdm(combinazioni, desc="Grid Search"):
    
    if not dense_val and not sparse_val: #skippo configurazione non valida
        continue
    if sparse_val and not dense_val and hyde_val:# skippo augmentation su vettori solamente sparsi
        continue
    
    print(f"\nTest: Dense={dense_val}, Sparse={sparse_val}, HyDE={hyde_val}")
    risultato = evaluate(dense=dense_val, sparse=sparse_val, hyde=hyde_val)

#PARTE PER INSERIRE I MISS SUL DB
# cursor = conn.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS retriever_miss_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         filename TEXT,
#         chunk_index TEXT,
#         retrieved_chunks TEXT,
#         question TEXT
#     )
# """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS reranker_miss_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         filename TEXT,
#         chunk_index TEXT,
#         retrieved_chunks TEXT,
#         question TEXT
#     )
# """)

# cursor.execute("""DELETE FROM retriever_miss_table""")
# cursor.execute("""DELETE FROM reranker_miss_table""")

#ORA AGGIUNGO I DATI AL DB

# dataframe_miss_retriever = pd.DataFrame(rows_dataframe_miss_retriever)
# dataframe_miss_reranker = pd.DataFrame(rows_dataframe_miss_reranker)

# for idx, row in dataframe_miss_retriever.iterrows():
#     cursor.execute("""
#         INSERT INTO retriever_miss_table (filename, chunk_index, retrieved_chunks,question)
#         VALUES (?, ?, ?, ?)
#     """, (row['filename'], str(row['chunk_index']), str(row['retrieved_chunks']), row['question']))

# for idx, row in dataframe_miss_reranker.iterrows():
#     cursor.execute("""
#         INSERT INTO reranker_miss_table (filename, chunk_index, retrieved_chunks, question)
#         VALUES (?, ?, ?, ?)
#     """, (row['filename'], str(row['chunk_index']), str(row['retrieved_chunks']), row['question']))


# conn.commit()


conn.close()

df = pd.DataFrame(risultati_benchmark)

df.to_csv(f"risultati_embedder_{nome_db}.csv", index=False)

# Debug: stampa le configurazioni uniche presenti
print(f"\nConfigurazioni trovate nel dataframe:")
for config in sorted(df['Configurazione'].unique()):
    count = len(df[df['Configurazione'] == config])
    print(f"  - {config}: {count} righe")

# Crea il grafico Recall vs Token (asse principale)
fig, ax1 = plt.subplots(figsize=(16, 10))

# Colori e stili per le configurazioni (5 possibili)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
line_styles = ['-', '--', '-.', ':', '-']

# Calcola valore massimo token
max_token_total = int(df.groupby('Num_Chunks_Retrieved')['Tokens_Cumulative'].mean().max())

# Calcola e plotta ogni configurazione
for idx, config in enumerate(sorted(df['Configurazione'].unique())):
    df_config = df[df['Configurazione'] == config]
    
    # Raggruppa per numero di chunk e calcola media recall e media token
    df_grouped = df_config.groupby('Num_Chunks_Retrieved').agg({
        'Recall': 'mean',
        'Tokens_Cumulative': 'mean'
    }).reset_index()
    
    # Stampa info su ogni configurazione
    print(f"\nConfig: {config}")
    print(f"  - Token: {df_grouped['Tokens_Cumulative'].min():.0f}-{df_grouped['Tokens_Cumulative'].max():.0f}")
    print(f"  - Recall: {df_grouped['Recall'].min():.2f}%-{df_grouped['Recall'].max():.2f}%")
    
    recall_100 = df_grouped[df_grouped['Recall'] >= 99.9]
    if not recall_100.empty:
        print(f"  - Raggiunge 100% a {recall_100['Tokens_Cumulative'].iloc[0]:.0f} token")
    
    # PLOTTA CON TOKEN COME ASSE X PRINCIPALE
    ax1.plot(df_grouped['Tokens_Cumulative'], df_grouped['Recall'], 
            label=config, linewidth=2, 
            color=colors[idx % len(colors)], 
            linestyle=line_styles[idx % len(line_styles)], 
            alpha=0.9)

# Configurazione assi
ax1.set_xlabel('Token Cumulativi', fontsize=14, fontweight='bold')
ax1.set_ylabel('Recall (%)', fontsize=14, fontweight='bold')
ax1.set_title(f'Recall embedder - {chunking_type}', 
            fontsize=16, fontweight='bold', pad=30)
ax1.legend(title='Configurazione', fontsize=11, title_fontsize=12, 
         loc='lower right', framealpha=0.9)

ax1.grid(True, which='major', alpha=0.3, linestyle='-')
ax1.set_xlim(left=0, right=max_token_total)
ax1.set_ylim(bottom=15, top=100)
ax1.set_yticks(range(20, 101, 10))

# Tick sull'asse X - ogni 1000 token
token_ticks = list(range(0, max_token_total + 1, 1000))
ax1.set_xticks(token_ticks)
labels = ax1.get_xticklabels()
for label in labels:
    label.set_rotation(45)
    label.set_ha('right')

plt.tight_layout()

# Salva il grafico
plt.savefig(f'recall_vs_tokens_{nome_db}.png', dpi=300, bbox_inches='tight')
print(f"Grafico salvato come: recall_vs_tokens_{nome_db}.png")

plt.show()