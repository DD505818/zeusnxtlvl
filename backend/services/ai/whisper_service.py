class WhisperService:
    def __init__(self, api_key: str):
        self.api_key = api_key
    async def transcribe(self, audio):
        return "transcription"
