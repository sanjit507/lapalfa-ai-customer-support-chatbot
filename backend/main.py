from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from lapalfa_chatbot.intent import detect_intent
from lapalfa_chatbot.product_service import search_product_for_chat, check_compatibility


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Lapalfa Customer Support Chatbot",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# CONTACT DETAILS  (change here to update everywhere)
# =========================================================

WHATSAPP_NUMBER = "919472937493"   # country code + number, no +
SUPPORT_PHONE   = "+91 94729 37493"
WHATSAPP_LINK   = f"https://wa.me/{WHATSAPP_NUMBER}"


# =========================================================
# REQUEST / RESPONSE MODELS
# =========================================================

class ChatRequest(BaseModel):
    message: str


class ProductResponse(BaseModel):
    title: str
    price: Optional[float] = None
    comparePrice: Optional[float] = None
    sku: Optional[str] = None
    imageUrl: Optional[str] = None
    productUrl: Optional[str] = None
    inStock: bool = False


class ChatResponse(BaseModel):
    answer: str
    type: str = "text"           # "text" | "product" | "handover"
    products: list[ProductResponse] = []
    whatsappLink: Optional[str] = None


# =========================================================
# HELPERS
# =========================================================

def make_product_data(products: list) -> list[ProductResponse]:
    return [
        ProductResponse(
            title=p.get("title", "Product"),
            price=p.get("price"),
            comparePrice=p.get("comparePrice"),
            sku=p.get("sku"),
            imageUrl=p.get("imageUrl"),
            productUrl=p.get("productUrl"),
            inStock=p.get("inStock", False),
        )
        for p in products
    ]


def handover_response(reason: str = "") -> ChatResponse:
    """
    Returns a human-handover response.
    Never provides wrong/invented information.
    """
    msg = (
        "I wasn't able to find what you're looking for in our catalog.\n\n"
        "🙋 **Our team is here to help!**\n"
        "Chat with a real agent on WhatsApp — they can check availability, "
        "confirm compatibility, and place orders for you.\n\n"
        f"📞 **{SUPPORT_PHONE}**"
    )
    return ChatResponse(
        type="handover",
        answer=msg,
        products=[],
        whatsappLink=WHATSAPP_LINK,
    )


def canned_responses() -> dict:
    return {

        "greeting": (
            "Hello! 👋 Welcome to **Lapalfa Support**.\n\n"
            "I can help you with:\n"
            "• 🔋 **Battery compatibility** – e.g. \"Battery for HP 15-DE0999NF\"\n"
            "• 🚚 **Shipping & delivery** timelines\n"
            "• ↩️ **Returns & refunds**\n"
            "• 🔍 **Product search** – prices, availability, links\n\n"
            "What can I help you with today?"
        ),

        "shipping": (
            "🚚 **Shipping & Delivery**\n\n"
            "• **Standard Delivery:** 3–7 business days across India\n"
            "• **Express Delivery:** 1–2 business days (select cities)\n"
            "• **Free shipping** on orders above ₹999\n"
            "• A tracking link is sent via SMS/email after dispatch.\n\n"
            "Need help with a specific order? Share your **order ID** and I'll assist."
        ),

        "returns": (
            "↩️ **Returns & Refund Policy**\n\n"
            "• **7-day return window** from delivery date\n"
            "• Item must be unused and in original packaging\n"
            "• Refunds processed within **5–7 business days**\n"
            "• Defective or wrong items replaced **free of charge**\n\n"
            "To start a return, share your **order ID** and reason."
        ),

    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Lapalfa chatbot API is running"}


# =========================================================
# CHAT API
# =========================================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    message = request.message.strip()
    intent  = detect_intent(message)

    responses = canned_responses()


    # =====================================================
    # GREETING / SHIPPING / RETURNS  — safe canned answers
    # =====================================================

    if intent in responses:
        return ChatResponse(
            type="text",
            answer=responses[intent],
            products=[],
        )

    # =====================================================
    # ASK FOR MODEL (Generic battery query)
    # =====================================================
    if intent == "ask_model":
        return ChatResponse(
            type="text",
            answer="Sure! Please provide your **laptop model number** (e.g., HP 15-DE0999NF) so I can find the exact battery or part for you.",
            products=[],
        )


    # =====================================================
    # COMPATIBILITY SEARCH  — battery for <laptop model>
    # =====================================================

    if intent == "compatibility":

        products = check_compatibility(message)

        if products:
            return ChatResponse(
                type="product",
                answer="🔋 Here are the compatible batteries I found for your laptop:",
                products=make_product_data(products),
            )

        # Not found → hand over to human, do NOT invent an answer
        return ChatResponse(
            type="handover",
            answer=(
                "I couldn't find a battery for that model in our current catalog.\n\n"
                "🙋 **Our team can help!**\n"
                "They have access to our full inventory and can confirm "
                "compatibility for your exact model.\n\n"
                f"📞 **{SUPPORT_PHONE}**"
            ),
            products=[],
            whatsappLink=WHATSAPP_LINK,
        )


    # =====================================================
    # PRODUCT SEARCH  — general product queries
    # =====================================================

    if intent == "product":

        products = search_product_for_chat(message)

        if products:
            return ChatResponse(
                type="product",
                answer="✅ Here are the products I found for you:",
                products=make_product_data(products),
            )

        # Not found → hand over, never guess
        return ChatResponse(
            type="handover",
            answer=(
                "I searched our catalog but couldn't find a matching product.\n\n"
                "🙋 **Talk to our team on WhatsApp** — they can check "
                "availability and help you place an order.\n\n"
                f"📞 **{SUPPORT_PHONE}**"
            ),
            products=[],
            whatsappLink=WHATSAPP_LINK,
        )


    # =====================================================
    # HANDOVER  — anything else we don't recognise
    # We NEVER call the LLM/RAG here to avoid wrong answers.
    # =====================================================

    return handover_response()


# =========================================================
# SERVE FRONTEND (index.html, style.css, script.js)
# =========================================================

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")