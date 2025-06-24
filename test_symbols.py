from gomarket_client import get_supported_symbols

for ex in ['binance', 'okx']:
    print(f"Supported symbols for {ex}:")
    symbols = get_supported_symbols(ex)
    for s in symbols:
        print(f" - {s}")
