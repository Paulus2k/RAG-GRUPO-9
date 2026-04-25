from pathlib import Path
from pypdf import PdfReader


def load_pdf_pages(pdf_path: str):
    pdf_file = Path(pdf_path)
    reader = PdfReader(str(pdf_file))

    pages = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        if text:
            pages.append(
                {
                    "source": pdf_file.name,
                    "page": i,
                    "text": text
                }
            )

    return pages