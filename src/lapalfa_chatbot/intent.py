import re


def detect_intent(message: str) -> str:

    text = message.lower().strip()

    # =====================================================
    # GREETING
    # =====================================================

    greetings = [
        "hi", "hello", "hey", "good morning",
        "good afternoon", "good evening", "howdy", "sup",
    ]

    if text in greetings:
        return "greeting"


    # =====================================================
    # SHIPPING
    # =====================================================

    shipping_phrases = [
        "shipping", "delivery", "ship", "deliver",
        "how long", "when will", "dispatch", "courier",
        "track", "tracking", "order status",
    ]

    for phrase in shipping_phrases:
        if phrase in text:
            return "shipping"


    # =====================================================
    # RETURNS / REFUND
    # =====================================================

    return_phrases = [
        "return", "refund", "exchange", "replace",
        "send back", "money back", "warranty", "damaged",
        "wrong item", "broken",
    ]

    for phrase in return_phrases:
        if phrase in text:
            return "returns"


    # =====================================================
    # COMPATIBILITY (battery for <model>)
    # =====================================================

    compatibility_phrases = [
        "battery for",
        "battery compatible",
        "compatible battery",
        "compatible with",
        "will this battery fit",
        "does this battery fit",
        "battery fit",
        "battery suitable",
        "suitable battery",
        "do you have a battery",
        "do you have battery",
    ]

    for phrase in compatibility_phrases:
        if phrase in text:
            return "compatibility"

    # Detect model number pattern like 15-DE0999NF / X360 14-BA etc.
    # We require a digit and letter mix with hyphens, specific brands, or attached numbers to avoid false positives like "do 16".
    if re.search(r"\b(?:(?:hp|dell|lenovo|asus|acer|macbook|sony|toshiba)[\s-]?\d{2,}[a-z0-9-]*|[a-z]+\d+[a-z0-9-]*|\d{2,}-[a-z0-9]+)\b", text):
        return "compatibility"

    # =====================================================
    # ASK MODEL (Generic battery inquiry)
    # =====================================================
    
    generic_inquiries = [
        "do you have laptop batteries",
        "do you have laptop batteries?",
        "laptop battery",
        "need laptop battery",
        "battery for laptop",
        "do you sell batteries",
        "battery",
        "batteries"
    ]
    if text in generic_inquiries:
        return "ask_model"



    # =====================================================
    # PRODUCT SEARCH
    # =====================================================

    product_keywords = [
        # batteries
        "battery", "batteries",
        # laptop parts / accessories
        "laptop", "charger", "adapter", "cable", "screen", "display",
        "keyboard", "ram", "ssd", "storage", "hard disk", "hard drive",
        "memory", "upgrade", "part", "parts", "accessory", "accessories",
        "hp", "dell", "lenovo", "asus", "acer", "samsung", "toshiba",
        "sony", "msi", "lg", "apple", "macbook",
        # shopping intent
        "product", "price", "sku", "available", "in stock", "stock",
        "buy", "purchase", "order", "want", "need", "looking for",
        "do you have", "do you sell", "can i get", "show me",
        "list", "catalog",
    ]

    for keyword in product_keywords:
        if keyword in text:
            return "product"


    # =====================================================
    # DEFAULT → Human Handover
    # (We NEVER hallucinate — if we don't know the intent, hand over)
    # =====================================================

    return "handover"