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
        """Simulate an order fill with basic slippage."""
        price = market_data.get("price") if isinstance(market_data, dict) else None
        if price is None:
            price = getattr(market_data, "price", 0)
        trade = {
            "symbol": signal.get("symbol"),
            "qty": signal.get("qty", 0),
            "price": price,
            "action": signal.get("action"),
        }
        return trade

