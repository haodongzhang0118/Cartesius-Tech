from langchain.document_loaders import PyPDFLoader

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
