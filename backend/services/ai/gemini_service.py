class GeminiService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def analyze_market_data(self, data: str) -> str:
        return "analysis"
