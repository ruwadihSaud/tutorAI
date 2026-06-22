from collections.abc import Callable

from dotenv import load_dotenv

from backend.services.gemini_service import ask_gemini, is_gemini_error
from backend.services.ollama_service import ask_ollama, is_ollama_error


load_dotenv()


# Change the active service or model here when comparing LLMs.
ACTIVE_SERVICE = "gemini"
ACTIVE_MODEL = "gemini-2.5-flash-lite"
FALLBACK_SERVICE = "ollama"
FALLBACK_MODEL = "qwen3:14b"


LLM_SERVICES: dict[str, Callable[..., str]] = {
    "gemini": ask_gemini,
    "ollama": ask_ollama,
}


LLM_ERROR_PREFIXES = (
    "LLM configuration error:",
    "LLM service error:",
)


def _service_has_error(service_name: str, response_text: str) -> bool:
    if service_name == "gemini":
        return is_gemini_error(response_text)

    if service_name == "ollama":
        return is_ollama_error(response_text)

    return response_text.startswith(LLM_ERROR_PREFIXES)


def _call_service(
    service_name: str,
    model_name: str,
    user_message: str,
    system_prompt: str | None,
) -> str:
    service = LLM_SERVICES.get(service_name)

    if service is None:
        return f"LLM configuration error: Unknown service '{service_name}'."

    return service(
        user_message=user_message,
        system_prompt=system_prompt,
        model_name=model_name,
    )


def ask_llm(user_message: str, system_prompt: str | None = None) -> str:
    primary_reply = _call_service(
        ACTIVE_SERVICE,
        ACTIVE_MODEL,
        user_message,
        system_prompt,
    )
    if not _service_has_error(ACTIVE_SERVICE, primary_reply):
        return primary_reply

    fallback_reply = _call_service(
        FALLBACK_SERVICE,
        FALLBACK_MODEL,
        user_message,
        system_prompt,
    )
    if not _service_has_error(FALLBACK_SERVICE, fallback_reply):
        return fallback_reply

    return "LLM service error: Gemini and Ollama are currently unavailable."


def is_llm_error(response_text: str) -> bool:
    return (
        response_text.startswith(LLM_ERROR_PREFIXES)
        or is_gemini_error(response_text)
        or is_ollama_error(response_text)
    )
