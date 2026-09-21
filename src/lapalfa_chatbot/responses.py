def get_response(intent: str) -> str | None:

    responses = {

        "greeting":
            "Hello! 👋 Welcome to Lapalfa Support. "
            "How can I help you today?",

        "thanks":
            "You're welcome! 😊 "
            "Let me know if you need anything else.",

        "human_support":
            "Sure. You can contact our support team at "
            "+91 9472937493 or email support@lapalfa.com.",

    }

    return responses.get(intent)