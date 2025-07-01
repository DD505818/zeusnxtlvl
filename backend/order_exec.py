import logging


class OrderExecutor:
    def __init__(self, risk, portfolio):
        self.risk = risk
        self.portfolio = portfolio

    async def handle_signal(self, signal, market_data):
        # Run risk checks first
        if not self.risk.check_trade(signal, self.portfolio):
            logging.warning("RiskSentinel blocked trade: %s", signal)
            return

        # Simulate execution: add slippage, partial fills (in backtest)
        executed = await self.simulate_fill(signal, market_data)
        if executed:
            self.portfolio.update(executed)

    async def simulate_fill(self, signal, market_data):
        # Very simple fill logic
        return {**signal, "price": market_data.get("price"), "pnl": 0.0}

