# step2_split.py
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200  # Ensures context across page/chunk boundaries isn't lost
    )
    return text_splitter.split_documents(documents)