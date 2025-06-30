class Portfolio:
    def __init__(self):
        self.positions = {}
        self.trades = []

    def update(self, trade):
        symbol = trade["symbol"]
        qty = trade["qty"]
        if trade["action"] == "buy":
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
        elif trade["action"] == "sell":
            self.positions[symbol] = self.positions.get(symbol, 0) - qty
        self.trades.append(trade)
