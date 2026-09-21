from lapalfa_chatbot.knowledge_loader import load_knowledge


documents = load_knowledge()

print(f"Loaded documents: {len(documents)}")

for document in documents:
    print("\n" + "=" * 60)
    print("FILE:", document["filename"])
    print("=" * 60)
    print(document["content"][:500])