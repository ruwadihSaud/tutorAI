from backend.services.LLM import ask_llm


def generate_general(user_message: str) -> str:
    system_prompt = (
        "You are TutorAI, a friendly educational tutor. Respond to the student's "
        "general message clearly and briefly. Keep the conversation focused on "
        "learning and do not invent lesson content."
    )

    return ask_llm(user_message, system_prompt=system_prompt)
