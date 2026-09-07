import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from every page of a PDF.
    Returns a list of dicts: [{"page": 1, "text": "..."}, ...]
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append({
                    "page": i + 1,
                    "text": text.strip()
                })
    return pages
