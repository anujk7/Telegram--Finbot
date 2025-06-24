import pytest
from arbitrage import find_arbitrage_opportunities

# Dummy data for BBOs
dummy_bbo_data = {
    "BTC-USDT": {
        "binance": {"bid": 30000, "ask": 30100},
        "coinbase": {"bid": 30200, "ask": 30300},
        "kraken": {"bid": 30050, "ask": 30150}
    },
    "ETH-USDT": {
        "binance": {"bid": 1900, "ask": 1910},
        "coinbase": {"bid": 1925, "ask": 1930}
    }
}

def test_arbitrage_detection():
    opportunities = find_arbitrage_opportunities(dummy_bbo_data)
    
    assert isinstance(opportunities, list)
    assert len(opportunities) > 0  # There should be arbitrage opportunities
    
    for opp in opportunities:
        assert "symbol" in opp
        assert "buy_from" in opp
        assert "sell_to" in opp

        assert "percentage" in opp
        assert opp["percentage"] > 0


def test_no_arbitrage_case():
    # All exchanges have the same bid/ask
    flat_bbo_data = {
        "BTC-USDT": {
            "binance": {"bid": 30000, "ask": 30100},
            "coinbase": {"bid": 30000, "ask": 30100}
        }
    }

    opportunities = find_arbitrage_opportunities(flat_bbo_data)
    assert opportunities == []

