import os
import json
import sqlite3
from typing import List

from llama_index.llms.openai_like import OpenAILike
from llama_index.core import PromptTemplate
from pydantic import BaseModel, Field
from tqdm import tqdm
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

#nomi possibili:
# docling_eval
# overlap_eval
# hierarchical_eval


#MODIFICARE
nome_db = "overlap_eval"


url_llm = os.getenv("VLLM_API_BASE_URL")

llm = OpenAILike(
    model='Qwen/Qwen3-32B-AWQ',
    api_base=url_llm,
    api_key="null",
    is_chat_model=True,
    is_function_calling_model=True,
    timeout=60.0,
    temperature=0.3,
    context_window=8192
)

class MultiQueryOutput(BaseModel):
    queries: List[str] = Field(
        description="Lista di riformulazioni alternative della domanda originale, con fraseggio diverso ma significato equivalente."
    )

MULTIQUERY_TEMPLATE_STR = (
    "Sei un assistente esperto del sistema WAMAS (WMS / ERP di magazzino).\n"
    "Data una domanda utente, genera 4 riformulazioni alternative della stessa domanda, utili a migliorare il retrieval "
    "in un sistema RAG su documentazione logistica.\n\n"
    "Regole:\n"
    "- Mantieni intatto il significato e l'intento della domanda originale.\n"
    "- Varia il lessico: sinonimi, termini tecnici specifici di magazzino (UDC, picking, stoccaggio, carico, ecc.), parafrasi naturali.\n"
    "- Alterna formulazioni colloquiali e tecniche.\n"
    "- NON aggiungere informazioni non presenti né inventare vincoli non impliciti nella domanda.\n"
    "- NON ripetere la domanda originale tra le riformulazioni.\n\n"
    "Domanda utente: {query}"
)
multiquery_prompt = PromptTemplate(MULTIQUERY_TEMPLATE_STR)

def generate_multiqueries(query_text):
    try:
        risultato = llm.structured_predict(
            MultiQueryOutput,
            prompt=multiquery_prompt,
            query=query_text
        )
        return risultato.queries

    except Exception as e:
        print(f"Errore nella generazione strutturata: {e}")

        return None



#test (inutile)
if __name__ == "__main__":
    #MODIFICARE
    conn = sqlite3.connect(f"./{nome_db}.db", check_same_thread=False)

    df = pd.read_sql_query("SELECT * FROM question_table", conn)
    cursor = conn.cursor()

    # Ricrea la tabella di evaluation con schema corretto (no unique su filename/chunk)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evaluation_table'")
    if cursor.fetchone():
        cursor.execute("DROP TABLE evaluation_table")
        conn.commit()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluation_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        chunk_index TEXT,
        question TEXT,
        multi_queries TEXT
    )
""")
    conn.commit()


    print("Tabella evaluation_table svuotata.")



    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing questions", unit="query", dynamic_ncols=True):
        try:
            queries = generate_multiqueries(row['question'])
            mq_str = json.dumps(queries, ensure_ascii=False) if queries else None

            cursor.execute("""
            INSERT INTO evaluation_table (filename, chunk_index, question, multi_queries)
            VALUES (?, ?, ?, ?)""",
            (row['filename'], row['chunk_index'], row['question'], mq_str))
            conn.commit()
        except Exception as e:
            print(f"Errore nella generazione per la domanda '{row['question']}': {e}")


    conn.close()
