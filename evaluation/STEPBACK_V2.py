import os

from llama_index.llms.openai_like import OpenAILike
from llama_index.core import PromptTemplate
from pydantic import BaseModel, Field
import sqlite3
from tqdm import tqdm
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

class StepBackOutput(BaseModel):
    step_back_question: str = Field(
        description="Versione più generale e astratta della domanda originale, che ne catturi il concetto/processo sottostante."
    )

STEPBACK_TEMPLATE_STR = (
    "Sei un assistente esperto del sistema WAMAS (WMS / ERP di magazzino).\n"
    "Data una domanda utente molto specifica, riformulala in una versione PIÙ GENERALE e astratta: "
    "una 'step-back question' che catturi il concetto, il processo o la categoria di riferimento sottostante, "
    "così da recuperare documentazione di contesto più ampia utile a rispondere alla domanda originale.\n\n"
    "Regole:\n"
    "- Astrai dai dettagli operativi (valori specifici, codici, messaggi di errore, nomi di pulsanti) verso il processo/concetto generale.\n"
    "- La step-back question deve essere sensata da sola e rispondibile da documentazione procedurale.\n"
    "- NON deve essere identica o quasi identica alla domanda originale.\n"
    "- Scrivila in linguaggio naturale, come la farebbe un operatore che vuole capire il principio generale.\n\n"
    "Esempio:\n"
    "Domanda specifica: \"Perché il tasto 'Conferma' nella maschera di uscita merce è grigio e non cliccabile?\"\n"
    "Step-back: \"In quali condizioni un'operazione di uscita merce in WAMAS risulta bloccata o non confermabile?\"\n\n"
    "Domanda utente: {query}"
)
stepback_prompt = PromptTemplate(STEPBACK_TEMPLATE_STR)

def generate_stepback(query_text):
    try:
        risultato = llm.structured_predict(
            StepBackOutput,
            prompt=stepback_prompt,
            query=query_text
        )
        return risultato.step_back_question

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
        step_back_question TEXT
    )
""")
    conn.commit()


    print("Tabella evaluation_table svuotata.")



    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing questions", unit="query", dynamic_ncols=True):
        try:
            sb = generate_stepback(row['question'])

            cursor.execute("""
            INSERT INTO evaluation_table (filename, chunk_index, question, step_back_question)
            VALUES (?, ?, ?, ?)""",
            (row['filename'], row['chunk_index'], row['question'], sb))
            conn.commit()
        except Exception as e:
            print(f"Errore nella generazione per la domanda '{row['question']}': {e}")


    conn.close()
