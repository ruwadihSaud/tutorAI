import requests

OLLAMA_URL = "http://localhost:11434/api/chat"


OLLAMA_ERROR_PREFIXES = (
    "Ollama connection error:",
    "Unexpected response format from Ollama.",
)


def is_ollama_error(response_text: str) -> bool:
    return response_text.startswith(OLLAMA_ERROR_PREFIXES)


def ask_ollama(
    user_message: str,
    model_name: str,
    system_prompt: str | None = None,
) -> str:
    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )

    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.3,
            "num_ctx": 4096,
            "num_predict": 350,
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Ollama connection error: {e}"

    except KeyError:
        return "Unexpected response format from Ollama."
