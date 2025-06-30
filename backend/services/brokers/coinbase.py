from .base import BrokerInterface

class CoinbaseBroker(BrokerInterface):
    def __init__(self, api_key: str = "", secret: str = ""):
        self.api_key = api_key
        self.secret = secret

    async def execute_order(self, symbol: str, side: str, qty: float):
        print(f"Coinbase mock order {side} {qty} {symbol}")
        return {"symbol": symbol, "side": side, "qty": qty}

    async def get_current_price(self, symbol: str):
        return 0.0
