class PostgresDB:
    def __init__(self, host: str = 'localhost', port: int = 5432, user: str = '', password: str = '', database: str = ''):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.pool = None

    async def connect(self):
        pass

    async def disconnect(self):
        pass
