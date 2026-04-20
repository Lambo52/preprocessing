

# QUA INVECE VIENE FATTA ANDARE PIPELINE DI RAG NORMALE, POI PRENDENDO DA EVALUATION_TABLE LE DOMANDE, MI CALCOLO IL GROUND TRUTH A PARTIRE DAI CHUNK_INDEX, POI PASSO A GEMINI DOMANDA, RISPOSTA E GROUND TRUTH PER AVERNE LA VALUTAZIONE, PER I METODI IN CUI C'è AUGMENTATION LA PRENDO DALLA TABELLA EVALUATION_TABLE

import os
import qdrant_client
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter, FilterOperator
from rerank import reranka
from pydantic import BaseModel, Field
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import PromptTemplate, Settings
from llama_index.core import QueryBundle
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted, DeadlineExceeded, InternalServerError
except Exception:
    ServiceUnavailable = ResourceExhausted = DeadlineExceeded = InternalServerError = Exception
import time, random, sys, gc
from transformers import AutoTokenizer


load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

VLLM_API_BASE_URL = os.getenv("VLLM_API_BASE_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
client = qdrant_client.QdrantClient(url=QDRANT_URL)

print(f"[INIT] SCRIPT_DIR: {SCRIPT_DIR}")
print(f"[INIT] PROJECT_ROOT: {PROJECT_ROOT}")
print(f"[INIT] VLLM_API_BASE_URL: {VLLM_API_BASE_URL}")
print(f"[INIT] QDRANT_URL: {QDRANT_URL}")

# ============================================================================
# CONFIGURAZIONE EVALUATION
# ============================================================================

# Tecniche di chunking da valutare
#docling
#overlap
#hierarchical
TECNICA_CHUNKING = "hierarchical"

# GRID SEARCH CONFIGURATION
TOPK_VALUES = [14, 52, 90]# DOCLING -> 10, 30, 50; HIERARCHICAL -> 14, 52, 90; OVERLAP -> 3, 8, 17;
TARGET_TOKENS_VALUES = [1024, 4096, 6144]


# Crea la grid search combinando tutti i valori
TOP_K_CONFIG = {}
config_id = 0
for topk in TOPK_VALUES:
    for target_tokens in TARGET_TOKENS_VALUES:
        if topk == TOPK_VALUES[0] and target_tokens == TARGET_TOKENS_VALUES[2]:
            continue
        TOP_K_CONFIG[config_id] = {"topk": topk, "target_tokens": target_tokens}
        config_id += 1

TECNICA_RETRIEVE = None
if TECNICA_CHUNKING == "docling":
    TECNICA_RETRIEVE = "Dense + HyDE"
elif TECNICA_CHUNKING == "hierarchical":
    TECNICA_RETRIEVE = "Dense + Base"
elif TECNICA_CHUNKING == "overlap":
    TECNICA_RETRIEVE = "Hybrid + Base"

print(f"[CONFIG] Tecnica chunking: {TECNICA_CHUNKING}")
print(f"[CONFIG] Tecnica retrieve: {TECNICA_RETRIEVE}")
print(f"[CONFIG] TOP_K_CONFIG: {TOP_K_CONFIG}")

collectionname = ""
db_history = ""
db_eval = ""
    
if TECNICA_CHUNKING == "docling":
    collectionname = "WAMASRAGBASE"
    db_history = "WAMASRAGBASE.db"
    db_eval = "docling_eval.db"
elif TECNICA_CHUNKING == "hierarchical":
    collectionname = "WAMASHIERARCHICAL"
    db_history = "WAMASHIERARCHICAL.db"
    db_eval = "hierarchical_eval.db"
elif TECNICA_CHUNKING == "overlap":
    collectionname = "WAMASRAGOVERLAP"
    db_history = "WAMASRAGOVERLAP.db"
    db_eval = "overlap_eval.db"




# Numero di worker paralleli per il processing
MAX_WORKERS = 4

print(f"[CONFIG] Collection: {collectionname}")
print(f"[CONFIG] DB history: {db_history}")
print(f"[CONFIG] DB eval: {db_eval}")
print(f"[CONFIG] MAX_WORKERS: {MAX_WORKERS}")

# ============================================================================

print("[INIT] Caricamento embed_model...")
embed_model = OpenAIEmbedding(
    api_base=VLLM_API_BASE_URL,
    model_name="BAAI/bge-m3",
    api_key="null",
)
Settings.embed_model = embed_model
print("[INIT] embed_model caricato.")

print("[INIT] Caricamento LLM (Qwen)...")
llm = OpenAILike(
    model='Qwen/Qwen3-32B-AWQ',
    api_base=VLLM_API_BASE_URL, 
    api_key="null",
    is_chat_model=True,
    is_function_calling_model=True,    
    timeout=60.0,
    streaming=False,
    context_window=8192,
    temperature=0,
    max_tokens=1024
)
print("[INIT] LLM (Qwen) caricato.")

print("[INIT] Caricamento LLM giudice (Gemini)...")
llm_evaluation = GoogleGenAI(
    model="models/gemini-2.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1,        
    max_tokens=8192
)
print("[INIT] LLM giudice (Gemini) caricato.")

print("[INIT] Caricamento tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-32B-Instruct")
print("[INIT] Tokenizer caricato.")

def count_tokens(text: str) -> int:
    """Conta i token nel testo usando il tokenizer del modello."""
    return len(tokenizer.encode(text))

def get_context_from_knowledge_base(query, topk, target_tokens, hyde_doc=None):
    print(f"  [RETRIEVE] Query: {query[:80]}... | topk={topk} | target_tokens={target_tokens}")
    
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collectionname,
        enable_hybrid=True,
        dense_vector_name="bge_m3",
        sparse_vector_name="bm25",
        fastembed_sparse_model="Qdrant/bm25"
    )

    index = None

    if TECNICA_CHUNKING == "hierarchical":
        try:
            storage_context = StorageContext.from_defaults(persist_dir=os.path.join(SCRIPT_DIR, "storage_hierarchical"))
            index = VectorStoreIndex.from_vector_store(
                        vector_store=vector_store,
                        storage_context=storage_context
                    )
            print("Docstore caricato da disco locale.")

        except Exception as e:

            print(f"Attenzione: Impossibile caricare StorageContext locale: {e}")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

    else:
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    # Configura retriever in base alla tecnica
    retriever = None
    
    if TECNICA_RETRIEVE == "Hybrid + Base":
        # Usa VectorStoreQueryMode.HYBRID nativo di Qdrant
        retriever = index.as_retriever(
            vector_store_query_mode=VectorStoreQueryMode.HYBRID,
            similarity_top_k=topk,
            sparse_top_k=topk,
            filters=None
        )
    else:
        # Dense search (per Dense + Base e Dense + HyDE)
        retriever = index.as_retriever(
            vector_store_query_mode=VectorStoreQueryMode.DEFAULT,
            similarity_top_k=topk,
            filters=None
        )

    # Configura augmentation in base alla tecnica
    custom_embeddings = [hyde_doc] if "HyDE" in TECNICA_RETRIEVE and hyde_doc else None
    if custom_embeddings:
        print(f"  [RETRIEVE] Custom embedding generato per query: {custom_embeddings[0][:80]}...")

    query_bundle = QueryBundle(
        query_str=query,
        custom_embedding_strs=custom_embeddings
    )

    # Retrieve dei nodi
    nodes = []
    if TECNICA_CHUNKING == "hierarchical":
        automerging_retriever = AutoMergingRetriever(
            retriever, 
            storage_context=storage_context, 
            verbose=True,
        )
        nodes = automerging_retriever.retrieve(query_bundle)
    else:
        nodes = retriever.retrieve(query_bundle)

    

    print(f"  [RETRIEVE] Nodi recuperati pre-rerank: {len(nodes)}")
    nodes = reranka(nodes, query, topk)
    print(f"  [RETRIEVE] Nodi dopo rerank: {len(nodes)}")
    
    # Prendi TUTTI i nodi rerankati e costruisci il contesto completo
    context_parts = [
        f"--- Documento: {node_ws.node.metadata.get('origin_filename', 'Unknown File')} "
        f"(Pag. {node_ws.node.metadata.get('pages', [])}) ---\n{node_ws.node.get_content().strip()}\n"
        for node_ws in nodes
    ]

    # Estrai informazioni sui chunk retrievati
    retrieved_chunks_info = []
    for node_ws in nodes:
        retrieved_chunks_info.append({
            'filename': node_ws.node.metadata.get('origin_filename', 'Unknown File'),
            'chunk_index': node_ws.node.metadata.get('chunk_index', -1),
            'score': node_ws.score,
            'content': node_ws.node.get_content().strip()
        })

    # Taglia il contesto a livello di chunk per rispettare target_tokens
    selected_chunks = []
    selected_chunks_info = []

    for i, chunk_part in enumerate(context_parts):
        # Crea la stringa temporanea con il nuovo chunk
        if selected_chunks:
            temp_context = "\n".join(selected_chunks + [chunk_part])
        else:
            temp_context = chunk_part
        
        temp_tokens = len(tokenizer.encode(temp_context))
        
        # Se è il primo chunk e supera il target, includilo comunque
        if i == 0 and temp_tokens > target_tokens:
            selected_chunks.append(chunk_part)
            selected_chunks_info.append(retrieved_chunks_info[i])
            print(f"  [RETRIEVE] Primo chunk troppo grande ({temp_tokens} token), incluso comunque")
            break
        
        # Se aggiungere questo chunk supera il target, fermati
        if temp_tokens > target_tokens:
            break
        
        # Aggiungi il chunk
        selected_chunks.append(chunk_part)
        selected_chunks_info.append(retrieved_chunks_info[i])

    context_str = "\n".join(selected_chunks)
    retrieved_chunks_info = selected_chunks_info
    final_tokens = len(tokenizer.encode(context_str))

    print(f"  [RETRIEVE] Selezionati {len(selected_chunks)} chunk per {final_tokens} token (target: {target_tokens})")
    
    return context_str, retrieved_chunks_info        


