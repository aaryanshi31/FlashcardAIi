def extract_text(uploaded_file) -> str:
    """Extract plain text from uploaded .txt or .pdf files."""
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return _read_txt(uploaded_file)
    elif name.endswith(".pdf"):
        return _read_pdf(uploaded_file)
    return ""


def _read_txt(file) -> str:
    try:
        raw = file.read()
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1", errors="replace")
    except Exception:
        return ""


def _read_pdf(file) -> str:
    try:
        import fitz
        data = file.read()
        doc = fitz.open(stream=data, filetype="pdf")
        pages = [doc[i].get_text("text") for i in range(len(doc))]
        doc.close()
        return "\n\n".join(p for p in pages if p.strip())
    except ImportError:
        return _read_pdf_fallback(file)
    except Exception:
        return ""


def _read_pdf_fallback(file) -> str:
    try:
        from pypdf import PdfReader
        file.seek(0)
        reader = PdfReader(file)
        return "\n\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception:
        return ""
