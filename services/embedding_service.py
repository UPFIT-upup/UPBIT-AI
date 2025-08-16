from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    JSONLoader,
    UnstructuredFileLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def embed_file(file_path: str, index_path: str) -> int:
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        loader = PyPDFLoader(file_path)
    elif ext == "txt":
        loader = TextLoader(file_path)
    elif ext == "html":
        loader = UnstructuredHTMLLoader(file_path)
    elif ext == "json":
        loader = JSONLoader(file_path)
    elif ext in ["docx", "xlsx", "pptx"]:
        loader = UnstructuredFileLoader(file_path)
    else:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {ext}")

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)

    return len(chunks)