def answer_question(query, topk, target_tokens, hyde_doc=None):
    print(f"  [ANSWER] Inizio risposta per: {query[:80]}...")

    context_str, retrieved_chunks_info = get_context_from_knowledge_base(query, topk, target_tokens, hyde_doc)

    system_prompt_content = (
        "Sei un assistente tecnico esperto del sistema WMS WAMAS. "
        "Il tuo obiettivo è fornire risposte precise, professionali e basate esclusivamente sui dati forniti.\n\n"
        
        "### REGOLE DI COMPORTAMENTO:\n"
        "1. Usa SOLTANTO il contesto fornito nei tag <context> per rispondere.\n"
        "2. Se le informazioni necessarie per rispondere non sono presenti nel contesto, rispondi testualmente: "
        "'Mi dispiace, ma non ho informazioni sufficienti nel manuale WAMAS per rispondere a questa domanda.'\n"
        "3. Non utilizzare conoscenze esterne al di fuori del contesto fornito.\n"
        "4. Mantieni un tono tecnico, asciutto e professionale.\n"
        "5. Se possibile, cita la sezione o il capitolo specifico se presente nel testo.\n\n"
        
        f"<context>\n{context_str}\n</context>\n\n"
        
        "### ISTRUZIONE FINALE:\n"
        "Rispondi alla domanda dell'utente in modo strutturato (usa elenchi puntati se la procedura è complessa)."
    )

    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=system_prompt_content),
        ChatMessage(role=MessageRole.USER, content=query)
    ]

    print(f"  [ANSWER] Invio richiesta a LLM...")
    response = llm.chat(messages)
    print(f"  [ANSWER] Risposta ricevuta.")
    return response.message.content, context_str, retrieved_chunks_info


