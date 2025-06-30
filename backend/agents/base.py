import abc

class AbstractAgent(abc.ABC):
    name: str = "AbstractAgent"

    @abc.abstractmethod
    async def execute_trade(self, side: str, asset: str, quantity: float):
        """Execute a trade. Should return a dict with trade information."""
        raise NotImplementedError
