from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "data" / "knowledge"


def load_knowledge():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        content = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            {
                "filename": file_path.name,
                "content": content,
            }
        )

    return documents