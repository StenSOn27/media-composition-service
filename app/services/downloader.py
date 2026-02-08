import httpx
import os
import asyncio
from typing import List, Dict

class FileDownloader:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir

    async def download_all(self, urls: List[str]) -> Dict[str, str]:
        unique_urls = list(set(urls))
        async with httpx.AsyncClient() as client:
            tasks = [self._download(client, url) for url in unique_urls]
            results = await asyncio.gather(*tasks)
            return dict(results)

    async def _download(self, client: httpx.AsyncClient, url: str) -> tuple:
        filename = url.split('/')[-1]
        local_path = os.path.join(self.target_dir, filename)
        
        if not os.path.exists(local_path):
            async with client.stream("GET", url) as r:
                r.raise_for_status()
                with open(local_path, "wb") as f:
                    async for chunk in r.aiter_bytes():
                        f.write(chunk)
        return url, local_path
