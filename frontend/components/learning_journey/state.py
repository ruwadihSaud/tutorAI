import streamlit as st


LEVELS = ["Beginner", "Intermediate", "Advanced"]
PASSING_SCORE = 70


def initialize_journey_state() -> None:
    defaults = {
        "student_stage": "subject_selection",
        "selected_subject": None,
        "student_level": None,
        "current_lesson_id": None,
        "current_lesson_order": None,
        "completed_lessons": [],
        "placement_score": None,
        "level_test_score": None,
        "lesson_ready_to_continue": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def determine_level(score: int) -> str:
    if score >= 80:
        return "Advanced"

    if score >= 50:
        return "Intermediate"

    return "Beginner"


def get_next_level(level: str | None) -> str | None:
    if level not in LEVELS:
        return None

    next_index = LEVELS.index(level) + 1
    if next_index >= len(LEVELS):
        return None

    return LEVELS[next_index]


def reset_for_subject(subject: str) -> None:
    st.session_state.selected_subject = subject
    st.session_state.student_level = None
    st.session_state.current_lesson_id = None
    st.session_state.current_lesson_order = None
    st.session_state.completed_lessons = []
    st.session_state.placement_score = None
    st.session_state.level_test_score = None
    st.session_state.lesson_ready_to_continue = False
    st.session_state.student_stage = "placement_test"


def reset_journey() -> None:
    st.session_state.student_stage = "subject_selection"
    st.session_state.selected_subject = None
    st.session_state.student_level = None
    st.session_state.current_lesson_id = None
    st.session_state.current_lesson_order = None
    st.session_state.completed_lessons = []
    st.session_state.placement_score = None
    st.session_state.level_test_score = None
    st.session_state.lesson_ready_to_continue = False
