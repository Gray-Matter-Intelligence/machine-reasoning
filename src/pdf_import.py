import pymupdf

def importPdf_pymupdf(file_path: str) -> str:
    """
    Function to import a single PDF file and return its text content as a string
    """
    doc = pymupdf.open(file_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    doc.close()
    return full_text