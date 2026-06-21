from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.data.lesson_loader import load_lessons


def get_subjects() -> list[str]:
    lessons = load_lessons()
    return sorted({lesson["subject"] for lesson in lessons})


def get_level_lessons(subject: str | None, level: str | None) -> list[dict]:
    if not subject or not level:
        return []

    lessons = [
        lesson
        for lesson in load_lessons()
        if lesson["subject"] == subject and lesson["level"] == level
    ]
    return sorted(lessons, key=lambda lesson: lesson["order"])


def set_current_lesson(lesson: dict) -> None:
    st.session_state.current_lesson_id = lesson["id"]


def get_current_lesson() -> dict | None:
    lessons = get_level_lessons(
        st.session_state.selected_subject,
        st.session_state.student_level,
    )

    if not lessons:
        return None

    current_id = st.session_state.current_lesson_id
    for lesson in lessons:
        if lesson["id"] == current_id:
            return lesson

    first_lesson = lessons[0]
    set_current_lesson(first_lesson)
    return first_lesson


def get_next_lesson(current_lesson: dict) -> dict | None:
    lessons = get_level_lessons(
        st.session_state.selected_subject,
        st.session_state.student_level,
    )

    for lesson in lessons:
        if lesson["order"] > current_lesson["order"]:
            return lesson

    return None
