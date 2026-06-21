from fastapi import FastAPI
from pydantic import BaseModel

from backend.generators.quiz_generator import generate_placement_test
from backend.services.ollama_service import ask_ollama

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class PlacementTestRequest(BaseModel):
    subject: str


@app.get("/")
def root():
    return {"message": "TutorAI FastAPI backend is running."}


@app.post("/chat")
def chat(request: ChatRequest):
    reply = ask_ollama(request.message)
    return {"reply": reply}


@app.post("/placement-test")
def placement_test(request: PlacementTestRequest):
    return generate_placement_test(request.subject)
