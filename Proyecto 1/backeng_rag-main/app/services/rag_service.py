from app.config import settings
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore
from app.retrieval.retriever import Retriever
from app.llm.generator import OllamaGenerator


class RagService:
    def __init__(self):
        self.embedder = Embedder(settings.embedding_model)
        self.store = ChromaStore(settings.chroma_path, settings.collection_name)
        self.retriever = Retriever(self.embedder, self.store)
        self.generator = OllamaGenerator(settings.ollama_url, settings.ollama_model)

    def _build_context(self, results):
        context_parts = []

        for i, item in enumerate(results, start=1):
            source = item["metadata"].get("source", "desconocido")
            page = item["metadata"].get("page", "N/A")

            context_parts.append(
                f"[Fragmento {i} | Fuente: {source} | Página: {page}]\n{item['text']}"
            )

        return "\n\n".join(context_parts)

    def ask(self, question: str, top_k=None):
        if top_k is None:
            top_k = settings.top_k

        results = self.retriever.search(question, top_k=top_k)

        if not results:
            return {
                "respuesta": "No tengo evidencia suficiente en los documentos recuperados.",
                "fragmentos": [],
                "fuentes": []
            }

        context = self._build_context(results)

        prompt = f"""
Eres un asistente académico.
Responde únicamente con base en el contexto recuperado.
Si no encuentras evidencia suficiente, responde:
"No tengo evidencia suficiente en los documentos recuperados."

Contexto:
{context}

Pregunta:
{question}

Responde de forma clara y breve.
"""

        answer = self.generator.generate(prompt)

        return {
            "respuesta": answer,
            "fragmentos": [
                {
                    "texto": item["text"],
                    "score": item["score"]
                }
                for item in results
            ],
            "fuentes": [
                {
                    "archivo": item["metadata"].get("source"),
                    "pagina": item["metadata"].get("page"),
                    "chunk_id": item["id"]
                }
                for item in results
            ]
        }