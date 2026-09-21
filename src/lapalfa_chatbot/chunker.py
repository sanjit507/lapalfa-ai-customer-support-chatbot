from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            " ",
            "",
        ],
    )

    chunks = []

    for document in documents:
        split_texts = splitter.split_text(
            document["content"]
        )

        for index, text in enumerate(split_texts):
            chunks.append(
                {
                    "filename": document["filename"],
                    "chunk_id": index,
                    "content": text,
                }
            )

    return chunks