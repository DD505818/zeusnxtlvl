class WhisperService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def transcribe_audio(self, path: str) -> str:
        return "transcript"
