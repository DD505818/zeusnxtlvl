import asyncio
import logging
import random
from .base import AbstractAgent

logger = logging.getLogger(__name__)

class NGHeikinBreakoutAgent(AbstractAgent):
    """Minimal placeholder agent demonstrating async trade loop."""

    async def run(self) -> None:
        logger.info("Agent started")
        while True:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            logger.info("Executed mock trade")
