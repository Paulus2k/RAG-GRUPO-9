from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def encode_texts(self, texts):
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def encode_query(self, text: str):
        return self.model.encode(text, convert_to_numpy=True).tolist()