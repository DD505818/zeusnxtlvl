class GrokService:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    async def get_trading_sentiment_insight(self, text: str):
        return "neutral"
