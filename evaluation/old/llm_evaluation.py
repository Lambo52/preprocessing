import os
import qdrant_client
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter, FilterOperator
from rerank import reranka
from pydantic import BaseModel, Field
from llama_index.core.retrievers import QueryFusionRetriever
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
import time, random, sys
from HYDE_V2 import generate_hypothetical_doc, generate_step_back


load_dotenv()

VLLM_API_BASE_URL = os.getenv("VLLM_API_BASE_URL")
QDRANT_URL = os.getenv("QDRANT_URL")
client = qdrant_client.QdrantClient(url=QDRANT_URL)


embed_model = OpenAIEmbedding(
    api_base=VLLM_API_BASE_URL,
    model_name="BAAI/bge-m3",
    api_key="null",
)
Settings.embed_model = embed_model


llm = OpenAILike(
    model='Qwen/Qwen2.5-32B-Instruct-AWQ',
    api_base=VLLM_API_BASE_URL, 
    api_key="null",
    is_chat_model=True,
    is_function_calling_model=True,    
    timeout=60.0,
    streaming=False,
    context_window=8192,
    temperature=0,
    max_tokens=1024,
)

llm_evaluaion = GoogleGenAI(
    model="models/gemini-2.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.8,        
    max_tokens=8192
)

def get_context_from_knowledge_base(query, topk, rerank_topk, tecnica_chunking, tecnica_retrieve) -> str:
    
    collectionname = ""
    
    if tecnica_chunking == "docling":
        collectionname = "WAMASRAGBASE"
    elif tecnica_chunking == "hierarchical":
        collectionname = "WAMASHIERARCHICAL"
    elif tecnica_chunking == "window":
        collectionname = "WAMASRAGBASE"
    elif tecnica_chunking == "overlap":
        collectionname = "WAMASRAGOVERLAP"

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collectionname,
        enable_hybrid=True,
        dense_vector_name="bge_m3",
        sparse_vector_name="bm25",
        fastembed_sparse_model="Qdrant/bm25"
    )

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    retriever_dense = index.as_retriever(
        vector_store_query_mode=VectorStoreQueryMode.DEFAULT, 
        similarity_top_k=topk,
        filters = None
    )
    retriever_sparse = index.as_retriever(
        vector_store_query_mode=VectorStoreQueryMode.SPARSE,
        sparse_top_k=topk,
        filters = None
    )

    retriever = QueryFusionRetriever(
        retrievers=[retriever_dense, retriever_sparse],
        similarity_top_k=2*topk,
        num_queries=1,          
        mode="simple",                                       
        use_async=False
    )

    aug_final = None
    if tecnica_retrieve == "Hybrid + HyDe":
        aug_final = [generate_hypothetical_doc(query)]
    elif tecnica_retrieve == "Hybrid + HyDe + Aug":
        hypotetical_doc = generate_hypothetical_doc(query)
        step_back = generate_step_back(query)
        if step_back:
            # Filtra eventuali stringhe vuote e unisci con il separatore |||
            aug_final = [q.strip() for q in step_back if q.strip()]
        aug_final.append(hypotetical_doc)

    query_bundle = QueryBundle(
        query_str=query,
        custom_embedding_strs = aug_final
    )

    nodes = retriever.retrieve(query_bundle)

    nodes = reranka(nodes, query, rerank_topk)

    context_parts = []
    
    docs_dict = {}
    
    for node_ws in nodes:
        filename = node_ws.node.metadata.get('origin_filename', 'Unknown File')
        page = node_ws.node.metadata.get('pages', 'N/A')
        content = node_ws.node.get_content().strip()
        context_parts.append(f"--- Documento: {filename} (Pag. {page}) ---\n{content}\n")
        
        if filename not in docs_dict:
            docs_dict[filename] = []
        
        docs_dict[filename].extend(page)
    
    
    context_parz_list = []
    for filename, pages in docs_dict.items():
        
        unique_pages = sorted(set(pages))
        
        clean_pages = [str(p).strip('[]') for p in unique_pages]
        pages_str = ", ".join(clean_pages)
        context_parz_list.append(f"--- Documento: {filename} (Pag. {pages_str}) ---")
    
    full_context = "\n".join(context_parts)

    return full_context        


