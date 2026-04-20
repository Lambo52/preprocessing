import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("RERANKER_API_URL")

def reranka(nodes, query_text, top_n=5):

    top_n = min(top_n, len(nodes))

    nodinuovi = []

    noditesto = [n.node.get_content() for n in nodes]
    # PER DEBUG
    #noditesto = nodes

    payload = {
        "model": "BAAI/bge-reranker-v2-m3",
        "query": f"{query_text}",
        "documents": noditesto,
        "top_n": top_n
    }

    headers = {
        "Content-Type": "application/json"
         
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        results = response.json()
        #print(results)
           
        
        for i in range(len(results["results"])):

            nodinuovi.append(nodes[results["results"][i]["index"]])

    except Exception as e:
        print(f"Errore: {e}")

    return nodinuovi

if __name__ == "__main__":
    reranka(["""3.4. Incongruenza logica tra WAMAS e Lighthouse\\nPuò  verificarsi  la  situazione  in  cui  su  WAMAS  vedo  un  UDC  in  una  certa  locazione  che  però  su Lighthouse non viene visto. Questo causa un disallineamento dei sistemi a gestire.\\nPer ovviare a questo problema bisogna selezionare l'opzione 'Forza' e poi refresh e reset per forza il sistema a rilevare l'UDC e sistemare la questione."""], "ho un disallineamento fisico logico di un pallet, come posso risolvere?")
