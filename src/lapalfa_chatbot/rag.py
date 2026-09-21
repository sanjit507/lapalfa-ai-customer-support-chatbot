from lapalfa_chatbot.retriever import search_knowledge
from lapalfa_chatbot.llm import generate_answer


def answer_question(question: str) -> str:

    results = search_knowledge(
        question,
        limit=2,
    )

    context_parts = []

    for result in results:
        content = result.payload["content"]

        context_parts.append(content)

    context = "\n\n---\n\n".join(context_parts)

    return generate_answer(
        question,
        context,
    )