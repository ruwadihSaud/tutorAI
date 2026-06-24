import json
from pathlib import Path
from typing import Any

from backend.data.lesson_loader import get_lesson_by_id, load_lessons


PROGRESS_PATH = Path(__file__).resolve().parents[1] / "data" / "student_progress.json"


def _load_saved_progress() -> dict:
    if not PROGRESS_PATH.exists():
        return {}

    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as file:
            progress = json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}

    return progress if isinstance(progress, dict) else {}


def _merge_progress(progress_context: dict | None) -> dict:
    saved_progress = _load_saved_progress()
    if not isinstance(progress_context, dict):
        return saved_progress

    merged_progress = saved_progress.copy()
    for key, value in progress_context.items():
        if value is not None:
            merged_progress[key] = value

    return merged_progress


def _get_level_lessons(subject: str | None, level: str | None) -> list[dict]:
    if not subject or not level:
        return []

    return sorted(
        [
            lesson
            for lesson in load_lessons()
            if lesson.get("subject") == subject and lesson.get("level") == level
        ],
        key=lambda lesson: lesson.get("order", 0),
    )


def _normalize_completed_lessons(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    return [str(lesson_id) for lesson_id in value]


def generate_progress(
    user_message: str,
    lesson_id: str | None = None,
    progress_context: dict | None = None,
) -> dict:
    progress = _merge_progress(progress_context)
    current_lesson = get_lesson_by_id(lesson_id or progress.get("current_lesson_id"))

    subject = progress.get("selected_subject") or (
        current_lesson.get("subject") if current_lesson else None
    )
    level = progress.get("student_level") or (
        current_lesson.get("level") if current_lesson else None
    )

    if not subject or not level:
        return {
            "reply": (
                "I do not have enough progress data yet.\n\n"
                "Start your Learning Journey first, then I can show your subject, "
                "current level, and how many lessons are left."
            ),
            "progress": None,
        }

    level_lessons = _get_level_lessons(subject, level)
    completed_lessons = set(_normalize_completed_lessons(progress.get("completed_lessons")))
    completed_count = sum(lesson["id"] in completed_lessons for lesson in level_lessons)
    total_lessons = len(level_lessons)
    remaining_count = max(total_lessons - completed_count, 0)
    progress_percent = round((completed_count / total_lessons) * 100) if total_lessons else 0

    current_title = current_lesson["title"] if current_lesson else "No current lesson selected"
    placement_score = progress.get("placement_score")
    level_test_score = progress.get("level_test_score")

    score_lines = []
    if placement_score is not None:
        score_lines.append(f"- Placement score: {placement_score}%")
    if level_test_score is not None:
        score_lines.append(f"- Level test score: {level_test_score}%")

    scores_text = "\n".join(score_lines) if score_lines else "- Scores: Not available yet"

    return {
        "reply": (
            "Here is your current TutorAI progress:\n\n"
            f"- Subject: {subject}\n"
            f"- Current level: {level}\n"
            f"- Current lesson: {current_title}\n"
            f"- Completed lessons: {completed_count} of {total_lessons}\n"
            f"- Lessons remaining in this level: {remaining_count}\n"
            f"{scores_text}\n\n"
            "Keep going from your current lesson when you are ready."
        ),
        "progress": {
            "subject": subject,
            "level": level,
            "current_lesson": current_title,
            "completed_count": completed_count,
            "total_lessons": total_lessons,
            "remaining_count": remaining_count,
            "progress_percent": progress_percent,
            "placement_score": placement_score,
            "level_test_score": level_test_score,
        },
    }
