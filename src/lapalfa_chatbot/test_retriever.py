from lapalfa_chatbot.retriever import search_knowledge


query = input("Ask a question: ")

results = search_knowledge(query)

print("\nRESULTS:\n")

for result in results:
    print("=" * 70)
    print("FILE:", result.payload["filename"])
    print("SCORE:", result.score)
    print("=" * 70)
    print(result.payload["content"])
    print()