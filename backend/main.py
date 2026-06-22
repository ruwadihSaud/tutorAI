from fastapi import FastAPI
from pydantic import BaseModel

from backend.tutor import (
    generate_level_test_reply,
    generate_placement_test_reply,
    generate_tutor_reply,
)

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    lesson_id: str | None = None


class PlacementTestRequest(BaseModel):
    subject: str


class LevelTestRequest(BaseModel):
    subject: str
    level: str


@app.get("/")
def root():
    return {"message": "TutorAI FastAPI backend is running."}


@app.post("/chat")
def chat(request: ChatRequest):
    return generate_tutor_reply(
        user_message=request.message,
        lesson_id=request.lesson_id,
    )


@app.post("/placement-test")
def placement_test(request: PlacementTestRequest):
    return generate_placement_test_reply(request.subject)


@app.post("/level-test")
def level_test(request: LevelTestRequest):
    return generate_level_test_reply(request.subject, request.level)
