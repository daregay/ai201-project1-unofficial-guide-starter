import chromadb
from sentence_transformers import SentenceTransformer

from ingest import build_chunks

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "cu_boulder_guide"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def build_vector_store():
    chunks = build_chunks()
    collection = get_collection()

    existing_count = collection.count()
    if existing_count > 0:
        print(f"Collection already has {existing_count} chunks. Skipping rebuild.")
        return collection

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Stored {collection.count()} chunks in ChromaDB.")
    return collection


def retrieve(query: str, top_k: int = TOP_K):
    collection = build_vector_store()
    model = SentenceTransformer(MODEL_NAME)

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_chunks.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )

    return retrieved_chunks


if __name__ == "__main__":
    test_queries = [
        "What do students wish they knew before enrolling at CU Boulder?",
        "What transportation options are available for CU Boulder students?",
        "Where are quiet places to study on campus?",
    ]

    for query in test_queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = retrieve(query)

        for i, chunk in enumerate(results, start=1):
            print(f"\nResult {i}")
            print(f"Source: {chunk['source']}")
            print(f"Chunk index: {chunk['chunk_index']}")
            print(f"Distance: {chunk['distance']:.4f}")
            print(chunk["text"][:500])