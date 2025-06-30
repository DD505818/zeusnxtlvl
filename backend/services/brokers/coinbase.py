from .base import BrokerInterface

class CoinbaseBroker(BrokerInterface):
    async def execute_order(self, symbol: str, side: str, qty: float):
        print(f"Coinbase mock order {side} {qty} {symbol}")
        return {"filled_qty": qty}
