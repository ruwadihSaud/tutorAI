# backend/generators/summary_generator.py


def generate_summary(lesson: dict | None = None) -> str:
    if not lesson:
        return "I could not find the current lesson. Please select a lesson first."

    title = lesson.get("title", "Current Lesson")
    content = lesson.get("content", "")

    if not content or len(content.split()) < 20:
        return "The selected lesson does not have enough content to summarize."

    sentences = content.replace("\n", " ").split(".")

    selected_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence.split()) >= 6:
            selected_sentences.append(sentence)

        if len(selected_sentences) == 3:
            break

    if not selected_sentences:
        return "I could not generate a summary from the current lesson."

    summary = "\n".join([f"- {sentence}." for sentence in selected_sentences])

    return (
        f"Summary of {title}:\n\n"
        f"{summary}"
    )