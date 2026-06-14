# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel

from backend.tutor import generate_tutor_reply


app = FastAPI(
    title="TutorAI Backend",
    description="Backend API for the TutorAI adaptive tutoring agent",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str
    lesson_id: str | None = None


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def root():
    return {
        "message": "TutorAI FastAPI backend is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = generate_tutor_reply(
        user_message=request.message,
        lesson_id=request.lesson_id
    )

    return ChatResponse(reply=reply)