from llama_index.core import VectorStoreIndex, StorageContext, Settings, SimpleDirectoryReader, SummaryIndex
from dotenv import load_dotenv
from docling.datamodel.document import DoclingDocument
from llama_index.llms.openai_like import OpenAILike


load_dotenv()

# qua fatto porcata per importare utils da altro file
__all__ = [
    "iniezionetagimmagini",
    "metadata_extraction",
    "riassuntodocumento",
]

# INSERIMENTO TAG IMMAGINE
def iniezionetagimmagini(doc: DoclingDocument) -> DoclingDocument:
    for i in range(0,len(doc.pictures)):
        if doc.pictures[i].meta:
            doc.pictures[i].meta.description.text = "[IMAGE] " + doc.pictures[i].meta.description.text + " [/IMAGE]"
    return doc

# ESTRAZIONE METADATI CHUNK
def metadata_extraction(chunk):
    meta_dict = chunk.meta.export_json_dict()

    pages = list({
        prov["page_no"]
        for item in meta_dict["doc_items"]
        for prov in item["prov"]
    })

    origin = meta_dict.get("origin", {})

    gruppi = origin.get("filename").split("_")[0]

    gruppi = gruppi.split("-") if "-" in gruppi else [gruppi]

    clean_meta = {
        "pages": pages,
        "origin_filename": origin.get("filename"),
        "origin_mimetype": origin.get("mimetype"),
        "groups": gruppi,
    }
    return clean_meta

# RIASSUNTO DOCUMENTO INTERO
def riassuntodocumento(file_path):    
    llm = OpenAILike(
        model="Qwen/Qwen2.5-32B-Instruct-AWQ",
        api_base="http://10.1.2.98/v1", 
        api_key="fake-key",                 
        is_chat_model=True,
        is_function_calling_model=True,
        timeout=600.0,
        temperature=0,
        context_window=8192                       
    )


    Settings.llm = llm

    def process_document_with_summary(file_path):
        print(f"Caricamento di: {file_path}...")
        
        
        loader = SimpleDirectoryReader(input_files=[file_path])
        documents = loader.load_data()
        

        doc = documents[0] 
        
        print("Generazione della descrizione breve (questo potrebbe richiedere tempo)...")
        
        summary_index = SummaryIndex.from_documents([doc])
        
        query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize"
        )
        
        
        prompt = (
            "Analizza l'intero documento e fornisci una descrizione molto breve "
            "(massimo 2 frasi) che riassuma l'argomento principale e lo scopo del file. "
            "Rispondi solo con la descrizione."
        )
        
        summary_response = query_engine.query(prompt)
        short_description = str(summary_response).strip()
        
        print(f"Descrizione generata: {short_description}")
        
        doc.metadata["document_summary"] = short_description

        #print(doc.text[:20000])
        
        
        return doc

    # --- ESECUZIONE ---


    documento_aggiornato = process_document_with_summary(file_path)

    return documento_aggiornato.metadata["document_summary"]

