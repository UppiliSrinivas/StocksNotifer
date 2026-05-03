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
        
        # Check if quote data is available
        if not quote.get('close') or not quote['close'] or quote['close'][-1] is None:
            print(f"No quote data available for {symbol}")
            return None
        
        # Get the latest data (last item)
        close = quote['close'][-1]
        open_price = quote['open'][-1] if quote.get('open') and quote['open'] else close
        high = quote['high'][-1] if quote.get('high') and quote['high'] else close
        low = quote['low'][-1] if quote.get('low') and quote['low'] else close
        volume = quote['volume'][-1] if quote.get('volume') and quote['volume'] else 0
        
        if close is None:
            return None
        
        return {
            "price": round(close, 2),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "volume": int(volume),
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