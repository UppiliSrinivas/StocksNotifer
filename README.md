# Share Market Stock Price Fetcher

A Python script that fetches live stock prices from Yahoo Finance for NSE-listed companies and sends formatted updates to a Telegram group during market hours.

## Features

- Fetches real-time stock prices for multiple NSE companies
- Sends formatted table updates to Telegram
- Includes timestamps and percentage changes
- Runs automatically during market hours (9:15 AM, 11:00 AM, 1:00 PM, 2:30 PM, 3:30 PM IST)
- Error handling and User-Agent rotation for reliable API access
- Flask API endpoints for manual testing

## Setup

### Local Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ShareMarket
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install requests flask fake-useragent python-dotenv pandas rich
```

4. Create a `.env` file with your Telegram credentials:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Telegram Bot Setup

1. Create a new bot with [@BotFather](https://t.me/botfather) on Telegram
2. Get your bot token from BotFather
3. Add the bot to your group and make it an admin
4. Get the chat ID by sending a message to the group and checking:
   - `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - Look for the `chat.id` in the response

### GitHub Actions Setup

1. Push this repository to GitHub
2. Go to your repository Settings > Secrets and variables > Actions
3. Add the following secrets:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram group chat ID

The workflow will automatically run during market hours (Monday-Friday) in IST timezone.

## Usage

### Running Locally

```bash
python app.py
```

This will fetch stock data and send it to your Telegram group.

### API Endpoints

The Flask app provides these endpoints:

- `GET /`: Fetch and send stock updates to Telegram
- `GET /test`: Test endpoint that returns stock data as JSON

### Cron Setup (Alternative to GitHub Actions)

For local cron jobs, add these lines to your crontab:

```bash
15 9 * * 1-5 cd /path/to/project && /path/to/python app.py
0 11 * * 1-5 cd /path/to/project && /path/to/python app.py
0 13 * * 1-5 cd /path/to/project && /path/to/python app.py
30 14 * * 1-5 cd /path/to/project && /path/to/python app.py
30 15 * * 1-5 cd /path/to/project && /path/to/python app.py
```

## Companies

Currently tracks these NSE-listed companies:
- Reliance Industries (RELIANCE.NS)
- Tata Consultancy Services (TCS.NS)
- HDFC Bank (HDFCBANK.NS)
- Infosys (INFY.NS)
- ICICI Bank (ICICIBANK.NS)
- Hindustan Unilever (HINDUNILVR.NS)
- ITC (ITC.NS)
- Kotak Mahindra Bank (KOTAKBANK.NS)
- Larsen & Toubro (LT.NS)
- Axis Bank (AXISBANK.NS)
- Bajaj Finance (BAJFINANCE.NS)
- Maruti Suzuki (MARUTI.NS)

To add more companies, edit `companies.json`:

```json
{
  "Company Name": "SYMBOL.NS",
  "Another Company": "ANOTHER.NS"
}
```

## Dependencies

- `requests`: HTTP requests to Yahoo Finance API
- `flask`: Web framework for API endpoints
- `fake-useragent`: Random User-Agent generation
- `python-dotenv`: Environment variable loading
- `pandas`: Data manipulation for table formatting
- `rich`: Enhanced console output

## License

MIT License