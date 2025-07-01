class VectorDB:
    def __init__(self, url: str = ''):
        self.url = url

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def query_similar_events(self, query: str):
        return []
