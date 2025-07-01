class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.host = host
        self.port = port

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def set(self, key: str, value):
        pass

    async def get_agent_status(self, name: str) -> dict:
        return {}

    async def set_total_system_pnl(self, pnl: float):
        pass

    async def get_total_system_pnl(self) -> float:
        return 0.0
