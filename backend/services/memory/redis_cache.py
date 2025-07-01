class RedisCache:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        pass

    async def set(self, key, value):
        pass

