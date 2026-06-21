# شرح مفهوم
# backend/generators/explanation_generator.py


from backend.generators.general_generator import generate_general_system_prompt
from backend.services.LLM import ask_llm


def generate_explanation(
    user_message: str,
    lesson: dict | None = None,
    explanation_scope: str = "specific_topic",
) -> str:
    if not lesson:
        return "I could not find the current lesson. Please select a lesson first."

    title = lesson.get("title", "Current Lesson")
    content = lesson.get("content", "")

    if not content or len(content.split()) < 20:
        return "The selected lesson does not have enough content to explain."

    if explanation_scope == "current_lesson":
        explanation_instruction = (
            "The student did not identify a specific point. Explain the complete "
            "lesson currently displayed, focusing on its main idea and key concepts."
        )
    else:
        explanation_instruction = (
            "The student identified a topic or point. Explain that exact topic and "
            "use the retrieved lesson as the main source."
        )

    prompt = (
        f"Current lesson title: {title}\n\n"
        f"Current lesson content:\n{content}\n\n"
        f"Student question:\n{user_message}\n\n"
        f"Explanation mode:\n{explanation_instruction}\n\n"
        "Use simple language, explain step by step, and include one practical "
        "example. Do not discuss unrelated topics. The interface will ask whether "
        "the student understood, so do not add a separate understanding question."
    )

    feature_requirements = (
        "The student is viewing a specific lesson. Explain the requested concept "
        "from the supplied lesson context accurately and step by step. Adapt the "
        "explanation to the student's question."
        "Keep the answer focused, short, and relevant. "
    )

    return ask_llm(
        prompt,
        system_prompt=generate_general_system_prompt(feature_requirements),
    )
