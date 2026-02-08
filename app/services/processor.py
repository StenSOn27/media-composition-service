import os
import asyncio
import random
from itertools import product
from app.services.downloader import FileDownloader
from app.services.voice import VoiceService
from app.services.video import VideoEditor

class MediaProcessor:
    def __init__(self, data: dict, temp_dir: str, api_key: str):
        self.data = data
        self.task_dir = os.path.join(temp_dir, data['task_name'])
        os.makedirs(self.task_dir, exist_ok=True)
        self.downloader = FileDownloader(self.task_dir)
        self.voice = VoiceService(self.task_dir, api_key)
        self.editor = VideoEditor()

    async def run(self):
        v_urls = [u for b in self.data['video_blocks'].values() for u in b]
        a_urls = [u for b in self.data['audio_blocks'].values() for u in b]
        
        v_map = await self.downloader.download_all(v_urls)
        a_map = await self.downloader.download_all(a_urls)
        tts_paths = await self.voice.generate_speech(self.data['text_to_speech'])

        v_blocks = [[v_map[u] for u in self.data['video_blocks'][k]] for k in sorted(self.data['video_blocks'].keys())]
        combos = list(product(*v_blocks))

        for i, combo in enumerate(combos):
            output = os.path.join(self.task_dir, f"result_{i}.mp4")
            await asyncio.to_thread(
                self.editor.render, 
                list(combo), 
                random.choice(list(a_map.values())), 
                random.choice(tts_paths), 
                output
            )