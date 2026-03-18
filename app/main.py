from fastapi import FastAPI
from tasks import check_price

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "stock-price-alert"}

@app.post("/alert")
def create_alert(symbol: str, threshold: float):
    # This sends the task to Redis immediately
    check_price.delay(symbol.upper(), threshold)
    return {"message": f"Alert queued for {symbol} at ${threshold}"}
