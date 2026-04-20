

import sqlite3
from llama_index.core.schema import TextNode
import os
import json
from pydantic import BaseModel, Field
from llama_index.core import PromptTemplate, Settings
from llama_index.llms.openai_like import OpenAILike
from tqdm import tqdm
from dotenv import load_dotenv
from difflib import SequenceMatcher # Necessario per controllare duplicati

load_dotenv()

# nomi possibili:
# docling_eval
# WAMASRAGBASE

# overlap_eval
# WAMASRAGOVERLAP

# hierarchical_eval
# WAMASHIERARCHICAL


#MODIFICARE
evaluation_name = "overlap_eval"
chunk_name = "WAMASRAGOVERLAP"
skip_initial_chunks = True 
skip_images = True
min_chunk_length = 100 

# Rimuovi il DB se esiste (prima di aprire una connessione)
if os.path.exists(f"./{evaluation_name}.db"):
    try:
        os.remove(f"./{evaluation_name}.db")
    except Exception as e:
        print(f"Errore rimozione DB: {e}")

conn_evaluation = sqlite3.connect(f"./{evaluation_name}.db", check_same_thread=False)
cursor_evaluation = conn_evaluation.cursor()

cursor_evaluation.execute("""
    CREATE TABLE IF NOT EXISTS question_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        chunk_index INTEGER,
        question TEXT
    )
""")
conn_evaluation.commit()




conn = sqlite3.connect(f"../{chunk_name}.db", check_same_thread=False)
cursor = conn.cursor()

connsummary = sqlite3.connect("../RIASSUNTODOCUMENTI.db", check_same_thread=False)
cursorsummary = connsummary.cursor()

# Recupero lista file
res = cursor.execute("SELECT DISTINCT filename FROM document_chunks")
filenames = [row[0] for row in res.fetchall()]

listanodi = []

# --- CREAZIONE NODI ---
for i, filename in enumerate(filenames):
    nchunks = []
    try:
        res = cursor.execute(
            "SELECT chunk_index, text_content FROM document_chunks WHERE filename = ?", 
            (filename,)
        ).fetchall()
        # Filtro base per contenuto vuoto
        nchunks = [r for r in res if r[1] and r[1].strip() != '']
    except Exception as e:
        print(f"Problemi per {filename}: {e}")
    res_summary = None
    try:
        res_summary = cursorsummary.execute(
            "SELECT text_summary FROM document_chunks WHERE filename = ?", 
            (filename,)
        ).fetchone()
        if res_summary:
            print(f"Riassunto trovato per {filename}")
    except Exception as e2:
        print(f"Problemi nel recuperare il riassunto per {filename}: {e2}")
    #MODIFICARE
    for c in nchunks:
        # Skip indici iniziali (spesso indici o copertine)
        if c[0] in [0, 1, 2] and skip_initial_chunks:
            continue
        # Skip immagini
        if "<image>" in c[1] and skip_images:
            continue
        # Skip chunk troppo corti
        if len(c[1]) < min_chunk_length:
            continue
            
        nodotesto = TextNode(
            text=c[1], 
            metadata={
                "origin_filename": filename, 
                "chunk_index": c[0], 
                "summary": res_summary[0]
            }
        )
        listanodi.append(nodotesto)

# --- CONFIGURAZIONE LLM ---
VLLM_API_BASE_URL = os.getenv("VLLM_API_BASE_URL")

llm = OpenAILike(
    model='Qwen/Qwen2.5-32B-Instruct-AWQ',
    api_base=VLLM_API_BASE_URL,
    api_key="fake", 
    is_chat_model=True,
    is_function_calling_model=True, 
    context_window=8192,
    temperature=0.1
)

Settings.llm = llm

