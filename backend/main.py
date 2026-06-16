from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.ollama_service import ask_ollama

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "TutorAI FastAPI backend is running."}


@app.post("/chat")
def chat(request: ChatRequest):
    reply = ask_ollama(request.message)
    return {"reply": reply}