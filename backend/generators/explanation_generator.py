# شرح مفهوم
# backend/generators/explanation_generator.py


from backend.services.ollama_service import ask_ollama


EXPLANATION_KEYWORDS = [
    "explain",
    "explanation",
    "teach me",
    "clarify",
    "what does",
    "what is",
    "what is meant",
    "why",
    "how does",
    "understand",
    "اشرح",
    "شرح",
    "وضح",
    "فسر",
    "فهمني",
    "ما معنى",
    "وش يعني",
    "ليش",
    "كيف",
    "ما فهمت",
]


def is_explanation_request(user_message: str) -> bool:
    message = user_message.lower().strip()
    return any(keyword in message for keyword in EXPLANATION_KEYWORDS)


def generate_explanation(
    user_message: str,
    lesson: dict | None = None,
) -> str:
    if not lesson:
        return "I could not find the current lesson. Please select a lesson first."

    title = lesson.get("title", "Current Lesson")
    content = lesson.get("content", "")

    if not content or len(content.split()) < 20:
        return "The selected lesson does not have enough content to explain."

    prompt = (
        f"Current lesson title: {title}\n\n"
        f"Current lesson content:\n{content}\n\n"
        f"Student question:\n{user_message}\n\n"
        "Explain the exact point the student asked about using the current lesson "
        "as the main context. Use simple language and one practical example. "
        "Do not discuss unrelated topics. Do not ask a check-for-understanding "
        "question because the interface will show understanding buttons."
    )

    system_prompt = (
        "You are TutorAI, a patient educational agent. The student is viewing a "
        "specific lesson. Explain the requested concept from the supplied lesson "
        "context accurately and step by step. Adapt the explanation to the student's "
        "question and avoid adding unrelated information."
    )

    return ask_ollama(prompt, system_prompt=system_prompt)
