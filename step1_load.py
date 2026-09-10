from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} document pages.")
    return documents