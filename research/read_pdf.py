from PyPDF2 import PdfReader


def read_pdf_content_with_pypdf2(file_path: str) -> str:
    """
    Reads the text content from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content from the PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle potential None from extract_text
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
    
def read_pdf_with_unstructured(file_path: str):
    from unstructured.partition.pdf import partition_pdf
    elements = partition_pdf(filename=file_path)
    return elements

def read_pdf_with_pdfminer(file_path: str):
    from pdfminer.high_level import extract_text

    return extract_text(file_path)


if __name__=="__main__":
    file_path = "C:\\Users\\Spandan\\Downloads\\70__ATS_rating_Resume_Template.pdf"
    # content = read_pdf_content_with_pypdf2(file_path)
    # content = read_pdf_with_unstructured(file_path)
    content = read_pdf_with_pdfminer(file_path)
    x = 1