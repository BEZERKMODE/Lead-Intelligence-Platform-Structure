class EmbeddingEngine:

    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
            self.offline_fallback = False
        except Exception as e:
            print(f"[AI] SentenceTransformer not loaded ({e}). Using mock fallbacks.")
            self.offline_fallback = True

    def create_embedding(
        self,
        text
    ):
        if self.offline_fallback:
            return [0.01] * 384

        try:
            vector = self.model.encode(text)
            return vector.tolist()
        except Exception:
            return [0.01] * 384
