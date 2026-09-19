from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


class FAISSRetriever:
    MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self):
        base = Path(__file__).parent
        index_dir = base / "knowledge" / "index"

        index_path = index_dir / "knowledge.faiss"
        metadata_path = index_dir / "metadata.json"

        if not index_path.exists() or not metadata_path.exists():
            raise RuntimeError(
                "FAISS index not found. Run: python build_index.py"
            )

        self.index = faiss.read_index(str(index_path))
        self.documents = json.loads(
            metadata_path.read_text(encoding="utf-8")
        )

        self.model = SentenceTransformer(self.MODEL_NAME)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not query.strip():
            return []

        vector = self.model.encode(
            [query],
            normalize_embeddings=True,
        )

        scores, ids = self.index.search(
            vector,
            min(top_k, len(self.documents)),
        )

        results = []

        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue

            results.append({
                **self.documents[idx],
                "score": round(float(score), 4),
            })

        return results