from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def generate_task(question: str, index_path: str) -> str:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4")  # OpenAI API 키 환경변수 설정 필요

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa.run(question)
    return result
