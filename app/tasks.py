import os
from celery import Celery
import yfinance as yf

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery("tasks", broker=REDIS_URL)

@celery.task
def check_price(symbol, threshold):
    ticker = yf.Ticker(symbol)
    price = ticker.fast_info['last_price']
    print(f"Checking {symbol}: Current {round(price, 2)} vs Threshold {threshold}")
    
    if price <= threshold:
        print(f"!!! ALERT !!! {symbol} is at {price}")
    return price
