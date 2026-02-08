from typing import List, Dict
from pydantic import BaseModel, HttpUrl, field_validator


class TTSItem(BaseModel):
    text: str
    voice: str


class TaskRequest(BaseModel):
    task_name: str
    video_blocks: Dict[str, List[HttpUrl]]
    audio_blocks: Dict[str, List[HttpUrl]]
    text_to_speech: List[TTSItem]

    @field_validator("video_blocks")
    @classmethod
    def validate_video_blocks_count(cls, v: Dict) -> None | Dict:
        if not (1 <= len(v) <= 10):
            raise ValueError("Number of video blocks must be from 1 to 10")
        return v


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
