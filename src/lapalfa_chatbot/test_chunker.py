from lapalfa_chatbot.knowledge_loader import load_knowledge
from lapalfa_chatbot.chunker import create_chunks


documents = load_knowledge()

chunks = create_chunks(documents)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")

for chunk in chunks[:10]:
    print("\n" + "=" * 70)
    print("FILE:", chunk["filename"])
    print("CHUNK:", chunk["chunk_id"])
    print("=" * 70)
    print(chunk["content"])