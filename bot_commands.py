from telegram import Update
from telegram.ext import ContextTypes
import time
import asyncio

# State holders for async tasks
view_tasks = {}

# Dummy symbol list
SUPPORTED_SYMBOLS = {
    "okx": ["BTC-USDT", "ETH-USDT"],
    "binance": ["BTC-USDT", "ETH-USDT"],
    "deribit": ["BTC-USDT", "ETH-USDT"]
}

# ---------------------------
# /help command
# ---------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>📘 GoQuant Finbot Help Guide</b>\n\n"
        "<b>Basic Commands:</b>\n"
        "/start - Start the bot and show welcome message\n"
        "/help - Show this help message\n\n"
        "<b>Symbol & Market Info:</b>\n"
        "/list_symbols &lt;exchange&gt; - List available symbols (e.g., <code>/list_symbols binance</code>)\n"
        "/get_cbbo &lt;symbol&gt; - Get consolidated BBO (e.g., <code>/get_cbbo BTC-USDT</code>)\n"
        "/market &lt;symbol&gt; - Live CBBO view (e.g., <code>/market BTC-USDT</code>)\n"
        "/stop_market - Stop CBBO live updates\n\n"
        "<b>Arbitrage:</b>\n"
        "/arbitrage - Run one-time arbitrage check\n"
        "/monitor_arb &lt;symbol&gt; &lt;threshold&gt; - Start monitoring (e.g., <code>/monitor_arb BTC-USDT 0.5</code>)\n"
        "/stop_arb - Stop arbitrage monitoring"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")


# ---------------------------
# /list_symbols <exchange>
# ---------------------------
async def list_symbols_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Usage: /list_symbols <exchange>\nExample: /list_symbols binance")
        return

    exchange = context.args[0].lower()
    if exchange not in SUPPORTED_SYMBOLS:
        await update.message.reply_text("❌ Exchange not supported. Try: binance, okx, deribit")
        return

    symbols = SUPPORTED_SYMBOLS[exchange]
    await update.message.reply_text(f"📈 Symbols on {exchange.upper()}: {', '.join(symbols)}")


# ---------------------------
# Dummy CBBO for view and testing
# ---------------------------
def get_dummy_cbbo(symbol):
    dummy_data = {
        "BTC-USDT": {
            "binance": {"bid": 60000.10, "ask": 60001.20},
            "okx": {"bid": 60000.25, "ask": 60001.10},
            "deribit": {"bid": 59999.80, "ask": 60000.90}
        },
        "ETH-USDT": {
            "binance": {"bid": 3000.25, "ask": 3001.10},
            "okx": {"bid": 3000.20, "ask": 3001.25},
            "deribit": {"bid": 2999.90, "ask": 3000.80}
        }
    }
    if symbol not in dummy_data:
        return None

    all_prices = dummy_data[symbol]
    best_bid = max((info["bid"], ex) for ex, info in all_prices.items())
    best_ask = min((info["ask"], ex) for ex, info in all_prices.items())
    mid_price = round((best_bid[0] + best_ask[0]) / 2, 2)

    return {
        "symbol": symbol,
        "best_bid": best_bid,
        "best_ask": best_ask,
        "mid_price": mid_price
    }


# ---------------------------
# /market <symbol> command (CBBO live)
# ---------------------------
async def view_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Usage: /market <symbol>\nExample: /market BTC-USDT")
        return

    symbol = context.args[0].upper()
    chat_id = update.effective_chat.id

    msg = await update.message.reply_text(f"📡 Starting CBBO view for {symbol}...")

    async def cbbo_loop():
        while True:
            cbbo = get_dummy_cbbo(symbol)
            if cbbo:
                text = (
                    f"<b>📊 CBBO View for {cbbo['symbol']}</b>\n\n"
                    f"🔼 Best Bid: <code>{cbbo['best_bid'][0]}</code> on <b>{cbbo['best_bid'][1].upper()}</b>\n"
                    f"🔽 Best Ask: <code>{cbbo['best_ask'][0]}</code> on <b>{cbbo['best_ask'][1].upper()}</b>\n"
                    f"⚖️ Mid Price: <code>{cbbo['mid_price']}</code>\n"
                    f"🕒 Last Updated: {time.strftime('%H:%M:%S')}"
                )
                try:
                    await msg.edit_text(text, parse_mode="HTML")
                except Exception as e:
                    print(f"Error editing message: {e}")
                    break
            await asyncio.sleep(5)

    # Stop existing view task if running
    old_task = view_tasks.get(chat_id)
    if old_task:
        old_task.cancel()

    task = context.application.create_task(cbbo_loop())
    view_tasks[chat_id] = task


# ---------------------------
# /stop_market
# ---------------------------
async def stop_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    task = view_tasks.get(chat_id)

    if task:
        task.cancel()
        del view_tasks[chat_id]
        await update.message.reply_text("✅ Stopped CBBO view.")
    else:
        await update.message.reply_text("⚠️ No active CBBO view running.")


# ---------------------------
# Export functions
# ---------------------------
__all__ = ["help_command", "list_symbols_command", "view_market", "stop_view"]
