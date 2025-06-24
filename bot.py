# bot.py

import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Global monitor flags ===
active_monitors = {}

# === Import handlers ===
from bot_commands import (
    help_command,
    list_symbols_command,
    view_market,  # mapped to /market
    stop_view     # mapped to /stop_market
)
from arbitrage import find_arbitrage_opportunities
from gomarket_client import get_cbbo_command


# === Command: /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to GoQuant Finbot!\n\n"
        "Try commands like:\n"
        "/monitor_arb <symbol> <threshold>\n"
        "/stop_arb\n"
        "/arbitrage\n"
        "/market <symbol>\n"
        "/list_symbols <exchange>\n"
        "/get_cbbo <symbol>\n"
        "/help"
    )


# === Command: /stop_arb ===
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_monitors[chat_id] = False
    await update.message.reply_text("🛑 Arbitrage monitoring stopped.")


# === Command: /monitor_arb <symbol> <threshold> ===
async def monitor_arb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    args = context.args

    if len(args) < 1:
        await update.message.reply_text(
            "⚠️ Usage: /monitor_arb <symbol> [threshold_percent]\nExample: /monitor_arb BTC-USDT 0.5"
        )
        return

    symbol = args[0].upper()
    threshold = float(args[1]) if len(args) > 1 else 0.5
    exchanges = ["binance", "okx", "bybit"]

    await update.message.reply_text(
        f"📡 Monitoring {symbol} with threshold {threshold}% across {', '.join(exchanges)}"
    )
    active_monitors[chat_id] = True

    async def monitor_loop():
        while active_monitors.get(chat_id, False):
            # Simulated dummy prices (replace with real API later)
            dummy_prices = {
                symbol: {
                    "binance": {"bid": 30100, "ask": 30000},
                    "okx": {"bid": 30050, "ask": 29950},
                    "bybit": {"bid": 30080, "ask": 29900}
                }
            }

            opportunities = find_arbitrage_opportunities(dummy_prices, threshold)

            if opportunities:
                for opp in opportunities:
                    msg = (
                        f"🚨 Arbitrage Opportunity!\n"
                        f"Symbol: {opp['symbol']}\n"
                        f"Buy on {opp['buy_from']} @ ${opp['buy_price']}\n"
                        f"Sell on {opp['sell_to']} @ ${opp['sell_price']}\n"
                        f"Profit: {opp['profit_percentage']:.2f}%"
                    )
                    await context.bot.send_message(chat_id=chat_id, text=msg)

            await asyncio.sleep(5)

    context.application.create_task(monitor_loop())


# === Command: /arbitrage ===
async def arbitrage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dummy_prices = {
        "BTC-USDT": {
            "binance": {"bid": 30100, "ask": 30000},
            "okx": {"bid": 30050, "ask": 29950},
            "bybit": {"bid": 30080, "ask": 29900}
        }
    }

    opportunities = find_arbitrage_opportunities(dummy_prices, threshold=0.5)

    if opportunities:
        for opp in opportunities:
            msg = (
                f"🚨 Arbitrage Opportunity!\n"
                f"Symbol: {opp['symbol']}\n"
                f"Buy on {opp['buy_from']} @ ${opp['buy_price']}\n"
                f"Sell on {opp['sell_to']} @ ${opp['sell_price']}\n"
                f"Profit: {opp['profit_percentage']:.2f}%"
            )
            await update.message.reply_text(msg)
    else:
        await update.message.reply_text("No arbitrage opportunities at the moment.")


# === Main Function ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list_symbols", list_symbols_command))
    app.add_handler(CommandHandler("get_cbbo", get_cbbo_command))
    app.add_handler(CommandHandler("market", view_market))         # 👈 Replaces /view_market
    app.add_handler(CommandHandler("stop_market", stop_view))      # 👈 Stops live CBBO updates
    app.add_handler(CommandHandler("arbitrage", arbitrage_command))
    app.add_handler(CommandHandler("monitor_arb", monitor_arb))
    app.add_handler(CommandHandler("stop_arb", stop))

    print("🤖 Bot started. Waiting for commands...")
    app.run_polling()


# === Entry Point ===
if __name__ == "__main__":
    main()
