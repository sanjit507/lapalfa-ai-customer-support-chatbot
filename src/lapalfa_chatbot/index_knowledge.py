from lapalfa_chatbot.knowledge_loader import load_knowledge
from lapalfa_chatbot.chunker import create_chunks
from lapalfa_chatbot.vector_store import (
    create_collection,
    store_chunks,
)


print("Loading knowledge...")

documents = load_knowledge()

print(f"Documents loaded: {len(documents)}")


print("Creating chunks...")

chunks = create_chunks(documents)

print(f"Chunks created: {len(chunks)}")


print("Creating Qdrant collection...")

create_collection()


print("Creating embeddings and storing vectors...")

stored = store_chunks(chunks)

print(f"Stored {stored} vectors successfully.")

print("Knowledge indexing completed.")