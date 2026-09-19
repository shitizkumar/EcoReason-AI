from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).parent
SOURCE_DIR = BASE / "knowledge"
INDEX_DIR = SOURCE_DIR / "index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_documents():
    documents = []

    for path in sorted(SOURCE_DIR.glob("*.txt")):
        documents.append({
            "id": path.stem,
            "text": path.read_text(encoding="utf-8"),
        })

    if not documents:
        raise RuntimeError("No knowledge documents found.")

    return documents


def main():
    documents = load_documents()

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        [doc["text"] for doc in documents],
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(
        index,
        str(INDEX_DIR / "knowledge.faiss"),
    )

    (INDEX_DIR / "metadata.json").write_text(
        json.dumps(documents, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Indexed {len(documents)} documents")
    print(f"FAISS index: {INDEX_DIR / 'knowledge.faiss'}")


if __name__ == "__main__":
    main()
