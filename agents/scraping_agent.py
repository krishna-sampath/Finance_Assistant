# agents/scraping_agent.py
from sec_edgar_downloader import Downloader
import feedparser
import os

class ScrapingAgent:
    def __init__(self):
        self.dl = Downloader(company_name="MyFinanceBot", email_address="your.email@example.com")
        # Base folder where sec-edgar-downloader writes
        self.base_path = os.path.join(os.getcwd(), "sec-edgar-filings")

    def download_sec_filings(self, ticker: str, form: str = "10-K", amount: int = 1):
        # Kick off the download (return value ignored)
        self.dl.get(form, ticker)
        
        # Construct expected folder path
        filings_dir = os.path.join(self.base_path, ticker, form)
        if not os.path.isdir(filings_dir):
            raise FileNotFoundError(f"No filings folder found at {filings_dir}")

        # Gather all files under that directory
        all_files = []
        for root, _, files in os.walk(filings_dir):
            for fname in files:
                all_files.append(os.path.join(root, fname))

        # Sort by modified time, newest first
        all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return all_files[:amount]

    def fetch_rss_news(self, rss_url: str):
        feed = feedparser.parse(rss_url)
        return [(entry.title, entry.link) for entry in feed.entries]
    
# Test usage
if __name__ == "__main__":
    agent = ScrapingAgent()
    # Test RSS fetch
    news = agent.fetch_rss_news("https://finance.yahoo.com/news/rssindex")
    print("RSS Headlines:", news[:5])
    # Test SEC download
    try:
        files = agent.download_sec_filings("AAPL", form="10-K", amount=1)
        print("Downloaded filing:", files[0])
    except Exception as e:
        print("Error downloading filings:", e)
