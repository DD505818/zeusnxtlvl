from agent_base import AbstractAgent
import asyncio
import random
import logging

logger = logging.getLogger(__name__)

class NGHeikinBreakoutAgent(AbstractAgent):
    """Minimal placeholder agent."""

    def __init__(self, brokers=None, redis_cache=None, postgres_db=None):
        self.brokers = brokers or {}
        self.redis_cache = redis_cache
        self.postgres_db = postgres_db

    async def run(self):
        logger.info("Agent started")
        while True:
            # placeholder trading logic
            await asyncio.sleep(random.uniform(0.1, 0.5))
            logger.info("Executed mock trade")

    async def execute_trade(self, side: str, asset: str, capital: float):
        logger.info(f"Executing {side} on {asset} with {capital}")
        return {"pnl": 0.0}

