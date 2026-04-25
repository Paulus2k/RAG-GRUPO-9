from pathlib import Path

from app.config import settings
from app.loaders.pdf_loader import load_pdf_pages
from app.processing.chunker import chunk_text
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore


def main():
    documents_dir = Path("data/documents")
    pdf_files = list(documents_dir.glob("*.pdf"))

    if not pdf_files:
        print("No se encontraron archivos PDF en data/documents")
        return

    embedder = Embedder(settings.embedding_model)
    store = ChromaStore(settings.chroma_path, settings.collection_name)

    ids = []
    texts = []
    metadatas = []

    for pdf_file in pdf_files:
        print(f"Procesando: {pdf_file.name}")
        pages = load_pdf_pages(str(pdf_file))

        for page_data in pages:
            chunks = chunk_text(
                page_data["text"],
                chunk_size=settings.chunk_size,
                overlap=settings.chunk_overlap
            )

            for chunk_index, chunk in enumerate(chunks, start=1):
                chunk_id = f"{pdf_file.stem}_p{page_data['page']}_c{chunk_index}"

                ids.append(chunk_id)
                texts.append(chunk)
                metadatas.append(
                    {
                        "source": page_data["source"],
                        "page": page_data["page"],
                        "chunk": chunk_index
                    }
                )

    print("Generando embeddings...")
    embeddings = embedder.encode_texts(texts)

    print("Guardando en Chroma...")
    store.add_documents(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Indexación finalizada. Total de chunks: {len(texts)}")


if __name__ == "__main__":
    main()