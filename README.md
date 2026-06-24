# TutorAI

TutorAI is a Streamlit + FastAPI learning assistant. The student starts a guided learning journey, chooses a subject, takes a placement test, studies lessons in order, asks questions about the current lesson, completes quizzes, and tracks progress.

## Project Structure

1. `backend/tutor.py`: routes the student's request to the correct generator.
2. `backend/generators/`: prompt builders and task-specific response logic.
3. `backend/data/`: lessons, placement tests, student progress, and video links.
4. `backend/services/intent_detector.py`: rule-based intent detection for Arabic and English messages.
5. `backend/services/LLM.py`: chooses the active LLM service and fallback model.
6. `backend/services/gemini_service.py`: Gemini API connection.
7. `backend/services/ollama_service.py`: local Ollama connection.
8. `backend/main.py`: FastAPI endpoints used by the frontend.
9. `frontend/components/`: shared Streamlit components such as chat, header, and footer.
10. `frontend/learning_journey/`: interactive learning journey UI blocks.
11. `frontend/pages/`: Streamlit pages such as My Learning, Dashboard, Contact, and Help.
12. `frontend/styles/theme.py`: global TutorAI frontend styling.
13. `backend/test_tutor.py`: backend routing and generator tests.

## Request Flow

`frontend/pages` -> `frontend/components/chat.py` -> `backend/main.py` -> `backend/tutor.py` -> `backend/generators` -> `backend/services/LLM.py` -> model service

## Run the Project

### 1. Create and activate an environment

```bash
conda create -n tutorai python=3.11
conda activate tutorai
```

Or use any existing Python 3.11 environment.

### 2. Install requirements

From the project root:

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Gemini is the primary model in `backend/services/LLM.py`. Ollama is used as the fallback model.

### 4. Run Ollama fallback

Make sure Ollama is running locally, then pull the fallback model if needed:

```bash
ollama pull qwen3:14b
```

TutorAI connects to Ollama at:

```text
http://localhost:11434/api/chat
```

### 5. Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### 6. Start the frontend

Open a second terminal, then run:

```bash
cd frontend
streamlit run streamlit_app.py
```

Streamlit will show a local URL, usually:

```text
http://localhost:8501
```

## Run Tests

From the project root:

```bash
python -m unittest backend.test_tutor -v
```
