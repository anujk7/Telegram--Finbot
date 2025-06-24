from telegram import Update
from telegram.ext import ContextTypes

# Dummy data for symbols
SYMBOLS = ["BTC-USDT", "ETH-USDT", "XRP-USDT"]


async def list_symbols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Available Symbols:\n" + "\n".join(SYMBOLS))


async def get_cbbo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("⚠️ Usage: /get_cbbo <symbol>\nExample: /get_cbbo BTC-USDT")
        return

    symbol = args[0]

    # Dummy CBBO data — replace with real API call later
    cbbo_data = {
        "binance": {"bid": 30100, "ask": 30000},
        "okx": {"bid": 30050, "ask": 29950},
        "bybit": {"bid": 30080, "ask": 29900}
    }

    if symbol not in SYMBOLS:
        await update.message.reply_text(f"❌ Symbol {symbol} not found.")
        return

    msg = f"📊 CBBO for {symbol}:\n"
    for exch, prices in cbbo_data.items():
        msg += f"• {exch.capitalize()} - Bid: ${prices['bid']}, Ask: ${prices['ask']}\n"

    await update.message.reply_text(msg)
