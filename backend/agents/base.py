import abc
import logging

class AbstractAgent(abc.ABC):
    """Simple abstract trading agent."""

    def __init__(self, brokers=None, redis_cache=None, postgres_db=None):
        self.brokers = brokers or {}
        self.redis_cache = redis_cache
        self.postgres_db = postgres_db
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    async def run(self):
        """Run the agent's main loop."""
        raise NotImplementedError

    async def shutdown(self):
        """Optional cleanup logic."""
        pass

    async def execute_trade(self, side: str, asset: str, capital: float):
        """Placeholder trade execution."""
        self.logger.info("Executing %s %s with capital %.2f", side, asset, capital)
        return {"pnl": 0.0}
