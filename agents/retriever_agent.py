# agents/retriever_agent.py
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

class RetrieverAgent:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings()
        self.vectorstore = None

    def build_vectorstore(self, texts: list[str]):
        docs = [Document(page_content=txt) for txt in texts]
        self.vectorstore = FAISS.from_documents(docs, self.embedding_model)

    def retrieve(self, query: str, k: int = 3):
        return self.vectorstore.similarity_search(query, k=k)

# Example usage
if __name__ == "__main__":
    agent = RetrieverAgent()
    agent.build_vectorstore(["Apple is a tech giant.", "Tesla focuses on electric cars."])
    results = agent.retrieve("electric cars")
    for res in results:
        print(res.page_content)
