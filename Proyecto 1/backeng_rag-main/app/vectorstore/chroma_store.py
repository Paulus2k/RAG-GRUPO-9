import chromadb


class ChromaStore:
    def __init__(self, path: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, ids, documents, metadatas, embeddings):
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def query(self, query_embedding, top_k: int = 4):
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        ids = result["ids"][0]

        items = []

        for doc_id, document, metadata, distance in zip(ids, documents, metadatas, distances):
            score = round(1 - float(distance), 4)
            items.append(
                {
                    "id": doc_id,
                    "text": document,
                    "metadata": metadata,
                    "score": score
                }
            )

        return items