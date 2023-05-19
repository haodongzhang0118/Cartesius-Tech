from langchain.document_loaders import PyPDFLoader
import PyPDF2
from io import BytesIO


def get_pdf_content(uploaded_file):
    pdf_bytes = uploaded_file.read()
    pdf = PyPDF2.PdfReader(pdf_bytes)
    content = ""
    for page in range(len(pdf.pages)):
        content += pdf.pages[page].extract_text()

    return content

def readPDF(file):
    """
    This function is used to read pdf's content and convert them to string type
    """
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    content = "Here is a personal statement used for applying for a college. "
    for i in pages:
        content += i.page_content
    return content
