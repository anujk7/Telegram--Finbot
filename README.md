# 📈 GoQuant Telegram Finbot (Assignment Project)

This is a Telegram bot built in Python as part of the GoQuant backend assignment. The bot simulates a real-time trading information system using **dummy data**, mimicking the GoMarket API, and offers insights like arbitrage opportunities and consolidated market views across multiple exchanges.

---

## 📌 Features Implemented

### ✅ Arbitrage Signal Service
- Detects arbitrage opportunities between the same asset across multiple exchanges (using dummy prices).
- Allows configuration via Telegram using:  
  `/monitor_arb <symbol> <threshold>`  
  `/stop_arb`

### ✅ Consolidated Market View
- Calculates **CBBO** (Consolidated Best Bid/Offer) and mid-price.
- Identifies the best exchange to trade.
- Supports command:  
  `/get_cbbo <symbol>`  
  `/market <symbol>`

### ✅ Symbol Discovery
- Lists symbols from dummy GoMarket responses.
- Uses:  
  `/list_symbols <exchange>`

---

## 🚀 Setup & Run

Step 1:clone the repo
git clone <your-repo-url>
cd goquant-telegram-bot


Step 2:Install Requirements
pip install -r requirements.txt

Step 3:Configure .env
BOT_TOKEN=your_telegram_bot_token_here

Step 4:Run the Bot
python bot.py


Assumptions
Real GoMarket APIs were replaced with dummy/static data due to HTTP 400 errors.

Arbitrage and CBBO logic are still fully functional on simulated data.

Simulated data mimics Binance, OKX, Bybit, and Deribit spot markets.

Deliverables Included
✅ Source code

✅ README with setup steps

✅ .env.example

✅ Working Telegram Bot demo (using dummy data)

✅ Video demo as per instructions


Author
Anuj Sharma
Backend Assignment - Telegram Finbot
LinkedIn:-
https://www.linkedin.com/in/anuj-khandelwal-425571246/ | Email:anujkhandelwal279@gmail.com