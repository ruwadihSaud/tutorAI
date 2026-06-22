import streamlit as st

from learning_journey.lesson_data import get_level_lessons, set_current_lesson
from learning_journey.state import get_next_level


def calculate_level_test_score(
    questions: list[dict],
    answers: dict[str, str | None],
) -> int:
    if not questions:
        return 0

    correct_answers = sum(
        answers.get(question["id"]) == question["correct_answer"]
        for question in questions
    )
    return round((correct_answers / len(questions)) * 100)


def _remove_lesson_boxes() -> None:
    st.session_state.chat_messages = [
        message
        for message in st.session_state.chat_messages
        if message.get("type") != "lesson_box"
    ]


def reset_for_new_journey() -> None:
    interactive_types = {
        "start_prompt",
        "subject_selection",
        "placement_test",
        "lesson_box",
        "explanation_check",
        "level_test",
    }
    st.session_state.chat_messages = [
        message
        for message in st.session_state.chat_messages
        if message.get("type") not in interactive_types
    ]
    st.session_state.journey_started = False
    st.session_state.selected_subject = None
    st.session_state.student_level = None
    st.session_state.current_lesson_id = None
    st.session_state.completed_lessons = []
    st.session_state.placement_score = None
    st.session_state.level_test_score = None
    st.session_state.level_test_results = {}
    st.session_state.level_lessons_completed = False
    st.session_state.pending_placement_subject = None
    st.session_state.pending_level_test = None
    st.session_state.pending_user_message = None
    st.session_state.resolved_explanation_checks = []
    st.session_state.learning_completed = False


def finish_learning_journey(subject: str, level: str = "Advanced") -> None:
    reset_for_new_journey()
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": (
                f"You passed the {level} test and completed all available "
                f"levels in {subject}."
            ),
            "type": "journey_complete",
        }
    )
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": "I am TutorAI. Are you ready for your Learning Journey?",
            "type": "start_prompt",
        }
    )


def _continue_after_test(
    subject: str,
    level: str,
    score: int,
    passed: bool,
) -> None:
    st.session_state.level_test_score = score
    st.session_state.completed_lessons = []
    st.session_state.level_lessons_completed = False
    _remove_lesson_boxes()

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": f"I completed the {level} level test and scored {score}%.",
        }
    )

    if passed:
        next_level = get_next_level(level)
        if next_level:
            next_lessons = get_level_lessons(subject, next_level)
            st.session_state.student_level = next_level

            if next_lessons:
                set_current_lesson(next_lessons[0])
                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            f"You passed the {level} test. You are now starting "
                            f"the {next_level} level."
                        ),
                        "type": "lesson_box",
                    }
                )
            else:
                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": f"You passed, but no {next_level} lessons are available.",
                    }
                )
        else:
            finish_learning_journey(subject, level)
        return

    current_lessons = get_level_lessons(subject, level)
    st.session_state.student_level = level
    if current_lessons:
        set_current_lesson(current_lessons[0])

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": (
                f"Your score is {score}%. You need more review, so you will stay "
                f"in the {level} level and repeat its lessons."
            ),
            "type": "lesson_box",
        }
    )


def render_level_test(message: dict) -> None:
    st.write(message["content"])
    questions = message.get("questions", [])
    if not questions:
        st.warning("No level test questions are available.")
        return

    test_id = message["test_id"]
    results = st.session_state.get("level_test_results", {})
    if test_id in results:
        result = results[test_id]
        if result["passed"]:
            st.success(f"Passed: {result['score']}%")
        else:
            st.warning(f"Review required: {result['score']}%")
        return

    subject = message["subject"]
    level = message["level"]
    passing_score = message.get("passing_score", 70)

    with st.form(f"level_test_{test_id}"):
        st.markdown(
            '<div class="placement-test-marker level-test-marker"></div>',
            unsafe_allow_html=True,
        )
        answers = {}
        for index, question in enumerate(questions, start=1):
            answers[question["id"]] = st.radio(
                f"{index}. {question['question']}",
                question["options"],
                index=None,
                key=f"level_test_{test_id}_{question['id']}",
            )

        submitted = st.form_submit_button(
            "Submit Level Test",
            use_container_width=True,
        )

    if not submitted:
        return

    if any(answer is None for answer in answers.values()):
        st.warning("Please answer every question before submitting the test.")
        return

    score = calculate_level_test_score(questions, answers)
    passed = score >= passing_score
    st.session_state.level_test_results[test_id] = {
        "score": score,
        "passed": passed,
    }
    _continue_after_test(subject, level, score, passed)
    st.rerun()
