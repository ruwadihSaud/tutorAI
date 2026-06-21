from collections.abc import Iterable

from backend.generators.general_generator import generate_general_system_prompt
from backend.services.LLM import ask_llm


def generate_intent_classification(
    user_message: str,
    allowed_intents: Iterable[str],
) -> str:
    intent_options = ", ".join(allowed_intents)
    feature_requirements = (
        "Act only as an intent classifier. Classify the student's message even "
        "when it contains spelling mistakes, informal Arabic, English, or a mix "
        "of both languages. Do not answer the student and do not explain your "
        "decision. Return exactly one line in this format: INTENT=<intent>."
    )
    prompt = (
        f"Allowed intents: {intent_options}\n\n"
        f"Student message: {user_message}\n\n"
        "Use general_chat for a clear greeting or normal conversation. "
        "Use unclear only when the message is meaningless, incomplete, or cannot "
        "be classified confidently. Return only INTENT=<intent>."
    )

    return ask_llm(
        prompt,
        system_prompt=generate_general_system_prompt(feature_requirements),
    )
