import logging

class OrderExecutor:
    def __init__(self, risk, portfolio):
        self.risk = risk
        self.portfolio = portfolio

    async def simulate_fill(self, signal, market_data):
        # simple mock execution
        return {
            "symbol": signal.get("symbol"),
            "qty": signal.get("qty", 0),
            "price": market_data.get("price"),
            "action": signal.get("action")
        }

    async def handle_signal(self, signal, market_data):
        if not self.risk.check_trade(signal, self.portfolio):
            logging.warning("RiskSentinel blocked trade: %s", signal)
            return
        executed = await self.simulate_fill(signal, market_data)
        if executed:
            self.portfolio.update(executed)
