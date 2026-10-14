from pathlib import Path

import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


class RAGKnowledgeBase:

    def __init__(
        self,
        kb_dir="knowledge_base"
    ):

        self.kb_dir = Path(kb_dir)

        self.kb_dir.mkdir(
            exist_ok=True
        )

        # Embedding model
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.documents = []
        self.index = None

        self._load_documents()

    # -----------------------------------------
    # LOAD DOCUMENTS
    # -----------------------------------------

    def _load_documents(self):

        self.documents = []

        for path in sorted(
            self.kb_dir.glob("*.txt")
        ):

            text = path.read_text(
                encoding="utf-8"
            )

            chunks = self._chunk_text(
                text
            )

            for i, chunk in enumerate(chunks):

                self.documents.append(
                    {
                        "source": path.name,
                        "chunk": i,
                        "text": chunk
                    }
                )

        if not self.documents:
            return

        # Create embeddings
        embeddings = self.model.encode(
            [
                document["text"]
                for document in self.documents
            ],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        # FAISS index
        self.index = faiss.IndexFlatIP(
            embeddings.shape[1]
        )

        self.index.add(embeddings)

    # -----------------------------------------
    # TEXT CHUNKING
    # -----------------------------------------

    @staticmethod
    def _chunk_text(
        text,
        chunk_size=700
    ):

        words = text.split()

        chunks = []

        for i in range(
            0,
            len(words),
            chunk_size
        ):

            chunks.append(
                " ".join(
                    words[
                        i:i + chunk_size
                    ]
                )
            )

        return chunks

    # -----------------------------------------
    # SEARCH
    # -----------------------------------------

    def search(
        self,
        query,
        top_k=4
    ):

        if self.index is None:
            return []

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            min(
                top_k,
                len(self.documents)
            )
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue

            item = dict(
                self.documents[index]
            )

            item["score"] = float(score)

            results.append(item)

        return results