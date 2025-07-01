class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_response(self, prompt: str):
        return "gemini-response"

