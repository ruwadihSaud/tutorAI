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
    selected_subject: str | None = None
    student_level: str | None = None
    current_lesson_id: str | None = None
    completed_lessons: list[str] | None = None
    placement_score: int | None = None
    level_test_score: int | None = None


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
        lesson_id=request.lesson_id or request.current_lesson_id,
        progress_context={
            "selected_subject": request.selected_subject,
            "student_level": request.student_level,
            "current_lesson_id": request.current_lesson_id or request.lesson_id,
            "completed_lessons": request.completed_lessons,
            "placement_score": request.placement_score,
            "level_test_score": request.level_test_score,
        },
    )


@app.post("/placement-test")
def placement_test(request: PlacementTestRequest):
    return generate_placement_test_reply(request.subject)


@app.post("/level-test")
def level_test(request: LevelTestRequest):
    return generate_level_test_reply(request.subject, request.level)
