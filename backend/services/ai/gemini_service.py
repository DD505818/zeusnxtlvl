class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def analyze_market_data(self, data: str):
        return "analysis"
