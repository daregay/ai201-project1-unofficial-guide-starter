from pathlib import Path
import re

DOCUMENTS_DIR = Path("documents")
CHUNK_SIZE = 700
OVERLAP = 120
MIN_CHUNK_LENGTH = 100


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.lower() in {"skip to content", "menu", "search", "home"}:
            continue
        lines.append(line)

    return "\n".join(lines)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) >= MIN_CHUNK_LENGTH:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def load_documents() -> list[dict]:
    docs = []

    for path in DOCUMENTS_DIR.glob("*.txt"):
        raw_text = path.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)

        docs.append({
            "source": path.name,
            "text": cleaned
        })

    return docs


def build_chunks() -> list[dict]:
    all_chunks = []

    for doc in load_documents():
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "id": f"{doc['source']}_{i}",
                "source": doc["source"],
                "chunk_index": i,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()

    print(f"Loaded {len(load_documents())} documents")
    print(f"Created {len(chunks)} chunks\n")

    for chunk in chunks[:5]:
        print("=" * 80)
        print(f"Source: {chunk['source']}")
        print(f"Chunk index: {chunk['chunk_index']}")
        print(chunk["text"][:700])
        print()