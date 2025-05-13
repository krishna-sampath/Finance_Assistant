# services/retriever_service.py
from fastapi import FastAPI
from agents.retriever_agent import RetrieverAgent
from pydantic import BaseModel

app = FastAPI()
agent = RetrieverAgent()

class BuildRequest(BaseModel):
    texts: list[str]

class QueryRequest(BaseModel):
    query: str
    k: int = 3

@app.post("/build_index")
def build_index(req: BuildRequest):
    agent.build_vectorstore(req.texts)
    return {"status": "index_built"}

@app.post("/query")
def query(req: QueryRequest):
    docs = agent.retrieve(req.query, req.k)
    return {"results": [d.page_content for d in docs]}
