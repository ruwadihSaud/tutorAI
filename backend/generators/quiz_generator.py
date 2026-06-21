# عمل اختبار قصير
# backend/generators/quiz_generator.py


import random

from backend.data.lesson_loader import load_lessons


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


def _first_sentence(content: str) -> str:
    sentence = content.split(".", 1)[0].strip()
    return f"{sentence}." if sentence else content


def _unique_options(
    correct: str,
    distractors: list[str],
    seed: str,
) -> list[str]:
    options = [correct]

    for option in distractors:
        if option and option not in options:
            options.append(option)

        if len(options) == 3:
            break

    random.Random(seed).shuffle(options)
    return options


def generate_placement_test(subject: str) -> dict:
    all_lessons = load_lessons()
    subject_lessons = sorted(
        [lesson for lesson in all_lessons if lesson["subject"] == subject],
        key=lambda lesson: (lesson["order"], lesson["level"]),
    )

    if not subject_lessons:
        return {
            "reply": f"I could not find lessons for {subject}.",
            "subject": subject,
            "questions": [],
        }

    other_lessons = [
        lesson for lesson in all_lessons if lesson["subject"] != subject
    ]
    beginner_lessons = [
        lesson for lesson in subject_lessons if lesson["level"] == "Beginner"
    ] or subject_lessons
    advanced_lessons = [
        lesson for lesson in subject_lessons if lesson["level"] == "Advanced"
    ] or subject_lessons[-1:]

    first_lesson = beginner_lessons[0]
    advanced_lesson = advanced_lessons[0]
    title_distractors = [lesson["title"] for lesson in other_lessons]
    description_distractors = [
        _first_sentence(lesson["content"])
        for lesson in subject_lessons[1:]
    ]

    questions = [
        {
            "id": "subject_foundation",
            "question": f"Which topic is part of the {subject} learning path?",
            "options": _unique_options(
                first_lesson["title"],
                title_distractors,
                f"{subject}:subject_foundation",
            ),
            "correct_answer": first_lesson["title"],
        },
        {
            "id": "concept_understanding",
            "question": f"Which description best matches {first_lesson['title']}?",
            "options": _unique_options(
                _first_sentence(first_lesson["content"]),
                description_distractors,
                f"{subject}:concept_understanding",
            ),
            "correct_answer": _first_sentence(first_lesson["content"]),
        },
        {
            "id": "advanced_awareness",
            "question": f"Which topic belongs to the advanced {subject} material?",
            "options": _unique_options(
                advanced_lesson["title"],
                [lesson["title"] for lesson in beginner_lessons],
                f"{subject}:advanced_awareness",
            ),
            "correct_answer": advanced_lesson["title"],
        },
    ]

    return {
        "reply": (
            f"Great choice. You will start with a short placement test in {subject} "
            "so TutorAI can choose the right level for you."
        ),
        "subject": subject,
        "questions": questions,
    }
