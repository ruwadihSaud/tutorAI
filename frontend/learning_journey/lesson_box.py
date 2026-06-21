from html import escape

import streamlit as st

from learning_journey.lesson_data import (
    get_current_lesson,
    get_level_lessons,
    get_next_lesson,
    set_current_lesson,
)


def _initialize_lesson_state() -> None:
    if "completed_lessons" not in st.session_state:
        st.session_state.completed_lessons = []

    if "level_lessons_completed" not in st.session_state:
        st.session_state.level_lessons_completed = False


def complete_current_lesson(lesson: dict) -> None:
    if lesson["id"] not in st.session_state.completed_lessons:
        st.session_state.completed_lessons.append(lesson["id"])

    next_lesson = get_next_lesson(lesson)

    if next_lesson:
        set_current_lesson(next_lesson)
    else:
        st.session_state.level_lessons_completed = True
        st.session_state.student_stage = "level_test"


def render_lesson_box() -> None:
    _initialize_lesson_state()

    if st.session_state.level_lessons_completed:
        st.success(
            f"You completed all {st.session_state.student_level} lessons in "
            f"{st.session_state.selected_subject}."
        )
        return

    lesson = get_current_lesson()
    lessons = get_level_lessons(
        st.session_state.selected_subject,
        st.session_state.student_level,
    )

    if not lesson or not lessons:
        st.warning("No lessons are available for the selected subject and level.")
        return

    lesson_position = lessons.index(lesson) + 1
    completed_count = sum(
        lesson_item["id"] in st.session_state.completed_lessons
        for lesson_item in lessons
    )
    progress = completed_count / len(lessons)

    with st.container(border=True):
        st.markdown(
            '<div class="lesson-box-marker"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<div class="lesson-box-heading">
<div class="lesson-box-step">Lesson {lesson_position} of {len(lessons)}</div>
<h3>{escape(lesson["title"])}</h3>
<div class="tutorai-title-meta">
<span><strong>Level:</strong> {escape(lesson["level"])}</span>
<span><strong>Chapter:</strong> {escape(lesson["chapter"])}</span>
<span><strong>Section:</strong> {escape(lesson["section"])}</span>
</div>
</div>""",
            unsafe_allow_html=True,
        )
        st.progress(progress)
        st.markdown(
            f'<p class="lesson-content">{escape(lesson["content"])}</p>',
            unsafe_allow_html=True,
        )

        if st.button(
            "I Understand - Continue",
            use_container_width=True,
            key=f"complete_lesson_{lesson['id']}",
        ):
            complete_current_lesson(lesson)
            st.rerun()
