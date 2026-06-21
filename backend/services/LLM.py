from collections.abc import Callable

from backend.services.ollama_service import ask_ollama, is_ollama_error


# Change the active service or model here when comparing LLMs.
ACTIVE_SERVICE = "ollama"
ACTIVE_MODEL = "qwen3:14b"


LLM_SERVICES: dict[str, Callable[..., str]] = {
    "ollama": ask_ollama,
}


LLM_ERROR_PREFIXES = (
    "LLM configuration error:",
)


def ask_llm(user_message: str, system_prompt: str | None = None) -> str:
    service = LLM_SERVICES.get(ACTIVE_SERVICE)

    if service is None:
        return f"LLM configuration error: Unknown service '{ACTIVE_SERVICE}'."

    return service(
        user_message=user_message,
        system_prompt=system_prompt,
        model_name=ACTIVE_MODEL,
    )


def is_llm_error(response_text: str) -> bool:
    return response_text.startswith(LLM_ERROR_PREFIXES) or is_ollama_error(
        response_text
    )