# --- PROMPT OTTIMIZZATO ---
QUESTION_PROMPT = """
Sei un esperto creatore di dataset per la valutazione di sistemi RAG (Retrieval Augmented Generation) in ambito logistico (WAMAS).
Il tuo compito è analizzare il <CHUNK_CONTENT> e generare da 1 a 3 domande tecniche e specifiche.

REGOLE CRITICHE:
1. **FONTE DELLA VERITÀ:** Le risposte devono trovarsi ESPLICITAMENTE nel testo del <CHUNK_CONTENT>. 
   - Il <DOCUMENT_SUMMARY> serve SOLO per decifrare acronimi o capire il contesto generale. NON usarlo per formulare le domande o le risposte.

2. **SPECIFICITÀ:** 
   - EVITA domande generiche come "Qual è l'obiettivo del documento?" o "Di cosa parla il testo?".
   - Crea domande che richiedono dettagli presenti nel chunk (es. codici errore, nomi pulsanti, procedure passo-passo).

3. **REALISMO:** Formula le domande come le farebbe un utente reale:
   - Usa SINONIMI e PARAFRASI (es. se il chunk dice "errore", chiedi "problema" o "malfunzionamento")
   - Varia il LIVELLO DI DETTAGLIO (es. chiedi la procedura completa invece di un singolo passo)
   - Usa termini COLLOQUIALI quando appropriato (es. "come faccio a..." invece di "qual è la procedura per...")
   - NON copiare letteralmente frasi dal chunk

4. **SELF-CONTAINED:** La domanda deve avere senso da sola. Sostituisci pronomi come "esso", "questa procedura" con il nome reale dell'oggetto.

5. **FORMATO:** Le domande devono essere frasi interrogative che terminano con "?".

6. **NIENTE DOMANDE:** Se il chunk non contiene informazioni utili (es. è solo un elenco di nomi o un piè di pagina), restituisci una lista vuota.

ESEMPI:
- ❌ "Qual è il codice errore 404 in WAMAS?" (troppo letterale)
- ✅ "Cosa significa quando il sistema mi dice che non trova il pallet?" (realistica)

- ❌ "Quale pulsante premere per confermare l'operazione?" (troppo specifica)
- ✅ "Come completo il picking dopo aver scannerizzato gli articoli?" (più contestuale)

Contesto del documento (DA USARE SOLO PER CONTESTO):
----------------
{document_summary}
----------------

Chunk di testo (DA USARE PER GENERARE LE DOMANDE):
----------------
{chunk_text}
----------------
"""

prompt = PromptTemplate(QUESTION_PROMPT)

class QuestionOutput(BaseModel):
    analysis: str = Field(description="Una breve analisi (Chain-of-Thought) per decidere se il chunk merita domande e quali dettagli estrarre.")
    questions: list[str] = Field(description="Una lista di domande (max 3) pertinenti. Lasciare vuoto se il chunk non è significativo.")

# --- FUNZIONI DI UTILITÀ ---

def is_too_similar(q1, q2, threshold=0.85):
    """Controlla se due domande sono quasi identiche usando la similarità di stringa."""
    return SequenceMatcher(None, q1, q2).ratio() > threshold

def generate_questions(chunk_text, riassunto_documento):
    try:
        risultato = llm.structured_predict(
            QuestionOutput,
            prompt=prompt,
            chunk_text=chunk_text,
            document_summary=riassunto_documento
        )
        return risultato.questions
    except Exception as e:
        # Fallback in caso di errore LLM
        print(f"Errore LLM: {e}")
        return []

# --- LOOP PRINCIPALE ---

listadomande = []
# Buffer per ricordare le ultime domande e evitare duplicati consecutivi
recent_questions_buffer = [] 

for nodo in tqdm(listanodi, desc="Generazione domande", unit="nodo"):
    
    domande_generate = generate_questions(nodo.text, nodo.metadata.get("summary"))
    
    domande_filtrate = []
    
    if domande_generate:
        for q in domande_generate:
            q = q.strip()
            
            # 1. Deve finire con ?
            if not q.endswith('?'):
                continue
                
            # 2. Controllo duplicati rispetto alle ultime 10 domande generate
            is_duplicate = False
            for recent_q in recent_questions_buffer[-15:]: 
                if is_too_similar(q, recent_q):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                domande_filtrate.append(q)
                recent_questions_buffer.append(q)
                
        # Mantieni il buffer piccolo
        if len(recent_questions_buffer) > 20:
            recent_questions_buffer = recent_questions_buffer[-20:]

    # Aggiungi al dataset solo se abbiamo trovato domande valide
    if domande_filtrate:
        for d in domande_filtrate:
            listadomande.append((nodo.metadata.get('origin_filename', "unknown"), nodo.metadata.get('chunk_index', -1), d))
    else:

        pass

# --- SALVATAGGIO ---

cursor_evaluation.executemany(
        "INSERT INTO question_table (filename, chunk_index, question) VALUES (?, ?, ?)", 
        listadomande
    )
conn_evaluation.commit()