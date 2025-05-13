# services/api_service.py
from fastapi import FastAPI
from agents.api_agent import APIAgent
from pydantic import BaseModel

app = FastAPI()
agent = APIAgent()

class StockRequest(BaseModel):
    ticker: str
    period: str = "1d"
    interval: str = "1h"

@app.post("/stock_data")
def get_stock_data(req: StockRequest):
    df = agent.get_stock_data(req.ticker, req.period, req.interval)
    # return JSON-serializable dict
    return {"data": df.reset_index().to_dict(orient="records")}
