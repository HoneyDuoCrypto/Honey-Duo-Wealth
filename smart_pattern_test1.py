def calculate_portfolio_value(holdings, prices):
    """Calculate total portfolio value for HONEY DUO WEALTH"""
    total = 0
    for symbol, quantity in holdings.items():
        if symbol in prices:
            total += quantity * prices[symbol]
    return total

# Example usage
portfolio = {"BTC": 0.5, "ETH": 2.0}
current_prices = {"BTC": 43000, "ETH": 2500}
value = calculate_portfolio_value(portfolio, current_prices)
print(f"Portfolio value: ${value}")
