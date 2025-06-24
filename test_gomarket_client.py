from gomarket_client import get_symbols, get_bbo

# Try other exchanges
exchanges = ["okx", "bybit", "deribit"]

for exchange in exchanges:
    print(f"\n🔍 Fetching symbols for {exchange.upper()} Spot...")
    symbols = get_symbols(exchange)

    print(f"✅ {exchange.upper()} Spot Symbols: {symbols[:5]}")

    if symbols:
        first_symbol = symbols[0]
        print(f"📊 Fetching BBO for {first_symbol} on {exchange.upper()}...")
        bbo = get_bbo(exchange, first_symbol)
        print(f"📈 BBO for {first_symbol} on {exchange.upper()}: {bbo}")
