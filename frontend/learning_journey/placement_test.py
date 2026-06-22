import streamlit as st

from learning_journey.lesson_data import (
    get_level_lessons,
    set_current_lesson,
)
from learning_journey.state import determine_level


def render_placement_test(message: dict) -> None:
    st.write(message["content"])

    questions = message.get("questions", [])
    if not questions:
        st.warning("No placement questions are available for this subject.")
        return

    if st.session_state.placement_score is not None:
        st.success(
            f"Placement complete: {st.session_state.placement_score}% - "
            f"{st.session_state.student_level}"
        )
        return

    subject = message.get("subject", st.session_state.selected_subject)

    with st.form(f"placement_test_{subject}"):
        st.markdown(
            '<div class="placement-test-marker"></div>',
            unsafe_allow_html=True,
        )
        answers = {}

        for index, question in enumerate(questions, start=1):
            answers[question["id"]] = st.radio(
                f"{index}. {question['question']}",
                question["options"],
                key=f"placement_{subject}_{question['id']}",
            )

        submitted = st.form_submit_button(
            "Submit Placement Test",
            use_container_width=True,
        )

    if not submitted:
        return

    correct_answers = sum(
        answers[question["id"]] == question["correct_answer"]
        for question in questions
    )
    score = round((correct_answers / len(questions)) * 100)
    level = determine_level(score)
    level_lessons = get_level_lessons(subject, level)

    st.session_state.placement_score = score
    st.session_state.student_level = level
    st.session_state.completed_lessons = []
    st.session_state.level_lessons_completed = False
    st.session_state.pending_level_test = None
    st.session_state.level_test_results = {}
    st.session_state.level_test_score = None
    st.session_state.learning_completed = False

    if level_lessons:
        set_current_lesson(level_lessons[0])

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": "I submitted the placement test.",
        }
    )
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": (
                f"Your placement score is {score}%. Your starting level is "
                f"{level}."
            ),
        }
    )
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": "Your first lesson is ready.",
            "type": "lesson_box",
        }
    )
    st.rerun()
