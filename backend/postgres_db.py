class FakePool:
    async def acquire(self):
        return None


class PostgresDB:
    def __init__(self, host: str = "localhost", port: int = 5432, user: str = "", password: str = "", database: str = ""):
        self.pool = FakePool()

    async def connect(self):
        pass

    async def disconnect(self):
        pass

