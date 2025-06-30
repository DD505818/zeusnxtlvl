import logging
import random

class OrderExecutor:
    def __init__(self, risk, portfolio):
        self.risk = risk
        self.portfolio = portfolio

    async def simulate_fill(self, signal, market_data):
        price = market_data.get("price")
        qty = signal.get("qty", 0)
        side = signal.get("action")
        if price is None or side not in ("buy", "sell"):
            return None
        slippage = price * random.uniform(-0.001, 0.001)
        executed_price = price + slippage
        return {"symbol": market_data.get("symbol"), "qty": qty, "price": executed_price, "action": side}

    async def handle_signal(self, signal, market_data):
        if not self.risk.check_trade(signal, self.portfolio):
            logging.warning("RiskSentinel blocked trade: %s", signal)
            return

        executed = await self.simulate_fill(signal, market_data)
        if executed:
            self.portfolio.update(executed)
