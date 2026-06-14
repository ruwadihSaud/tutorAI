# عمل اختبار قصير
# backend/generators/quiz_generator.py


def generate_quiz(lesson: dict | None = None) -> str:
    if not lesson:
        return "I could not find the current lesson. Please select a lesson first."

    title = lesson.get("title", "Current Lesson")
    content = lesson.get("content", "")

    if not content or len(content.split()) < 20:
        return "The selected lesson does not have enough content to generate a quiz."

    return (
        f"Quiz for {title}:\n\n"
        "1. What is the main idea of this lesson?\n"
        "2. Mention two important concepts from the lesson.\n"
        "3. Why is this topic important?\n"
        "4. Give one example related to the lesson.\n"
        "5. Summarize the lesson in one sentence."
    )
