class GrokService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def get_trading_sentiment_insight(self, text: str) -> str:
        return "neutral"