def answer_question(query, topk, rerank_topk, tecnica_chunking, tecnica_retrieve) -> str:

    context_str = get_context_from_knowledge_base(query, topk, rerank_topk, tecnica_chunking, tecnica_retrieve)

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

    messages = []
    messages.append(ChatMessage(role=MessageRole.SYSTEM, content=system_prompt_content))
    messages.append(ChatMessage(role=MessageRole.USER, content=query))

    # chiamata NON streaming
    response = llm.chat(messages)

    # testo puro della risposta
    testo_risposta = response.message.content

    return testo_risposta, context_str


class Evaluation(BaseModel):
    reasoning: list[str] = Field(
        description=
            "Lista di passaggi logici che analizzano la risposta fornita dall'LLM rispetto alla domanda originale e al contesto disponibile."
            "Valutando se la risposta è corretta, pertinente e basata sui dati forniti, e identificando eventuali errori o omissioni."
            "Se i dati forniti non sono sufficienti per rispondere, il llm deve riconoscerlo esplicitamente, valutare quindi anche questo aspetto."
        )
    evaluation: bool = Field(
        description="Valutazione finale binaria: True se la risposta è corretta e soddisfacente, False altrimenti."
    )

JUDGMENT_PROMPT = """
Sei un esperto valutatore di risposte generate da modelli di linguaggio (LLM) in ambito tecnico-logistico.
Il tuo compito è valutare la qualità e l'accuratezza della risposta fornita dall'LLM a una domanda tecnica specifica, basandoti esclusivamente sul contesto disponibile.

DOMANDA UTENTE:
{query}
----------

CONTESTO DISPONIBILE:
{context}
----------

RISPOSTA FORNITA DALL'LLM:
{answer}
----------
"""

prompt = PromptTemplate(JUDGMENT_PROMPT)

