# ط¹ظ…ظ„ ط§ط®طھط¨ط§ط± ظ‚طµظٹط±
# backend/generators/quiz_generator.py

import json
import random
from pathlib import Path

from backend.data.lesson_loader import load_lessons


PLACEMENT_TESTS_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "placement_tests.json"
)


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


def load_placement_tests() -> dict[str, dict[str, list[dict]]]:
    with open(PLACEMENT_TESTS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _prepare_question(question: dict, level: str) -> dict:
    option_items = list(question["options"].items())
    correct_text = question["options"][question["answer"]]
    random.shuffle(option_items)

    displayed_options = []
    correct_answer = ""

    for index, (_, option_text) in enumerate(option_items):
        display_letter = chr(ord("A") + index)
        displayed_option = f"{display_letter}. {option_text}"
        displayed_options.append(displayed_option)

        if option_text == correct_text:
            correct_answer = displayed_option

    return {
        "id": question["id"],
        "question": question["question"],
        "options": displayed_options,
        "correct_answer": correct_answer,
        "source_level": level,
    }


def generate_placement_test(subject: str) -> dict:
    all_lessons = load_lessons()
    subject_exists = any(lesson["subject"] == subject for lesson in all_lessons)

    if not subject_exists:
        return {
            "reply": f"I could not find lessons for {subject}.",
            "subject": subject,
            "questions": [],
        }

    placement_tests = load_placement_tests()
    subject_question_bank = placement_tests.get(subject, {})
    questions = []

    for level in ["Beginner", "Intermediate", "Advanced"]:
        level_questions = subject_question_bank.get(level, [])
        selected_questions = random.sample(
            level_questions,
            k=min(2, len(level_questions)),
        )
        questions.extend(
            _prepare_question(question, level)
            for question in selected_questions
        )

    random.shuffle(questions)

    return {
        "reply": (
            f"Great choice. You will start with a short placement test in {subject} "
            "so TutorAI can choose the right level for you. Choose one answer "
            "for each question, then submit the test."
        ),
        "subject": subject,
        "questions": questions,
    }
