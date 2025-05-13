# Finance Assistant

A multi-agent, multi-source finance assistant that delivers spoken market briefs via a Streamlit app. Built with modular microservices, Retrieval-Augmented Generation (RAG), and open-source voice toolkits, it gives you up-to-the-minute portfolio insights and earnings highlights—at the sound of your voice.

---

## 🔍 Project Overview

This system polls live market data, scrapes company filings, runs quantitative analysis, and uses LLM-powered RAG to generate human-readable narratives—all orchestrated via FastAPI microservices. At 8 AM each trading day, simply ask:
> “What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?”

…and hear back:
> “Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt due to rising yields.”

---

## 🛠️ Tech Stack

- **Data & APIs**:  
  - Yahoo Finance / AlphaVantage API Agent  
  - Python scraping loaders for SEC filings  
- **Indexing & Retrieval**:  
  - FAISS (or Pinecone) vector store  
  - Custom Retriever Agent  
- **Language & RAG**:  
  - LangChain (or alternative) + OpenAI/Open-source LLMs  
  - Analysis Agent for allocation & surprise calculations  
- **Voice I/O**:  
  - Whisper (STT)  
  - Coqui TTS (or comparable)  
  - Voice Agent microservice  
- **Orchestration**:  
  - FastAPI microservices for each agent  
  - Central orchestrator handles routing & fallbacks  
- **Frontend**:  
  - Streamlit app for text & voice UI  
- **Containerization**:  
  - Docker & Docker Compose  
- **Deployment**:  
  - Streamlit Cloud (or any Docker-compatible host)  

---

Sure! Here's your updated repository structure formatted correctly in Markdown — ready to paste into your README:

## 📂 Repository Structure

```

Finance\_Assistant/
│
├─ agents/                      # Agents
│   ├─ api\_agent/
│   ├─ scraping\_agent/
│   ├─ retrieving\_agent/
│   ├─ language\_agent/
│   └─ voice\_agent/
│
├─ services/                    # FastAPI microservices handled by orchestrator
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ api\_service/
│   ├─ scraping\_service/
│   ├─ retrieving\_service/
│   ├─ language\_service/
│   ├─ voice\_service/
│   └─ orchestrator\_service/
│
├─ streamlit\_app/               # Frontend UI (app.py + requirements)
│
├─ docker-compose.yml
│
└─ README.md                    # ← You are here

```
---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/krishna-sampath/Finance_Assistant.git
cd Finance_Assistant
````

### 2. Build & Start All Services with Docker Compose

From the project root:

```bash
docker-compose build
docker-compose up -d
```

This will build and launch all FastAPI agents, the orchestrator, and the Streamlit frontend in containers.

### 3. Run the Streamlit App

```bash
cd streamlit_app
streamlit run app.py
```

### 4. Open in Browser

Navigate to:

```
http://localhost:8501
```

…and you’re live! Speak or type your query, and hear your personalized market brief.

---

## 🎯 Features

* **Real-time Market Data**: Live quotes, historical time series, and allocation metrics.
* **Earnings Surprise Detection**: Auto-scrapes and computes beat/miss percentages.
* **RAG-Powered Narratives**: LLM synthesizes coherent market narratives.
* **Voice-First Interface**: From Whisper STT to Coqui TTS for end-to-end spoken briefings.
* **Modular Microservices**: Swap in your favorite APIs, vector stores, or LLM frameworks.

---

> **Note**: Make sure Docker is installed on your system. If you hit any issues, consult the service logs via `docker-compose logs --follow`. Enjoy your spoken market brief!
