def find_arbitrage_opportunities(price_data: dict, threshold: float = 0.5) -> list:
    opportunities = []
    for symbol, exchanges in price_data.items():
        for buy_exchange, buy_data in exchanges.items():
            buy_price = buy_data.get("ask")
            if buy_price is None:
                continue
            for sell_exchange, sell_data in exchanges.items():
                if buy_exchange == sell_exchange:
                    continue
                sell_price = sell_data.get("bid")
                if sell_price is None:
                    continue
                profit_percent = ((sell_price - buy_price) / buy_price) * 100
                if profit_percent >= threshold:
                    opportunities.append({
                        "symbol": symbol,
                        "buy_from": buy_exchange,
                        "buy_price": buy_price,
                        "sell_to": sell_exchange,
                        "sell_price": sell_price,
                        "profit_percentage": profit_percent
                    })
    return opportunities
