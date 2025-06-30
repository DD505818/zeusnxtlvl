class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.store = {}
        self.host = host
        self.port = port

    async def connect(self):
        pass

    async def set(self, key, value):
        self.store[key] = value

    async def get(self, key, default=None):
        return self.store.get(key, default)

    async def get_total_system_pnl(self):
        return float(self.store.get("total_pnl", 0.0))

    async def set_total_system_pnl(self, value: float):
        self.store["total_pnl"] = value

    async def get_agent_status(self, agent_name: str):
        return self.store.get(f"agent:{agent_name}", {})
