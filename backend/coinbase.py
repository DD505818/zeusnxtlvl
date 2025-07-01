class BrokerInterface:
    async def execute_order(self, symbol: str, side: str, qty: float):
        raise NotImplementedError

    async def get_current_price(self, symbol: str):
        raise NotImplementedError


class CoinbaseBroker(BrokerInterface):
    def __init__(self, api_key: str = "", secret: str = ""):
        self.api_key = api_key
        self.secret = secret

    async def execute_order(self, symbol: str, side: str, qty: float):
        # TODO: integrate official Coinbase SDK
        print(f"Coinbase mock order {side} {qty} {symbol}")

    async def get_current_price(self, symbol: str):
        # Placeholder price
        return 3000.0