class Evaluation(BaseModel):
    reasoning: list[str] = Field(
        description=
            "Lista di passaggi logici che analizzano la risposta fornita dall'LLM rispetto alla domanda originale e al ground thruth fornito."
            "Valutando se la risposta è corretta, pertinente e basata sui dati forniti"
            "Se il llm fornisce una risposta errata o incompleta deve essere considerata come '0', se dice 'non so' o 'non ho abbastanza informazioni per rispondere', deve essere considerata come '-1', mentre se è corretta allora va valutata come '1'."
        )
    evaluation: int = Field(
        description="Valutazione finale: '1' se la risposta è corretta e soddisfacente, '0' se è sbagliata, '-1' se il modello dice di non sapere la risposta o se non ha abbastanza informazioni per rispondere."
    )


#TODO: AGGIUNGERE RIGA SOTTO AL LLM PROMPT PER HIERARCHICAL
#Nota: i chunk del ground truth sono in realtà chunk figli, mentre al LLM da valutare viene data una versione già "fusa" di quei chunk.
JUDGMENT_PROMPT = """
Sei un esperto valutatore di risposte generate da modelli di linguaggio (LLM) in ambito tecnico-logistico.
Il tuo compito è valutare la qualità e l'accuratezza della risposta fornita dall'LLM a una domanda, basandoti esclusivamente sul ground truth fornito.
L'obiettivo è valutare la qualità della risposta.
Il ground truth è un insieme di chunk di testo estratti da manuali tecnici, procedure operative e documentazione ufficiale del sistema WAMAS, che contengono le informazioni corrette per rispondere alla domanda.
La risposta dell'LLM deve essere valutata come segue:
- '1' se la risposta è corretta, pertinente e basata sui dati forniti
- '0' se la risposta è errata, fuorviante o incompleta rispetto al ground truth
- '-1' se la risposta indica esplicitamente che il modello non sa la risposta o non ha abbastanza informazioni per rispondere

Nota: i chunk del ground truth sono in realtà chunk figli, mentre al LLM da valutare viene data una versione già "fusa" di quei chunk perché il metodo di chunking è il chunking gerarchico

DOMANDA UTENTE:
{query}
----------

GROUND TRUTH:
{ground_truth}
----------

RISPOSTA FORNITA DALL'LLM:
{answer}
----------
"""

