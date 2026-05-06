import json
from datetime import datetime
from collections import defaultdict

# Load the JSON data
with open('kpittech_data.json', 'r') as f:
    data = json.load(f)

# Extract the chart data
result = data['chart']['result'][0]
timestamps = result['timestamp']
highs = result['indicators']['quote'][0]['high']
lows = result['indicators']['quote'][0]['low']
opens = result['indicators']['quote'][0]['open']
closes = result['indicators']['quote'][0]['close']
volumes = result['indicators']['quote'][0]['volume']

# Group into 15-minute candles
candles_15m = defaultdict(lambda: {'high': -float('inf'), 'low': float('inf'), 'open': None, 'close': None, 'volume': 0})

for i, ts in enumerate(timestamps):
    if ts is None:
        continue
    
    # Round down to nearest 15-minute boundary
    # 15 minutes = 900 seconds
    candle_time = (ts // 900) * 900
    
    high = highs[i] if highs[i] is not None else 0
    low = lows[i] if lows[i] is not None else 0
    open_price = opens[i] if opens[i] is not None else 0
    close_price = closes[i] if closes[i] is not None else 0
    volume = volumes[i] if volumes[i] is not None else 0
    
    # Update high and low
    candles_15m[candle_time]['high'] = max(candles_15m[candle_time]['high'], high)
    candles_15m[candle_time]['low'] = min(candles_15m[candle_time]['low'], low)
    
    # Keep first open and last close
    if candles_15m[candle_time]['open'] is None:
        candles_15m[candle_time]['open'] = open_price
    candles_15m[candle_time]['close'] = close_price
    
    # Sum volume
    candles_15m[candle_time]['volume'] += volume

# Sort by timestamp
sorted_candles = sorted(candles_15m.items())

# Display results
print("15-MINUTE CANDLES - KPITTECH.NS")
print("=" * 90)
print(f"{'DateTime':<25} {'Open':<12} {'High':<12} {'Low':<12} {'Close':<12} {'Volume':<15}")
print("=" * 90)

for candle_time, data in sorted_candles:
    dt = datetime.fromtimestamp(candle_time, tz=__import__('datetime').timezone.utc)
    ist_time = dt.astimezone(__import__('pytz').timezone('Asia/Kolkata'))
    
    high = data['high'] if data['high'] != -float('inf') else 0
    low = data['low'] if data['low'] != float('inf') else 0
    
    print(f"{ist_time.strftime('%Y-%m-%d %H:%M'):<25} {data['open']:<12.2f} {high:<12.2f} {low:<12.2f} {data['close']:<12.2f} {data['volume']:<15.0f}")

# Save to JSON file
output_data = []
for candle_time, candle_data in sorted_candles:
    dt = datetime.fromtimestamp(candle_time, tz=__import__('datetime').timezone.utc)
    ist_time = dt.astimezone(__import__('pytz').timezone('Asia/Kolkata'))
    
    output_data.append({
        'timestamp': candle_time,
        'datetime': ist_time.isoformat(),
        'open': candle_data['open'],
        'high': candle_data['high'],
        'low': candle_data['low'],
        'close': candle_data['close'],
        'volume': candle_data['volume']
    })

with open('15m_candles.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("\n✓ Results saved to '15m_candles.json'")
print(f"✓ Total 15-minute candles: {len(sorted_candles)}")
