from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import requests
import shutil
import os
import uuid
import tempfile
import pandas as pd

app = FastAPI()

API_URL    = os.getenv("API_URL",    "http://localhost:8001")
SCRAPE_URL = os.getenv("SCRAPE_URL", "http://localhost:8002")
RETR_URL   = os.getenv("RETR_URL",   "http://localhost:8003")
LANG_URL   = os.getenv("LANG_URL",   "http://localhost:8004")
VOICE_URL  = os.getenv("VOICE_URL",  "http://localhost:8005")

@app.post("/run_brief")
async def run_brief(audio: UploadFile = File(...)):
    # 1. Save incoming audio
    tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1])
    with open(tmp_in.name, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    # 2. Transcribe
    r1 = requests.post(
        f"{VOICE_URL}/transcribe", files={"audio": open(tmp_in.name, "rb")}
    )
    if r1.status_code != 200:
        raise HTTPException(status_code=500, detail="Transcription failed")
    question = r1.json()["text"]
    print("QUESTION:", question)

    # 3. Fetch stock data
    stock_resp = requests.post(
        f"{API_URL}/stock_data", json={"ticker": "AAPL", "period": "2d", "interval": "1d"}
    )
    stock_resp.raise_for_status()
    stock_records = stock_resp.json()["data"]
    df_stock = pd.DataFrame(stock_records)
    # compute change
    if len(df_stock) >= 2:
        latest = df_stock.iloc[-1]["Close"]
        prev   = df_stock.iloc[-2]["Close"]
        pct_chg = (latest - prev) / prev * 100
        stock_summary = f"AAPL closed at ${latest:.2f}, {pct_chg:+.2f}% vs. prior day."
    else:
        stock_summary = "AAPL data insufficient for daily change."
    print("STOCK SUMMARY:", stock_summary)

    # 4. Fetch headlines
    news_resp = requests.post(
        f"{SCRAPE_URL}/rss", json={"url": "https://finance.yahoo.com/news/rssindex"}
    )
    news_resp.raise_for_status()
    headlines = news_resp.json()["headlines"][:5]
    headlines_text = "\n".join([f"- {t}" for t, _ in headlines])

    # 5. Build retrieval context
    context_pieces = [stock_summary, headlines_text]
    build_resp = requests.post(
        f"{RETR_URL}/build_index", json={"texts": context_pieces}
    )
    build_resp.raise_for_status()

    query_resp = requests.post(
        f"{RETR_URL}/query", json={"query": question, "k": 3}
    )
    query_resp.raise_for_status()
    docs = query_resp.json().get("results", [])
    print("DOCS RETRIEVED:", docs)
    combined_text = "\n".join(docs)

    # 6. Summarize
    summary_resp = requests.post(
        f"{LANG_URL}/summarize", json={"text": combined_text}
    )
    summary_resp.raise_for_status()
    summary = summary_resp.json().get("summary", "No summary generated.")
    print("SUMMARY:", summary)

    # 7. Text-to-speech
    tts_resp = requests.post(
        f"{VOICE_URL}/speak", json={"text": summary}, stream=True
    )
    tts_resp.raise_for_status()

    return StreamingResponse(tts_resp.raw, media_type="audio/wav")