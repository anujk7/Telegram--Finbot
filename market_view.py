# market_view.py

from config import SYMBOLS, EXCHANGES

def get_market_view(prices_by_exchange):
    result = []
    for symbol in SYMBOLS:
        bids = []
        asks = []
        for exchange in EXCHANGES:
            data = prices_by_exchange.get(symbol, {}).get(exchange, {})
            if data:
                bids.append((exchange, data.get("bid", 0)))
                asks.append((exchange, data.get("ask", float("inf"))))
        if bids and asks:
            best_bid = max(bids, key=lambda x: x[1])
            best_ask = min(asks, key=lambda x: x[1])
            result.append({
                "symbol": symbol,
                "best_bid_exchange": best_bid[0],
                "best_bid_price": best_bid[1],
                "best_ask_exchange": best_ask[0],
                "best_ask_price": best_ask[1],
            })
    return result
