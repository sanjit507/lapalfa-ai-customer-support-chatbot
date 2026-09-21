from lapalfa_chatbot.rag import answer_question


while True:

    question = input("\nCustomer: ")

    if question.lower() in ["exit", "quit"]:
        break

    answer = answer_question(question)

    print("\nLapalfa Bot:")
    print(answer)