prompt = PromptTemplate(JUDGMENT_PROMPT)

def evaluate_answer(query, testo_risposta, ground_truth):
    print(f"  [EVAL] Valutazione risposta per: {query[:80]}...")

    max_retries = 8
    base_delay = 5
    response = None
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            response = llm_evaluation.structured_predict(
            Evaluation,
            prompt=prompt,
            query=query,
            answer=testo_risposta,
            ground_truth=ground_truth
            )
            if response.evaluation is not None:
                break
            else:
                continue
        except (ServiceUnavailable, ResourceExhausted, DeadlineExceeded, InternalServerError) as e:
            # Errori transitori: 503, 429, timeout, ecc.
            last_error = e
            msg = str(e)
            sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 3)
            print(f"⚠️ Errore LLM transitorio ({msg}). Riprovo tra {sleep_time:.2f}s")
            time.sleep(sleep_time)
            continue
        except Exception as e:
            # Prova a riconoscere errori transitori anche da stringhe
            last_error = e
            msg_low = str(e).lower()
            transient = any(t in msg_low for t in ["503", "unavailable", "overloaded", "429", "rate", "quota", "timeout", "temporar"])
            if transient and attempt < max_retries - 1:
                sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 3)
                print(f"⚠️ Problema: {e}. Riprovo tra {sleep_time:.2f}s")
                time.sleep(sleep_time)
                continue
            print(f"❌ Errore fatale: {e}")
            break

    if response is None or response.evaluation is None:
        # Abbiamo fallito tutte le retry
        if last_error:
            print(f"  [EVAL] Saltato dopo {max_retries} tentativi: {last_error}")
        return None

    print(f"  [EVAL] Valutazione: {response.evaluation}")
    return response.evaluation


def parse_chunk_index(chunk_index_value):
    if chunk_index_value is None:
        return []
    if isinstance(chunk_index_value, list):
        return [int(idx) for idx in chunk_index_value]
    if isinstance(chunk_index_value, int):
        return [chunk_index_value]
    if isinstance(chunk_index_value, str):
        if "," in chunk_index_value:
            parts = [p.strip() for p in chunk_index_value.split(",") if p.strip()]
            return [int(idx) for idx in parts]
        return [int(chunk_index_value.strip())] if chunk_index_value.strip() else []
    return []


def fetch_gt_context(conn_history, gt_filename, gt_chunks):
    if not gt_filename or not gt_chunks:
        return ""

    placeholders = ",".join("?" for _ in gt_chunks)
    query = (
        "SELECT chunk_index, text_content FROM document_chunks "
        "WHERE filename = ? AND chunk_index IN (" + placeholders + ") "
        "ORDER BY chunk_index ASC"
    )
    params = [gt_filename, *gt_chunks]
    rows = conn_history.execute(query, params).fetchall()
    return "\n\n".join(row[1] for row in rows if row[1])


