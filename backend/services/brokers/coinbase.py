from backend.services.brokers.base import BrokerInterface


class CoinbaseBroker(BrokerInterface):
    async def execute_order(self, symbol: str, side: str, qty: float):
        # TODO: integrate official Coinbase SDK
        print(f"Coinbase mock order {side} {qty} {symbol}")