def evaluate_answer(query, testo_risposta, contesto):

    max_retries = 8
    base_delay = 5
    response = None
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            response = llm_evaluaion.structured_predict(
            Evaluation,
            prompt=prompt,
            query=query,
            answer=testo_risposta,
            context=contesto
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
            print(f"Saltato dopo {max_retries} tentativi: {last_error}")
        return None

    return response.evaluation


def process_single_question(domanda, topk, rerank_topk, tecnica_chunking, tecnica_retrieve):
    """
    Processa una singola domanda e restituisce il risultato della valutazione.
    Questa funzione è pensata per essere eseguita in parallelo.
    """
    try:
        risposta, contesto = answer_question(
            domanda, 
            topk=topk, 
            rerank_topk=rerank_topk, 
            tecnica_chunking=tecnica_chunking, 
            tecnica_retrieve=tecnica_retrieve
        )
        
        valutazione = evaluate_answer(domanda, risposta, contesto)
        
        return {
            'success': True, 
            'evaluation': valutazione,
            'skipped': valutazione is None
        }
    except Exception as e:
        print(f"\n❌ Error processing question: {str(e)}")
        return {
            'success': False, 
            'evaluation': None, 
            'error': str(e),
            'skipped': False
        }


if __name__ == "__main__":

    techiche_retrieve = ["Hybrid + Base", "Hybrid + HyDe", "Hybrid + HyDe + Aug"]
    techiche_chunking = ["overlap", "hierarchical", "window", "docling"]

    # Lista per salvare tutti i risultati
    risultati_benchmark = []
    
    # Numero di worker paralleli
    MAX_WORKERS = 4

    for retrieve_tech in tqdm(techiche_retrieve, total=len(techiche_retrieve), desc="Retrieve Techniques", unit="technique"):
        
        for t in techiche_chunking:
            
            print(f"\n{'='*60}")
            print(f"Evaluating: {retrieve_tech} | Chunking: {t}")
            print(f"{'='*60}")
            
            # Connessione al database
            conn = sqlite3.connect(f"./{t}_eval.db")

            # Estrai le domande come DataFrame
            df = pd.read_sql_query("SELECT * FROM question_table", conn)

            # Chiudi la connessione
            conn.close()

            # Ottieni lista di domande
            domande = df['question'].tolist()

            topk = None
            topk_rerank = None

            if t == "docling":
                topk = 25
                topk_rerank = 10
            elif t == "hierarchical":
                topk = 43
                topk_rerank = 15
            elif t == "window":
                topk = 8
                topk_rerank = 5
            elif t == "overlap":
                topk = 5
                topk_rerank = 4

            valutazionipositive = 0
            valutazioninegative = 0
            skipped = 0
            errori = 0

            # Processing parallelo delle domande
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                # Sottometti tutti i task
                futures = {
                    executor.submit(
                        process_single_question,
                        domanda,
                        topk,
                        topk_rerank,
                        t,
                        retrieve_tech
                    ): domanda for domanda in domande
                }
                
                # Processa i risultati man mano che completano
                with tqdm(total=len(domande), desc=f"  Questions ({retrieve_tech} | {t})", leave=False) as pbar:
                    for future in as_completed(futures):
                        result = future.result()
                        
                        if result['success']:
                            if result['skipped']:
                                skipped += 1
                            elif result['evaluation']:
                                valutazionipositive += 1
                            else:
                                valutazioninegative += 1
                        else:
                            errori += 1
                            
                        pbar.update(1)
            
            # Calcola lo score percentuale
            totale = valutazionipositive + valutazioninegative
            score = (valutazionipositive / totale * 100) if totale > 0 else 0
            
            # Salva i risultati
            risultati_benchmark.append({
                'Tecnica_Retrieve': retrieve_tech,
                'Tecnica_Chunking': t.capitalize(),
                'Score': score,
                'Positive': valutazionipositive,
                'Negative': valutazioninegative,
                'Skipped': skipped,
                'Errors': errori,
                'Total': totale
            })
            
            print(f"\n✓ Results: {valutazionipositive}/{totale} correct ({score:.1f}%)", end='')
            if skipped > 0:
                print(f" | {skipped} skipped", end='')
            if errori > 0:
                print(f" | {errori} errors", end='')
            print()

    # Crea il DataFrame con i risultati
    df_results = pd.DataFrame(risultati_benchmark)
    
    # Salva i risultati in CSV
    df_results.to_csv('benchmark_results.csv', index=False)
    print(f"\n{'='*60}")
    print("✓ Results saved to benchmark_results.csv")
    print(f"{'='*60}\n")
    
    # Crea la pivot table per la heatmap
    pivot_data = df_results.pivot_table(
        index='Tecnica_Retrieve', 
        columns='Tecnica_Chunking', 
        values='Score'
    )
    
    # Ordina le righe secondo l'ordine desiderato
    order_retrieve = ["Hybrid + Base", "Hybrid + HyDe", "Hybrid + HyDe + Aug"]
    pivot_data = pivot_data.reindex([x for x in order_retrieve if x in pivot_data.index])
    
    # Ordina le colonne secondo l'ordine desiderato
    order_chunking = ["Overlap", "Hierarchical", "Window", "Docling"]
    pivot_data = pivot_data.reindex(
        columns=[x for x in order_chunking if x in pivot_data.columns]
    )
    
    # Crea la figura
    plt.figure(figsize=(12, 8))
    
    # Crea la heatmap
    sns.heatmap(
        pivot_data, 
        annot=True, 
        fmt=".1f", 
        cmap="YlGn", 
        vmin=0, 
        vmax=100,
        linewidths=0.5,
        cbar_kws={'label': 'Score (%)'}
    )
    
    plt.title("Performance RAG: Tecniche di Retrieve vs Chunking", 
              fontsize=16, fontweight='bold', pad=20)
    plt.ylabel("Tecnica di Retrieve", fontsize=12, fontweight='bold')
    plt.xlabel("Tecnica di Chunking", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    # Salva il grafico
    plt.savefig("Heatmap_RAG_Performance.png", dpi=300, bbox_inches='tight')
    print("✓ Heatmap saved to Heatmap_RAG_Performance.png")
    
    plt.show()
    
    # Stampa anche una tabella riassuntiva
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(pivot_data.to_string())
    print("="*80)