# services/scraping_service.py
from fastapi import FastAPI
from agents.scraping_agent import ScrapingAgent
from pydantic import BaseModel
from typing import List

app = FastAPI()
agent = ScrapingAgent()

class RSSRequest(BaseModel):
    url: str

class FilingRequest(BaseModel):
    ticker: str
    form: str = "10-K"
    amount: int = 1

@app.post("/rss")
def fetch_rss(req: RSSRequest):
    headlines = agent.fetch_rss_news(req.url)
    return {"headlines": headlines}

@app.post("/filings")
def get_filings(req: FilingRequest):
    files = agent.download_sec_filings(req.ticker, req.form, req.amount)
    return {"files": files}
