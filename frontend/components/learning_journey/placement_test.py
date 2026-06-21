import streamlit as st

from components.learning_journey.lesson_data import (
    get_level_lessons,
    set_current_lesson,
)
from components.learning_journey.state import determine_level


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
    st.session_state.student_stage = "learning"

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
    st.rerun()
