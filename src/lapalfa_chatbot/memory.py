import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv(override=True)

CHATSORTER_API_URL = os.getenv("CHATSORTER_API_URL", "https://api.chatsorter.com")
API_KEY = os.getenv("CHATSORTER_API_KEY", "")


def get_memories_and_store(chat_id: str, message: str) -> List[Dict[str, Any]]:
    """
    Stores the user's message and retrieves relevant memories in a single call.
    Uses ChatSorter's /sdk/v1 endpoint.
    """
    api_key = os.getenv("CHATSORTER_API_KEY", API_KEY)
    if not api_key or api_key == "your_key_here":
        print("[ChatSorter] ⚠️ CHATSORTER_API_KEY not configured in .env")
        return []

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        print(f"[ChatSorter] 📤 Calling API | chat_id='{chat_id}' | message='{message}'")

        response = requests.post(
            f"{CHATSORTER_API_URL}/sdk/v1",
            headers=headers,
            json={
                "chat_id": chat_id,
                "message": message,
                "retrieve_memories": True,
            },
            timeout=5,
        )

        print(f"[ChatSorter] 📥 Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            memories = data.get("memories", [])
            print(f"[ChatSorter] ✅ Success! Stored message. Retrieved {len(memories)} memories.")
            if memories:
                print(f"[ChatSorter] 🧠 Memories: {memories}")
            return memories
        else:
            print(f"[ChatSorter] ❌ API error ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"[ChatSorter] ❌ Network error: {e}")

    return []


def format_memories_for_prompt(memories: List[Dict[str, Any]]) -> str:
    """Format memory items as context string for LLM or prompts."""
    if not memories:
        return ""

    lines = []
    for m in memories:
        summary = m.get("summary") or m.get("text") or ""
        score = m.get("score", 1.0)
        if summary and score >= 0.5:
            lines.append(f"- {summary}")

    if not lines:
        return ""

    return "User Profile & Past Memories:\n" + "\n".join(lines)
