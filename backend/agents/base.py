import abc

class AbstractAgent(abc.ABC):
    """Minimal abstract trading agent."""

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    async def run(self):
        """Run the agent asynchronously."""
        raise NotImplementedError

    async def execute_trade(self, side: str, asset: str, amount: float):
        """Placeholder trade execution."""
        return {"side": side, "asset": asset, "amount": amount, "pnl": 0.0}

    async def shutdown(self):
        """Gracefully shut down agent."""
        pass
