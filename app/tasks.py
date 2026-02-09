import asyncio
from celery import Celery
from app.services.processor import MediaProcessor
from app.config.settings import Settings

settings = Settings()

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task(name="process_media_task")
def process_media_task(data: dict):
    api_key = settings.ELEVENLABS_API_KEY
    temp_dir = settings.TEMP_MEDIA_DIR
    
    processor = MediaProcessor(data, temp_dir, api_key)

    return asyncio.run(processor.run())