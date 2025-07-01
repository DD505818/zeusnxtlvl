class AbstractAgent:
    """Base class for trading agents."""

    async def run(self):
        raise NotImplementedError

    async def shutdown(self):
        pass

    async def execute_trade(self, side: str, asset: str, capital: float):
        return {"pnl": 0.0}

