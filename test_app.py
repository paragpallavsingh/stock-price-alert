import requests
import time

BASE_URL = "http://localhost:8000"
TICKER = "AAPL"

def run_test():
    print(f"🚀 Triggering price check for {TICKER}...")
    # 1. Trigger the task
    resp = requests.post(f"{BASE_URL}/check-price/{TICKER}")
    task_id = resp.json()["task_id"]
    print(f"✅ Task queued! ID: {task_id}")

    # 2. Poll for the result
    print("⏳ Waiting for worker to process...")
    for _ in range(10):
        status_resp = requests.get(f"{BASE_URL}/task-status/{task_id}").json()
        if status_resp["status"] == "SUCCESS":
            print(f"💰 Final Result: {status_resp['result']}")
            return
        time.sleep(1)
    
    print("❌ Test timed out!")

if __name__ == "__main__":
    run_test()
