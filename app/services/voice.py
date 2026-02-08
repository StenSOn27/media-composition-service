import os
import httpx
from typing import List, Dict
from loguru import logger

class VoiceService:
    def __init__(self, target_dir: str, api_key: str):
        self.target_dir = target_dir
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}
        self._voice_map = {}

    async def setup(self):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{self.base_url}/voices", headers=self.headers)
                r.raise_for_status()
                data = r.json()
                self._voice_map = {v['name'].lower(): v['voice_id'] for v in data.get('voices', [])}
        except Exception as e:
            logger.error(f"Failed to fetch voices: {e}")

    async def generate_speech(self, tts_data: List[dict]) -> List[str]:
        if not self._voice_map:
            await self.setup()

        paths = []
        async with httpx.AsyncClient() as client:
            for i, item in enumerate(tts_data):
                local_path = os.path.join(self.target_dir, f"tts_{i}.mp3")
                voice_name = item.get('voice', '').lower()
                voice_id = self._voice_map.get(voice_name, "EXAVITQu4vr4xnNLMQyz")

                payload = {
                    "text": item['text'],
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
                }

                try:
                    r = await client.post(
                        f"{self.base_url}/text-to-speech/{voice_id}",
                        json=payload,
                        headers=self.headers
                    )
                    r.raise_for_status()

                    with open(local_path, "wb") as f:
                        f.write(r.content)

                    logger.success(f"Generated voice via REST: {local_path}")
                    paths.append(local_path)
                except Exception as e:
                    logger.error(f"REST API ElevenLabs error: {e}")
                    raise e
        return paths
