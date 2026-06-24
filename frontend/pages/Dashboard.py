import json
from html import escape
from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.data.lesson_loader import get_lesson_by_id, load_lessons


PROGRESS_PATH = PROJECT_ROOT / "backend" / "data" / "student_progress.json"
LEVELS = ["Beginner", "Intermediate", "Advanced"]


def load_student_progress() -> dict:
    default_progress = {
        "student_id": "student_001",
        "student_name": "TutorAI Student",
        "selected_subject": None,
        "student_level": None,
        "current_lesson_id": None,
        "completed_lessons": [],
        "placement_score": None,
        "level_test_score": None,
        "weak_lessons": [],
    }

    if not PROGRESS_PATH.exists():
        return default_progress

    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as file:
            saved_progress = json.load(file)
    except (json.JSONDecodeError, OSError):
        return default_progress

    if not isinstance(saved_progress, dict):
        return default_progress

    return {**default_progress, **saved_progress}


def get_live_progress(saved_progress: dict) -> dict:
    progress = saved_progress.copy()

    for key in (
        "selected_subject",
        "student_level",
        "current_lesson_id",
        "placement_score",
        "level_test_score",
    ):
        session_value = st.session_state.get(key)
        if session_value is not None:
            progress[key] = session_value

    completed_lessons = st.session_state.get("completed_lessons")
    if completed_lessons:
        progress["completed_lessons"] = completed_lessons

    return progress


def get_level_lessons(subject: str | None, level: str | None) -> list[dict]:
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


def get_completion_stats(progress: dict) -> tuple[int, int, float]:
    lessons = get_level_lessons(
        progress.get("selected_subject"),
        progress.get("student_level"),
    )
    completed_ids = set(progress.get("completed_lessons", []))
    completed_count = sum(lesson["id"] in completed_ids for lesson in lessons)
    total_count = len(lessons)
    completion_rate = completed_count / total_count if total_count else 0

    return completed_count, total_count, completion_rate


def get_next_level(current_level: str | None) -> str:
    if current_level not in LEVELS:
        return "Not started"

    level_index = LEVELS.index(current_level)
    if level_index == len(LEVELS) - 1:
        return "Journey complete"

    return LEVELS[level_index + 1]


def render_metric_card(title: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="dashboard-metric-card">
            <div class="dashboard-metric-title">{escape(title)}</div>
            <div class="dashboard-metric-value">{escape(value)}</div>
            <div class="dashboard-metric-caption">{escape(caption)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_progress_overview(progress: dict) -> None:
    completed_count, total_count, completion_rate = get_completion_stats(progress)
    percent = round(completion_rate * 100)

    with st.container(border=True):
        st.markdown('<div class="dashboard-card-marker"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="tutorai-section-title">Learning Progress</div>
            <p class="tutorai-muted">Your current subject, level, and lesson progress.</p>
            """,
            unsafe_allow_html=True,
        )

        metric_cols = st.columns(4)
        with metric_cols[0]:
            render_metric_card(
                "Subject",
                progress.get("selected_subject") or "Not selected",
                "Chosen learning track",
            )
        with metric_cols[1]:
            render_metric_card(
                "Level",
                progress.get("student_level") or "Not started",
                "Current difficulty",
            )
        with metric_cols[2]:
            render_metric_card(
                "Completed",
                f"{completed_count}/{total_count}",
                "Lessons in this level",
            )
        with metric_cols[3]:
            render_metric_card(
                "Next Level",
                get_next_level(progress.get("student_level")),
                "After passing the test",
            )

        st.progress(completion_rate)
        st.caption(f"{percent}% of the current level is complete.")


def render_current_lesson(progress: dict) -> None:
    lesson = get_lesson_by_id(progress.get("current_lesson_id"))

    with st.container(border=True):
        st.markdown('<div class="dashboard-card-marker"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="tutorai-section-title">Current Lesson</div>',
            unsafe_allow_html=True,
        )

        if not lesson:
            st.info("No current lesson is selected yet. Start your Learning Journey from My Learning.")
            return

        st.markdown(
            f"""
            <div class="dashboard-lesson-box">
                <div class="dashboard-lesson-title">{escape(lesson["title"])}</div>
                <div class="tutorai-title-meta">
                    <span><strong>Subject:</strong> {escape(lesson["subject"])}</span>
                    <span><strong>Level:</strong> {escape(lesson["level"])}</span>
                    <span><strong>Chapter:</strong> {escape(lesson["chapter"])}</span>
                    <span><strong>Section:</strong> {escape(lesson["section"])}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_scores(progress: dict) -> None:
    placement_score = progress.get("placement_score")
    level_test_score = progress.get("level_test_score")
    weak_lessons = progress.get("weak_lessons", [])

    with st.container(border=True):
        st.markdown('<div class="dashboard-card-marker"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="tutorai-section-title">Scores and Revision</div>',
            unsafe_allow_html=True,
        )

        score_cols = st.columns(2)
        with score_cols[0]:
            render_metric_card(
                "Placement Test",
                f"{placement_score}%" if placement_score is not None else "Not taken",
                "Initial level check",
            )
        with score_cols[1]:
            render_metric_card(
                "Level Test",
                f"{level_test_score}%" if level_test_score is not None else "Not taken",
                "Current level result",
            )

        if weak_lessons:
            st.markdown("**Recommended Revision**")
            for lesson_id in weak_lessons:
                lesson = get_lesson_by_id(lesson_id)
                st.markdown(f"- {lesson['title'] if lesson else lesson_id}")
        else:
            st.caption("No weak lessons are marked right now.")


def render_completed_lessons(progress: dict) -> None:
    completed_lessons = progress.get("completed_lessons", [])

    with st.container(border=True):
        st.markdown('<div class="dashboard-card-marker"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="tutorai-section-title">Completed Lessons</div>',
            unsafe_allow_html=True,
        )

        if not completed_lessons:
            st.info("Completed lessons will appear here after you finish them.")
            return

        for lesson_id in completed_lessons:
            lesson = get_lesson_by_id(lesson_id)
            if not lesson:
                continue

            st.markdown(
                f"""
                <div class="dashboard-completed-item">
                    <strong>{escape(lesson["title"])}</strong>
                    <span>{escape(lesson["subject"])} - {escape(lesson["level"])}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


saved_progress = load_student_progress()
progress = get_live_progress(saved_progress)

st.markdown(
    """
    <div class="page-title">
        <h2>Dashboard</h2>
        <p>Track your learning progress, scores, and revision areas.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_progress_overview(progress)

left_col, right_col = st.columns([1.35, 1], gap="large")

with left_col:
    render_current_lesson(progress)
    render_completed_lessons(progress)

with right_col:
    render_scores(progress)
