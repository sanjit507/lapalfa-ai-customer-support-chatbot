from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

QDRANT_PATH = Path(__file__).parent.parent.parent / "data" / "qdrant"


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "lapalfa_knowledge"


# Load embedding model
model = SentenceTransformer(MODEL_NAME)


# Local Qdrant database
client = QdrantClient(path=str(QDRANT_PATH))


def create_collection():
    # Remove old collection if it exists
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=Distance.COSINE,
        ),
    )


def store_chunks(chunks):
    points = []

    texts = [chunk["content"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
    )

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        points.append(
            PointStruct(
                id=index,
                vector=embedding.tolist(),
                payload={
                    "filename": chunk["filename"],
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"],
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return len(points)