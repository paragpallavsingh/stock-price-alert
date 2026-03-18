import streamlit as st
import requests
import time

# Configuration - Point this to your GCP VM Public IP
API_URL = "http://34.173.35.53:8000"

st.set_page_config(page_title="Stock Alert Pro", page_icon="📈")

st.title("📈 Stock Alert Pro")
st.markdown("### Real-time Market Monitor (FastAPI + Celery + Redis)")

# 1. Input Section
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, BTC-USD):", "AAPL").upper()

if st.button("Get Latest Price"):
    with st.spinner(f"Queuing task for {ticker}..."):
        # Step A: Trigger the Task
        try:
            response = requests.post(f"{API_URL}/check-price/{ticker}")
            if response.status_code == 200:
                task_id = response.json().get("task_id")
                st.info(f"Task ID Generated: `{task_id}`")
                
                # Step B: Poll for Result
                placeholder = st.empty()
                for i in range(10):  # Try for 10 seconds
                    status_resp = requests.get(f"{API_URL}/task-status/{task_id}").json()
                    
                    if status_resp["status"] == "SUCCESS":
                        res = status_resp["result"]
                        placeholder.empty()
                        
                        # Display Result in a nice Metric card
                        col1, col2 = st.columns(2)
                        col1.metric(label="Current Price", value=f"${res['price']}")
                        col2.metric(label="Data Source", value=res['source'])
                        st.success(f"Successfully fetched {ticker} data!")
                        break
                    else:
                        placeholder.text(f"Worker is processing... (Attempt {i+1}/10)")
                        time.sleep(1)
                else:
                    st.error("Task timed out. Check if the Celery worker is running.")
            else:
                st.error("Could not connect to the API. Is the server running?")
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("Backend: FastAPI | Task Queue: Redis | Background Worker: Celery")