def process_single_question(domanda, topk, target_tokens, gt_contesto, gt_filename, gt_chunks, hyde_doc=None):
    """
    Processa una singola domanda e restituisce il risultato della valutazione.
    Questa funzione è pensata per essere eseguita in parallelo.
    """
    try:
        print(f"  [PROCESS] Inizio processing domanda: {domanda[:80]}...")
        risposta, context_str, retrieved_chunks_info = answer_question(domanda, topk, target_tokens, hyde_doc)

        valutazione = evaluate_answer(domanda, risposta, gt_contesto)
        print(f"  [PROCESS] Domanda completata. Valutazione: {valutazione}")
        
        return {
            'success': True, 
            'evaluation': valutazione,
            'skipped': valutazione is None,
            'risposta': risposta,
            'retrieved_chunks': retrieved_chunks_info,
            'target_tokens': target_tokens,
            'gt_filename': gt_filename,
            'gt_chunks': gt_chunks
        }
    except Exception as e:
        print(f"\n❌ Error processing question: {str(e)}")
        return {
            'success': False, 
            'evaluation': None, 
            'error': str(e),
            'skipped': False,
            'risposta': None,
            'retrieved_chunks': [],
            'target_tokens': target_tokens,
            'gt_filename': None,
            'gt_chunks': []
        }


