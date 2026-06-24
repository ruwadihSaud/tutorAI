import os

import requests


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

GEMINI_ERROR_PREFIXES = (
    "Gemini configuration error:",
    "Gemini connection error:",
    "Unexpected response format from Gemini.",
)


def is_gemini_error(response_text: str) -> bool:
    return response_text.startswith(GEMINI_ERROR_PREFIXES)


def ask_gemini(
    user_message: str,
    model_name: str,
    system_prompt: str | None = None,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini configuration error: GEMINI_API_KEY is missing."

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_message}],
            }
        ]
    }
    if system_prompt:
        payload["system_instruction"] = {
            "parts": [{"text": system_prompt}],
        }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}/{model_name}:generateContent",
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        parts = data["candidates"][0]["content"]["parts"]
        reply = "".join(part.get("text", "") for part in parts).strip()

        if not reply:
            return "Unexpected response format from Gemini."

        return reply

    except requests.exceptions.RequestException as error:
        return f"Gemini connection error: {error}"
    except (KeyError, IndexError, TypeError, ValueError):
        return "Unexpected response format from Gemini."
