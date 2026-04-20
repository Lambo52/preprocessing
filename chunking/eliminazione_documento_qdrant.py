import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

collectionname = "WAMASRAGOVERLAP"
nome_documento = "Creazione_nuove_udc.pdf"   # <-- il valore di origin_filename

client = QdrantClient(url=os.getenv("QDRANT_URL"))

# conteggio preventivo di quanti chunk verranno eliminati
count_result = client.count(
    collection_name=collectionname,
    count_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="origin_filename",
                match=models.MatchValue(value=nome_documento),
            )
        ]
    ),
    exact=True,
)
print(f"Trovati {count_result.count} chunk per '{nome_documento}'")

# delete vero e proprio
client.delete(
    collection_name=collectionname,
    points_selector=models.FilterSelector(
        filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="origin_filename",
                    match=models.MatchValue(value=nome_documento),
                )
            ]
        )
    ),
)
print(f"Eliminati chunk di '{nome_documento}' da {collectionname}")
