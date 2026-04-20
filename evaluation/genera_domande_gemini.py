
# GENERA LA TABELLA QUESTION_TABLE, CON DOMANDE, FILENAME E CHUNK_INDEX NULLO

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

res = cursor.execute("SELECT DISTINCT filename FROM document_chunks")
filenames = [row[0] for row in res.fetchall()]

res_existing = cursor_evaluation.execute("SELECT DISTINCT filename FROM question_table")
existing_filenames = {row[0] for row in res_existing.fetchall()}

filenames = [f for f in filenames if f not in existing_filenames]
print(f"File da processare: {len(filenames)} (saltati {len(existing_filenames)} già elaborati)")

llm = GoogleGenAI(
    model="models/gemini-2.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.8,
    max_tokens=8192,
)
Settings.llm = llm

FULL_DOC_PROMPT = """
Sei un Architetto di Dataset per la valutazione di sistemi RAG su documentazione logistica (WAMAS).

INPUT DATA:
Ti fornirò un documento markdown completo.

OBIETTIVO:
Genera domande che coprano tre profili utente:

    L'Operatore Esperto: Vuole risolvere un problema specifico o compilare un campo.

    Il Novizio/Utente in Training: Non conosce il sistema, vuole capire i concetti base o il flusso generale ("Come funziona X?", "Cosa significa Y?").

    L'Amministratore: Deve impostare parametri o gestire eccezioni complesse. Cerca la logica dietro l'azione.

REGOLE CRITICHE DI STILE (DA SEGUIRE SEMPRE):

    NO "QUIZ MODE" ACCADEMICO:

        ❌ EVITA: "Definisci cos'è una UDC." (Troppo scolastico).

        ✅ PREFERISCI: "Come faccio a creare un carico se il camion non è ancora arrivato fisicamente?" oppure "Cosa s'intende per 'Area di Picking' in questo contesto?".

    OBIETTIVO OPERATIVO:

        La domanda deve sottintendere un'intenzione. Anche se la domanda è teorica, deve servire a fare qualcosa.

        Esempio: Invece di "Quali sono gli stati dell'ordine?", chiedi "L'ordine è bloccato, quali stati devo controllare per capire perché?".

    NATURALITÀ E LIVELLI DI CONOSCENZA:

        Esperto: Usa termini precisi, ma omette i passaggi ovvi.

        Novizio: Usa termini generici ("il pacco" invece di "LU"), è confuso sui processi ("Devo salvare prima o dopo aver scansionato?").

    REALISMO:

        NON suggerire esplicitamente nella domanda in quale parte del documento si trova la risposta.

COMPITI DI GENERAZIONE:
Analizza il documento e genera una lista di domande in formato JSON suddivisa in queste categorie:

    DOMANDE SINGLE-HOP (Fatti puntuali & Troubleshooting):

        Basate su un singolo punto del documento. Focus su errori, campi specifici, bottoni.

        Esempio: "Perché il tasto 'Conferma' è grigio e non cliccabile?"

    DOMANDE MULTI-HOP (Ragionamento & Procedure):

        Collegano informazioni di più parti del documento.

        Esempio: "Voglio stoccare questo materiale, ma ho bisogno di un'autorizzazione speciale, come procedo?"

    DOMANDE ONBOARDING & FLUSSI MACRO (Novizi & Creazione):

        Domande ad alto livello su come iniziare un'attività o creare nuove entità da zero.

        Focus su: "Come creo...", "Qual è il flusso per...", "Spiegazione concetti".

        Esempio: "Devo inserire una nuova UDC nel sistema per la prima volta, da dove parto?"

        Esempio: "Sono nuovo: qual è la procedura corretta per registrare un ingresso merce dall'inizio alla fine?"

        Esempio: "A cosa serve il flag 'Priorità'? Cambia qualcosa se non lo metto?"

DOCUMENTO COMPLETO:
{full_document_text}


{previous_feedback}
"""

prompt = PromptTemplate(FULL_DOC_PROMPT)


class GeneratedQuestion(BaseModel):
    user_scenario: str = Field(..., description="Breve ragionamento prima di porre la domanda, simulando il contesto dell'operatore.")
    question: str = Field(..., description="La domanda formulata in linguaggio naturale.")


class QuestionOutput(BaseModel):
    items: List[GeneratedQuestion] = Field(..., description="Lista completa delle domande generate dal documento.")


def generate_questions(text, previous_feedback=""):
    return llm.structured_predict(
        QuestionOutput,
        prompt=prompt,
        full_document_text=text,
        previous_feedback=previous_feedback,
    )


