from agent_base import AbstractAgent
import asyncio, random, logging

logger = logging.getLogger(__name__)

class NGHeikinBreakoutAgent(AbstractAgent):
    """Minimal placeholder agent."""

    async def run(self):
        logger.info("Agent started")
        while True:
            # placeholder trading logic
            await asyncio.sleep(random.uniform(0.1, 0.5))
            logger.info("Executed mock trade")

    async def execute_trade(self, side: str, asset: str, capital: float):
        logger.info(f"Executing {side} on {asset} with {capital}")
        return {"pnl": 0.0}

