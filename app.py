import json
from pathlib import Path
import pandas as pd
import requests
from fake_useragent import UserAgent
import time
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "companies.json", "r", encoding="utf-8") as f:
    stocks = json.load(f)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    print(response.json())
    
def fetch_stock(symbol):
    try:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Response text: {response.text[:500]}")  # Print first 500 chars
            return None
        
        data = response.json()
        
        print(f"Fetched data for {symbol}: {data}")  # Debugging line
        
        chart = data['chart']['result'][0]
        meta = chart['meta']
        quote = chart['indicators']['quote'][0]
        
        # Extract OHLC arrays
        opens = quote.get('open', [])
        highs = quote.get('high', [])
        lows = quote.get('low', [])
        
        # Filter out None values
        opens_clean = [x for x in opens if x is not None]
        highs_clean = [x for x in highs if x is not None]
        lows_clean = [x for x in lows if x is not None]
        
        # Get day's values: first open, max high, min low
        if not opens_clean or not highs_clean or not lows_clean:
            print(f"Incomplete OHLC data for {symbol}")
            return None
        
        open_price = opens_clean[0]  # First open of the day
        day_high = max(highs_clean)  # Highest price of the day
        day_low = min(lows_clean)    # Lowest price of the day

        return {
            "open": round(open_price, 2),
            "high": round(day_high, 2),
            "low": round(day_low, 2),
            "datetime": time.strftime("%d-%m-%Y:%H:%M:%S", time.localtime(meta['regularMarketTime']))
        }
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error for {symbol}: {e}")
        print(f"Response text: {response.text[:500]}")
        return None
    except (KeyError, IndexError, TypeError, ValueError, requests.RequestException) as e:
        print(f"Error fetching {symbol}: {e}")
        return None

results = []

for name, symbol in stocks.items():
    data = fetch_stock(symbol)
    if data:
        results.append({"Stock": name, **data})
    else:
        results.append({"Stock": name, "Error": "No Data"})

df = pd.DataFrame(results)
print(df)
send_telegram_message(f"```\n{df.to_string(index=False)}\n```")