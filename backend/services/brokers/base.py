class BrokerInterface:
    async def execute_order(self, symbol: str, side: str, qty: float):
        raise NotImplementedError

