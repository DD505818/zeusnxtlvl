import random
from typing import Any

class BrokerInterface:
    async def execute_order(self, symbol: str, side: str, qty: float) -> Any:
        raise NotImplementedError

    async def get_current_price(self, symbol: str) -> float:
        return 100.0 + random.random() * 10
