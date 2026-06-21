import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:14b"


OLLAMA_ERROR_PREFIXES = (
    "Ollama connection error:",
    "Unexpected response format from Ollama.",
)


def is_ollama_error(response_text: str) -> bool:
    return response_text.startswith(OLLAMA_ERROR_PREFIXES)


def ask_ollama(user_message: str, system_prompt: str | None = None) -> str:
    default_system_prompt = (
        "You are TutorAI, a friendly educational tutor. "
        "Explain clearly, ask simple follow-up questions, "
        "Use simple language. "
        "Maximum 2 short sentences. "
        "and help the student learn step by step."
        "Do not explain more unless the student asks."
    )
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": system_prompt or default_system_prompt,
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
