class Retriever:
    def __init__(self, embedder, store):
        self.embedder = embedder
        self.store = store

    def search(self, question: str, top_k: int = 4):
        query_embedding = self.embedder.encode_query(question)
        return self.store.query(query_embedding, top_k=top_k)