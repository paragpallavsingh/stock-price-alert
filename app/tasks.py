import os
import yfinance as yf
import requests
from celery import Celery

# 1. Setup Celery to use your Redis container as the "Post Office"
# In Docker Compose, the hostname 'redis' is automatically resolved
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("stock_tasks", broker=redis_url, backend=redis_url)

@celery_app.task(name="tasks.check_stock_price")
def check_stock_price(ticker: str):
    """
    Fetches the latest stock price. 
    Uses Alpha Vantage if API key is present, otherwise falls back to yfinance.
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    ticker = ticker.upper()
    
    try:
        if api_key and api_key != "your_key_here":
            # Professional Method: Alpha Vantage
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}'
            r = requests.get(url, timeout=10)
            data = r.json()
            
            # Alpha Vantage returns '05. price' inside 'Global Quote'
            quote = data.get("Global Quote", {})
            price = quote.get("05. price")
            source = "AlphaVantage"
        else:
            # Fallback Method: yfinance (Scraping)
            stock = yf.Ticker(ticker)
            # fast_info is efficient for just the price
            price = stock.fast_info['last_price']
            source = "yfinance"

        if price is None:
            return {"error": f"Could not find price for {ticker}", "source": source}

        return {
            "ticker": ticker, 
            "price": round(float(price), 2), 
            "source": source,
            "status": "success"
        }

    except Exception as e:
        return {"error": str(e), "status": "failure"}
