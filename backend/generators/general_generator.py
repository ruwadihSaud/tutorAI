from backend.services.LLM import ask_llm


GENERAL_SYSTEM_PROMPT = (
    "You are TutorAI, a friendly and patient educational tutor. "
    "Use clear, simple language and keep the conversation focused on learning. "
    "Do not invent lesson content or unrelated information."
)


def generate_general_system_prompt(feature_requirements: str = "") -> str:
    if not feature_requirements:
        return GENERAL_SYSTEM_PROMPT

    return f"{GENERAL_SYSTEM_PROMPT}\n\nTask requirements:\n{feature_requirements}"


def generate_general(user_message: str) -> str:
    feature_requirements = (
        "Respond to the student's general message clearly and briefly. "
        "If the message is a greeting, greet the student and offer learning help."
    )

    return ask_llm(
        user_message,
        system_prompt=generate_general_system_prompt(feature_requirements),
    )
