def detect_intent(message: str) -> str:
    """
    Detect the basic intent of a customer message.
    """

    text = message.lower().strip()

    # Greetings
    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if text in greetings:
        return "greeting"

    # Thanks
    thanks = {
        "thanks",
        "thank you",
        "thankyou",
        "thx",
        "ty",
    }

    if text in thanks:
        return "thanks"

    # Human support
    support_phrases = [
        "talk to human",
        "talk to agent",
        "customer support",
        "contact support",
        "speak to someone",
        "human agent",
    ]

    if any(phrase in text for phrase in support_phrases):
        return "human_support"

    return "knowledge"