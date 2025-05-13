# services/language_service.py
from fastapi import FastAPI
from agents.language_agent import LanguageAgent
from pydantic import BaseModel

app = FastAPI()
agent = LanguageAgent()

class SummarizeRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(req: SummarizeRequest):
    summary = agent.generate_summary(req.text)
    return {"summary": summary}
