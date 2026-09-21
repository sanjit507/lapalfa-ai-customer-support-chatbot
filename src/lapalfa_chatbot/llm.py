from ollama import chat


MODEL_NAME = "gemma3:1b"

SYSTEM_PROMPT = """
You are Lapalfa's customer support assistant.

Answer the customer's question using ONLY the supplied context.

STRICT RULES:

- Give the answer directly.
- Use complete, grammatically correct sentences.
- Never combine two separate facts into one incorrect sentence.
- Never change numbers, prices, dates, or ranges.
- Never invent information.
- If the context contains duplicate information, mention it only once.
- Do not repeat the question.
- Do not mention RAG, context, embeddings, Qdrant, or internal systems.
- If the answer is not clearly available in the context, say:
  "I don't have enough information to answer that. Please contact
  Lapalfa support at +91 9472937493."

For numerical or policy questions, prefer a short bullet list.

Example:

Question:
How much does shipping cost?

Context:
Free shipping on orders of ₹599 or more.
Orders below ₹599 have a shipping charge of ₹60–₹150.

Correct answer:
- Orders of ₹599 or more: Free shipping.
- Orders below ₹599: ₹60–₹150 shipping charge.
"""


def generate_answer(question: str, context: str) -> str:

    prompt = f"""Context:{context} Customer question: {question} Answer the customer using only the context above."""
    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.message.content