JUDGE_PROMPT = """
Sei un valutatore esperto di dataset di domande utilizzati per valutare un retriever in un sistema RAG (Retrieval-Augmented Generation).

Ti vengono forniti:
1) Un documento markdown completo
2) Una lista di domande generate a partire dal documento.

Il tuo compito è valutare l'INSIEME delle domande come set, non le singole domande in modo isolato.

Documento:
{full_document_text}

Domande generate:
{lista_domande}

Istruzioni di valutazione:

- Analizza attentamente l'insieme delle domande, ragionando step-by-step.
- Valuta in particolare i seguenti aspetti:
  • Tutte le domande sono effettivamente rispondibili usando SOLO il contenuto del documento?
  • Ci sono domande ambigue, poco specifiche o fuorvianti?
  • Ci sono ridondanze o domande che coprono lo stesso concetto?
  • Le domande coprono parti diverse e rilevanti del documento?
  • Le domande sono utili per valutare un retriever RAG (non banali, non puramente lessicali)?

- Scrivi un unico ragionamento coerente e dettagliato che giustifichi la tua valutazione complessiva.
- Il ragionamento deve spiegare come sei arrivato al verdetto finale, senza essere inutilmente prolisso.

- Dopo il ragionamento, scrivi un feedback finale in cui spieghi chiaramente:
  • cosa funziona bene nell'insieme delle domande
  • quali problemi sono presenti (domande, copertura, utilità)
  • come il modello generatore dovrebbe migliorare le domande nella prossima iterazione

- **Sii cattivo**, punta alla massima precision, basta anche solo una domanda mal formulata per invalidare l'intero set.

- SOLO ALLA FINE, dopo aver completato ragionamento e feedback, fornisci il verdetto finale.

Regola di validità:
- valid DEVE essere false se esistono problemi significativi di rispondibilità, copertura o utilità per la valutazione di un retriever.
- valid può essere true SOLO se l'insieme delle domande è già adatto, così com'è, a valutare un retriever in un sistema RAG.
"""

prompt_judge = PromptTemplate(JUDGE_PROMPT)


class JudgeEvaluation(BaseModel):
    reasoning: str = Field(..., description="Ragionamento step-by-step")
    feedback: str = Field(..., description="feedback finale, in cui spieghi se le domande vanno bene o no e perché")
    valid: bool = Field(..., description="Verdetto finale: le domande sono valide per la valutazione di un retriever in un sistema RAG?")


def judge_questions(testo_completo, lista_domande_str):
    return llm.structured_predict(
        JudgeEvaluation,
        prompt=prompt_judge,
        full_document_text=testo_completo,
        lista_domande=lista_domande_str,
    )


def genera_domande_con_judge(testo_completo, max_iter=5):
    feedback_accumulato = ""

    for i in range(max_iter):
        print(f"\n========ITERAZIONE {i+1}\n")

        domande_generate = generate_questions(
            text=testo_completo,
            previous_feedback=feedback_accumulato,
        )

        print("======== OUTPUT GENERATORE")
        print(domande_generate.model_dump_json(indent=2))

        lista_domande_str = json.dumps(
            [{"question": d.question} for d in domande_generate.items],
            ensure_ascii=False,
            indent=2,
        )

        giudizio = judge_questions(
            testo_completo=testo_completo,
            lista_domande_str=lista_domande_str,
        )

        print("======== OUTPUT JUDGE")
        print(giudizio.model_dump_json(indent=2))

        if giudizio.valid:
            return domande_generate

        if not feedback_accumulato:
            feedback_accumulato = f"""
            FEEDBACK DALL'ITERAZIONE PRECEDENTE:

            Le domande che hai generato erano:
            {lista_domande_str}

            Il judge ha valutato queste domande. Ecco il suo feedback:
            {giudizio.feedback}

            Genera un nuovo set di domande migliorato tenendo conto di questo feedback.
            """
        else:
            feedback_accumulato += f"""

            ---
            ITERAZIONE {i+1}:

            Le ultime domande che hai generato erano:
            {lista_domande_str}

            Nuovo feedback del judge:
            {giudizio.feedback}

            Continua a migliorare le domande.
            """

    return None


# --- LOOP PRINCIPALE ---
for filename in tqdm(filenames, desc="Generazione domande", unit="file"):
    try:
        res = cursor.execute(
            "SELECT chunk_index, text_content FROM document_chunks WHERE filename = ?",
            (filename,),
        ).fetchall()
        chunks = [(idx, txt) for idx, txt in res if txt and txt.strip() != ""]
        chunks.sort(key=lambda x: x[0] if x[0] is not None else -1)
    except Exception as e:
        print(f"Problemi per {filename}: {e}")
        continue

    if not chunks:
        print(f"Nessun contenuto per {filename}, saltato.")
        continue

    # Ricostruiamo il documento markdown completo, SENZA marker di chunk
    testo_completo = "NOME FILE: " + filename + "\n\n" + "\n\n".join(txt for _, txt in chunks)

    max_retries = 8
    base_delay = 5
    domande_generate = None
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            domande_generate = genera_domande_con_judge(testo_completo)
            if domande_generate:
                print(f"Generato {len(domande_generate.items)} domande per il file {filename}")
                break
            else:
                continue
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

    if not domande_generate:
        if last_error:
            print(f"Saltato {filename} dopo {max_retries} tentativi: {last_error}")
        continue

    for domanda in domande_generate.items:
        cursor_evaluation.execute(
            "INSERT INTO question_table (filename, chunk_index, question) VALUES (?, NULL, ?)",
            (filename, domanda.question),
        )

    conn_evaluation.commit()

conn_evaluation.close()
conn.close()

print(f"\nGenerazione completata! Database salvato in {evaluation_name}.db")
