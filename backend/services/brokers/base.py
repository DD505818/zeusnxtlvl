class BrokerInterface:
    async def execute_order(self, symbol: str, side: str, qty: float):
        raise NotImplementedError

    async def get_current_price(self, symbol: str):
        return 0.0