if __name__ == "__main__":
    print("\n" + "="*60)
    print("[START] Avvio RAG Evaluation")
    print("="*60)

    dettagli_valutazione_rag = []  # Lista per salvare i dettagli di ogni singola domanda in ottica rag
    dettagli_valutazione_llm = []  #lista per eval di llm

    # Connessione al database
    eval_db_path = os.path.join(SCRIPT_DIR, db_eval)
    print(f"[DB] Connessione a eval DB: {eval_db_path}")
    conn_eval = sqlite3.connect(eval_db_path)
    # Estrai le domande come DataFrame
    df_eval = pd.read_sql_query("SELECT * FROM evaluation_table", conn_eval)
    # Chiudi la connessione
    conn_eval.close()
    print(f"[DB] Caricate {len(df_eval)} domande dal DB eval. Connessione chiusa.")
    # Ottieni lista di domande
    history_db_path = os.path.join(PROJECT_ROOT, db_history)
    print(f"[DB] Connessione a history DB: {history_db_path}")
    conn_history = sqlite3.connect(history_db_path)


    tempo_inizio = time.time()

    for t in TOP_K_CONFIG:
        topk = TOP_K_CONFIG[t]['topk']
        target_tokens = TOP_K_CONFIG[t]['target_tokens']
        print(f"\n[RUN] === Configurazione {t}: topk={topk}, target_tokens={target_tokens} ===")

        valutazionipositive = 0
        llm_risposta_sbagliata = 0
        llm_non_sa = 0

        skipped = 0
        errori = 0

        tasks = []

        print(f"[RUN] Preparazione task per {len(df_eval)} domande...")
        for _, row in tqdm(
            df_eval.iterrows(),
            total=len(df_eval),
            desc=f"Preparazione domande ({TECNICA_RETRIEVE} | {t})",
            unit="query",
            dynamic_ncols=True,
        ):
            domanda = row["question"]
            gt_filename = row["filename"]
            gt_chunks = parse_chunk_index(row["chunk_index"])
            gt_contesto = fetch_gt_context(conn_history, gt_filename, gt_chunks)
            hyde_doc = row.get("hypothetical_doc") if "hypothetical_doc" in row.index else None
            tasks.append((domanda, gt_contesto, gt_filename, gt_chunks, hyde_doc))


        print(f"[RUN] {len(tasks)} task preparati. Avvio processing parallelo con {MAX_WORKERS} worker...")
        # Processing parallelo delle domande
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Sottometti tutti i task
            futures = {
                executor.submit(
                    process_single_question,
                    domanda,
                    topk,
                    target_tokens,
                    gt_contesto,
                    gt_filename,
                    gt_chunks,
                    hyde_doc,
                ): (domanda, gt_filename, gt_chunks)
                for (domanda, gt_contesto, gt_filename, gt_chunks, hyde_doc) in tasks
            }
                
            # Processa i risultati man mano che completano
            with tqdm(
                total=len(tasks),
                desc=f"  Questions ({TECNICA_RETRIEVE} | {t})",
                leave=False,
            ) as pbar:
                for future in as_completed(futures):
                    domanda, gt_filename, gt_chunks = futures[future]
                    result = future.result()
                    
                    # Estrai informazioni sui chunk retrievati (solo quelli del documento GT)
                    retrieved_chunks = result.get('retrieved_chunks', [])
                    retrieved_chunk_ids = [
                        chunk['chunk_index'] for chunk in retrieved_chunks 
                        if chunk['filename'] == gt_filename
                    ]
                    
                    # Salva i dettagli della singola domanda
                    valutazione_rag = {
                        'domanda': domanda,
                        'tecnica_retrieve': TECNICA_RETRIEVE,
                        'tecnica_chunking': TECNICA_CHUNKING,
                        'topk': topk,
                        'target_tokens': result.get('target_tokens', target_tokens),
                        'llm_risposta_corretta': 1 if result.get('evaluation') == 1 else 0,
                        'skipped': 1 if result.get('skipped') else 0,
                        'error': 1 if not result.get('success') else 0
                    }

                    valutazione_llm = {
                        'domanda': domanda,
                        'tecnica_retrieve': TECNICA_RETRIEVE,
                        'tecnica_chunking': TECNICA_CHUNKING,
                        'topk': topk,
                        'target_tokens': result.get('target_tokens', target_tokens),
                        'llm_risposta_corretta': 1 if result.get('evaluation') == 1 else 0,
                        'llm_risposta_sbagliata': 1 if result.get('evaluation') == 0 else 0,
                        'llm_non_sa': 1 if result.get('evaluation') == -1 else 0,
                        'skipped': 1 if result.get('skipped') else 0,
                        'error': 1 if not result.get('success') else 0,
                        'gt_filename': gt_filename,
                        'gt_chunks': gt_chunks,
                        'retrieved_chunk_ids': retrieved_chunk_ids
                    }

                    dettagli_valutazione_rag.append(valutazione_rag)
                    dettagli_valutazione_llm.append(valutazione_llm)
                        
                    if result['success']:
                        if result['skipped']:
                            skipped += 1
                        elif result['evaluation'] == 1:
                            valutazionipositive += 1
                        elif result['evaluation'] == 0:
                            llm_risposta_sbagliata += 1
                        elif result['evaluation'] == -1:
                            llm_non_sa += 1
                            
                    else:
                        errori += 1
                            
                    pbar.update(1)

                    # Pulizia memoria ad ogni query per gestire uso intensivo del tokenizer
                    gc.collect()
            
        # Calcola lo score percentuale
        totale = valutazionipositive + llm_risposta_sbagliata + llm_non_sa
        score = (valutazionipositive / totale * 100) if totale > 0 else 0
            
        print(f"\n✓ Results: {valutazionipositive}/{totale} correct ({score:.1f}%)", end='')
        if skipped > 0:
            print(f" | {skipped} skipped", end='')
        if errori > 0:
            print(f" | {errori} errors", end='')
        print()

    # Crea il DataFrame con i risultati dettagliati
    df_dettagli_rag = pd.DataFrame(dettagli_valutazione_rag)
    df_dettagli_llm = pd.DataFrame(dettagli_valutazione_llm)
    
    # Chiudi la connessione history
    conn_history.close()
    print("[DB] Connessione history chiusa.")

    # Salva i risultati in CSV
    rag_csv_path = os.path.join(SCRIPT_DIR, f'RAG_evaluation_results_{TECNICA_CHUNKING}_pro_dott.csv')
    llm_csv_path = os.path.join(SCRIPT_DIR, f'LLM_evaluation_results_{TECNICA_CHUNKING}_pro_dott.csv')
    df_dettagli_rag.to_csv(rag_csv_path, index=False)
    df_dettagli_llm.to_csv(llm_csv_path, index=False)
    
    print(f"\n✅ Risultati salvati in: {rag_csv_path}")
    print(f"✅ Dettagli LLM salvati in: {llm_csv_path}")
    print("\n" + "="*60)
    print("[DONE] RAG Evaluation completata.")
    print(f"Tempo totale: {(time.time() - tempo_inizio)/60:.2f} minuti")
    print("="*60)