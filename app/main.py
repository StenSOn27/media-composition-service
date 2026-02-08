from fastapi import FastAPI, status
from app.schemas import TaskRequest, TaskResponse
from app.tasks import process_media_task

app = FastAPI()

@app.post("/process_media")
async def process_media(request: TaskRequest):
    task_data = request.model_dump(mode='json')
    task = process_media_task.delay(task_data)

    return TaskResponse(
            status="queued",
            task_id=str(task.id),
            message=f"Task '{request.task_name}' added to the queue."
        )
