📈 How to Use the Stock Price Tracker
This app is a real-time "Worker" system. Because it fetches data from global markets, it doesn't just show a static page—it performs a "Job" for you in the background.

1. Open the "Control Panel"
Click this link to open the app interface:
👉 http://34.173.35.53:8000/docs

2. Request a Stock Price (The "Order")
Look for the Green Box labeled /check-price.

Click the down arrow on the right to expand it.

Click the "Try it out" button.

In the ticker box, type any stock symbol (e.g., AAPL, TSLA, NVDA).

Click the big blue Execute button.

What happens: The app creates a unique Task ID.

Action: Copy that Task ID (it looks like a long string of letters and numbers).

3. Get the Result (The "Delivery")
Since the app fetches live data, it takes about 1 second to "finish" the job.

Look for the Blue Box labeled /task-status.

Click to expand it and click "Try it out".

Paste your Task ID into the box.

Click Execute.

The Result: You will see the current market price, the company symbol, and where the data came from.
