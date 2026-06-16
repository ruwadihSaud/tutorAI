import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:14b"


def ask_ollama(user_message: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are TutorAI, a friendly educational tutor. "
                    "Explain clearly, ask simple follow-up questions, "
                    "Use simple language. "
                    "Maximum 2 short sentences. "
                    "and help the student learn step by step."
                    "Do not explain more unless the student asks."
                ),
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Ollama connection error: {e}"

    except KeyError:
        return "Unexpected response format from Ollama."