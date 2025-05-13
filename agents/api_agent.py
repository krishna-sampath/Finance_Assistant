# agents/api_agent.py
import yfinance as yf

class APIAgent:
    def get_stock_data(self, ticker: str, period: str = "1d", interval: str = "1h"):
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)
        return data

# Example usage
if __name__ == "__main__":
    agent = APIAgent()
    df = agent.get_stock_data("TSLA", "5d", "1d")
    print(df)
