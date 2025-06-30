import abc
import logging
from typing import Any

logger = logging.getLogger(__name__)

class AbstractAgent(abc.ABC):
    """Simple agent base class."""

    def __init__(self, *args, **kwargs) -> None:
        pass

    async def execute_trade(self, side: str, symbol: str, capital: float) -> dict:
        logger.info("Executing %s %s with capital %s", side, symbol, capital)
        return {"pnl": 0.0, "symbol": symbol, "side": side}

    async def shutdown(self) -> None:
        pass

    @abc.abstractmethod
    async def run(self) -> None:
        """Run the agent asynchronously."""
        raise NotImplementedError
