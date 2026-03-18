import os
import yfinance as yf
import requests
from celery import Celery

# 1. Setup Celery (Connect to your Redis container)
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("stock_tasks", broker=redis_url, backend=redis_url)

@app.task
def check_stock_price(ticker):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if api_key:
        # Professional Method: Alpha Vantage
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        price = data.get("Global Quote", {}).get("05. price")
        source = "AlphaVantage"
    else:
        # Fallback Method: yfinance (Scraping)
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        source = "yfinance"

    return {"ticker": ticker, "price": price, "source": source}
