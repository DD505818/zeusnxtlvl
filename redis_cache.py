class FakeRedisClient:
    async def ping(self):
        return True


class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.store = {}
        self.client = FakeRedisClient()

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def set(self, key: str, value):
        self.store[key] = value

    async def get(self, key: str):
        return self.store.get(key)

    async def get_agent_status(self, name: str):
        return await self.get(f"agent:{name}:status") or {}

    async def set_agent_status(self, name: str, status: dict):
        await self.set(f"agent:{name}:status", status)

    async def update_agent_status(self, name: str, **kwargs):
        status = await self.get_agent_status(name)
        status.update(kwargs)
        await self.set_agent_status(name, status)

    async def set_total_system_pnl(self, value: float):
        await self.set("system:daily_pnl", value)

    async def get_total_system_pnl(self):
        return self.store.get("system:daily_pnl", 0.0)

