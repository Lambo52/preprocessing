
#PRENDE LA QUESTION_TABLE E CI ASSEGNA IL CHUNK_INDEX GRAZIE A GEMINI

import sqlite3
import os
import json
import sys
import time
import random
from typing import List
from pydantic import BaseModel, Field
from llama_index.core import PromptTemplate, Settings
from llama_index.llms.google_genai import GoogleGenAI
from tqdm import tqdm
from dotenv import load_dotenv
try:
    from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted, DeadlineExceeded, InternalServerError
except Exception:
    ServiceUnavailable = ResourceExhausted = DeadlineExceeded = InternalServerError = Exception

load_dotenv()

# nomi possibili:
# docling_eval / WAMASRAGBASE
# overlap_eval / WAMASRAGOVERLAP
# hierarchical_eval / WAMASHIERARCHICAL

evaluation_name = sys.argv[1]
chunk_name = sys.argv[2]

conn_evaluation = sqlite3.connect(f"./{evaluation_name}.db", check_same_thread=False)
cursor_evaluation = conn_evaluation.cursor()

cursor_evaluation.execute("""
    CREATE TABLE IF NOT EXISTS question_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        chunk_index TEXT,
        question TEXT
    )
""")
conn_evaluation.commit()

conn = sqlite3.connect(f"../{chunk_name}.db", check_same_thread=False)
cursor = conn.cursor()

# Prendo solo i file con domande ancora non associate a chunk
res = cursor_evaluation.execute(
    "SELECT DISTINCT filename FROM question_table WHERE chunk_index IS NULL"
)
filenames = [row[0] for row in res.fetchall()]
print(f"File da processare: {len(filenames)}")

llm = GoogleGenAI(
    model="models/gemini-2.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2,
    max_tokens=8192,
)
Settings.llm = llm

ASSIGN_PROMPT = """
Sei un esperto di retrieval per sistemi RAG su documentazione logistica (WAMAS).

INPUT:
1) Un documento diviso in segmenti numerati, nel formato "CHUNK X: [testo]".
2) Una lista di domande generate a partire da questo documento. Ogni domanda ha un "question_id" numerico.

COMPITO:
Per ciascuna domanda, identifica l'insieme MINIMO e SUFFICIENTE di chunk che contengono l'informazione necessaria per rispondere.

REGOLE:
- Single-hop → un solo chunk_id (es. [2]).
- Multi-hop → più chunk_ids (es. [1, 4]).
- Se la domanda NON è chiaramente rispondibile usando il documento, restituisci una lista vuota [].
- NON includere chunk che non contribuiscono direttamente alla risposta.
- Gli id dei chunk devono corrispondere ESATTAMENTE a quelli indicati nel formato "CHUNK X: ...".
- Restituisci UNA entry per ogni question_id presente nella lista di domande.

DOCUMENTO:
{full_document_text}

DOMANDE:
{questions_list}
"""

prompt_assign = PromptTemplate(ASSIGN_PROMPT)


class AssignedQuestion(BaseModel):
    question_id: int = Field(..., description="ID della domanda a cui si riferisce l'assegnazione.")
    chunk_ids: List[int] = Field(..., description="Lista degli ID dei chunk che contengono la risposta (vuota se la domanda non è rispondibile).")


class AssignmentOutput(BaseModel):
    items: List[AssignedQuestion] = Field(..., description="Per ciascuna domanda, i chunk_ids corrispondenti.")


def assign_chunks(testo_completo, questions_list_str):
    return llm.structured_predict(
        AssignmentOutput,
        prompt=prompt_assign,
        full_document_text=testo_completo,
        questions_list=questions_list_str,
    )


# --- LOOP PRINCIPALE ---
for filename in tqdm(filenames, desc="Assegnazione chunk", unit="file"):
    # Carico domande ancora senza chunk_index
    qres = cursor_evaluation.execute(
        "SELECT id, question FROM question_table WHERE filename = ? AND chunk_index IS NULL",
        (filename,),
    ).fetchall()
    if not qres:
        continue

    # Carico chunk del file
    try:
        cres = cursor.execute(
            "SELECT chunk_index, text_content FROM document_chunks WHERE filename = ?",
            (filename,),
        ).fetchall()
        chunks = [(idx, txt) for idx, txt in cres if txt and txt.strip() != ""]
        chunks.sort(key=lambda x: x[0] if x[0] is not None else -1)
    except Exception as e:
        print(f"Problemi caricando chunk per {filename}: {e}")
        continue

    if not chunks:
        print(f"Nessun chunk trovato per {filename}, saltato.")
        continue

    testo_completo = "NOME FILE: " + filename + "\n\n" + "\n".join(
        f"CHUNK {idx}: [{txt}]" for idx, txt in chunks
    )

    questions_payload = [{"question_id": qid, "question": q} for qid, q in qres]
    questions_list_str = json.dumps(questions_payload, ensure_ascii=False, indent=2)

    max_retries = 8
    base_delay = 5
    result = None
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            result = assign_chunks(testo_completo, questions_list_str)
            break
        except (ServiceUnavailable, ResourceExhausted, DeadlineExceeded, InternalServerError) as e:
            last_error = e
            sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 3)
            print(f"⚠️ {filename}: Errore LLM transitorio ({e}). Riprovo tra {sleep_time:.2f}s")
            time.sleep(sleep_time)
            continue
        except Exception as e:
            last_error = e
            msg_low = str(e).lower()
            transient = any(t in msg_low for t in ["503", "unavailable", "overloaded", "429", "rate", "quota", "timeout", "temporar"])
            if transient and attempt < max_retries - 1:
                sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 3)
                print(f"⚠️ {filename}: {e}. Riprovo tra {sleep_time:.2f}s")
                time.sleep(sleep_time)
                continue
            print(f"❌ Errore fatale per {filename}: {e}")
            break

    if not result:
        if last_error:
            print(f"Saltato {filename} dopo {max_retries} tentativi: {last_error}")
        continue

    print("======== OUTPUT ASSIGNER")
    print(result.model_dump_json(indent=2))

    # Mappa question_id → chunk_ids, filtrando chunk realmente presenti
    chunks_by_q = {item.question_id: item.chunk_ids for item in result.items}
    valid_chunk_ids = {idx for idx, _ in chunks}

    for qid, _ in qres:
        assigned = chunks_by_q.get(qid, [])
        assigned = [c for c in assigned if c in valid_chunk_ids]
        chunk_index_str = ",".join(str(c) for c in assigned)
        cursor_evaluation.execute(
            "UPDATE question_table SET chunk_index = ? WHERE id = ?",
            (chunk_index_str, qid),
        )

    conn_evaluation.commit()

conn_evaluation.close()
conn.close()

print(f"\nAssegnazione chunk completata! Database aggiornato in {evaluation_name}.db")
