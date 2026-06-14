# شرح مفهوم
# backend/generators/explanation_generator.py


def generate_explanation(lesson: dict | None = None) -> str:
    if not lesson:
        return "I could not find the current lesson. Please select a lesson first."

    title = lesson.get("title", "Current Lesson")
    content = lesson.get("content", "")

    if not content or len(content.split()) < 20:
        return "The selected lesson does not have enough content to explain."

    return (
        f"Explanation of {title}:\n\n"
        f"{content}\n\n"
        "In simple terms, focus on the main concept first, then connect it with examples. "
        "This helps you understand the lesson step by step instead of memorizing it."
    )
