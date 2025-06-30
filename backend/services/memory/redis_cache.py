class RedisCache:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.store = {}

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def set(self, key: str, value):
        self.store[key] = value

    async def get(self, key: str, default=None):
        return self.store.get(key, default)

    async def get_agent_status(self, name: str):
        return self.store.get(f"agent:{name}:status", {})

    async def set_total_system_pnl(self, pnl: float):
        self.store["system:daily_pnl"] = pnl

    async def get_total_system_pnl(self):
        return self.store.get("system:daily_pnl", 0.0)
