from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
from tasks import check_stock_price

app = FastAPI(title="Stock Alert Pro API")

@app.get("/")
async def root():
    return {"status": "online", "message": "Stock Alert System is Active"}

@app.post("/check-price/{ticker}")
async def trigger_price_check(ticker: str):
    """
    Endpoint to trigger a background price check.
    Returns a task_id that can be used to track the result.
    """
    # .delay() sends the work to Redis; it does NOT wait for the result.
    task = check_stock_price.delay(ticker)
    return {
        "message": "Task queued successfully",
        "task_id": task.id,
        "ticker": ticker.upper()
    }

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Check if a background task is finished and get the price.
    """
    task_result = AsyncResult(task_id)
    
    return {
        "task_id": task_id,
        "status": task_result.status, # PENDING, SUCCESS, or FAILURE
        "result": task_result.result if task_result.ready() else None
    }
