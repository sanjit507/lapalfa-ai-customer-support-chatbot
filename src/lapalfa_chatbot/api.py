from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from lapalfa_chatbot.rag import answer_question
from lapalfa_chatbot.router import detect_intent
from lapalfa_chatbot.responses import get_response


app = FastAPI(
    title="Lapalfa Customer Support Chatbot",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {
        "message": "Lapalfa chatbot API is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    intent = detect_intent(request.message)

    # Handle normal conversation first
    if intent != "knowledge":

        answer = get_response(intent)

        return {
            "answer": answer
        }

    # Otherwise use RAG
    answer = answer_question(request.message)

    return {
        "answer": answer
    }