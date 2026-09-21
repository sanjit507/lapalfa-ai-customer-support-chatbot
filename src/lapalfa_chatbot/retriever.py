from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "lapalfa_knowledge"

QDRANT_PATH = Path(__file__).parent.parent.parent / "data" / "qdrant"

model = SentenceTransformer(MODEL_NAME)

client = QdrantClient(path=str(QDRANT_PATH))


def search_knowledge(query: str, limit: int = 3):
    query_vector = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    )

    return results.points