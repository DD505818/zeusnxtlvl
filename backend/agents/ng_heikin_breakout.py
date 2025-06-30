import asyncio
import logging
import random

from .base import AbstractAgent

logger = logging.getLogger(__name__)

class NGHeikinBreakoutAgent(AbstractAgent):
    """Minimal placeholder agent."""

    async def run(self):
        logger.info("Agent started")
        while True:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            logger.info("Executed mock trade")

    async def execute_trade(self, side: str, asset: str, quantity: float):
        logger.info("Mock execute %s %s %s", side, quantity, asset)
        await asyncio.sleep(0.1)
        return {"pnl": random.uniform(-1, 1)}
