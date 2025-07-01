class AbstractAgent:
    async def signal(self, data):
        raise NotImplementedError
