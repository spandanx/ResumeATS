from pdfminer.high_level import extract_text

class PDFContentReader:
    def read_pdf_with_pdfminer(self, file_path: str):
        return extract_text(file_path)


if __name__ == "__main__":
    file_path = "C:\\Users\\Spandan\\Downloads\\70__ATS_rating_Resume_Template.pdf"
    pdfContentReader = PDFContentReader()
    # content_pypdf = read_pdf_content_with_pypdf2(file_path)
    # content_unstr = read_pdf_with_unstructured(file_path)
    content_pdfminer = pdfReader.read_pdf_with_pdfminer(file_path)
    x = 1