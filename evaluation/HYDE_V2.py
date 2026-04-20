import os

from llama_index.llms.openai_like import OpenAILike
from llama_index.core import PromptTemplate
from pydantic import BaseModel, Field
import json, sys
from tqdm import tqdm
import sqlite3
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

#nomi possibili:
# docling_eval
# overlap_eval
# hierarchical_eval


#MODIFICARE
nome_db = "DUMMY"


url_llm = os.getenv("VLLM_API_BASE_URL")

llm = OpenAILike(
    model='Qwen/Qwen3-32B-AWQ',
    api_base=url_llm,
    api_key="null",
    is_chat_model=True,
    is_function_calling_model=True,
    timeout=60.0,
    temperature=0.1,
    context_window=8192
)

class DocumentoIpotetico(BaseModel):
    contenuto_tecnico: str = Field(
        description="Un breve paragrafo tecnico che descrive la soluzione procedurale al problema."
    )

#Scrivi un paragrafo tecnico tratto da un manuale di gestione di magazzino (WMS) o procedure ERP che spieghi come risolvere la seguente discrepanza
HYDE_TEMPLATE_STR = (
    "Sei un tecnico esperto del sistema WAMAS.\n"
    "Genera una soluzione procedurale ipotetica per il seguente problema utente.\n"
    "Scrivi un paragrafo tecnico tratto da un manuale di gestione di magazzino (WMS) o procedure ERP che spieghi come risolvere il problema. "
    "Usa terminologia specifica di magazzino, nomi di maschere o processi standard.\n\n"
    "Domanda utente: {query}"
)
hyde_prompt = PromptTemplate(HYDE_TEMPLATE_STR)

def generate_hypothetical_doc(query_text):
    #print(f"\n--- Generazione Documento Ipotetico Strutturato per: '{query_text}' ---")
    
    try:
        risultato = llm.structured_predict(
            DocumentoIpotetico,
            prompt=hyde_prompt,
            query=query_text
        )
        doc_text = risultato.contenuto_tecnico
        
        return doc_text

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
        hypothetical_doc TEXT
    )
""")
    conn.commit()


    
    print("Tabella evaluation_table svuotata.")

    

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing questions", unit="query", dynamic_ncols=True):
        try:
            hd = generate_hypothetical_doc(row['question'])

            cursor.execute("""
            INSERT INTO evaluation_table (filename, chunk_index, question, hypothetical_doc)
            VALUES (?, ?, ?, ?)""",
            (row['filename'], row['chunk_index'], row['question'], hd))
            conn.commit()
        except Exception as e:
            print(f"Errore nella generazione per la domanda '{row['question']}': {e}") 

    
    conn.close()