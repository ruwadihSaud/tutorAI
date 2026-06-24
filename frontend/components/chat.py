# frontend/components/chat.py

from html import escape

import requests
import streamlit as st

from learning_journey.explanation_check import render_explanation_check
from learning_journey.level_test import finish_learning_journey, render_level_test
from learning_journey.lesson_box import render_lesson_box
from learning_journey.lesson_data import get_subjects
from learning_journey.lesson_quiz import render_lesson_quiz
from learning_journey.placement_test import render_placement_test


API_URL = "http://127.0.0.1:8000/chat"
PLACEMENT_TEST_URL = "http://127.0.0.1:8000/placement-test"
LEVEL_TEST_URL = "http://127.0.0.1:8000/level-test"


def render_progress_report(message: dict) -> None:
    progress = message.get("progress") or {}
    subject = progress.get("subject", "Not selected")
    level = progress.get("level", "Not started")
    current_lesson = progress.get("current_lesson", "No lesson selected")
    completed_count = progress.get("completed_count", 0)
    total_lessons = progress.get("total_lessons", 0)
    remaining_count = progress.get("remaining_count", 0)
    progress_percent = progress.get("progress_percent", 0)
    placement_score = progress.get("placement_score")
    level_test_score = progress.get("level_test_score")

    st.markdown(
        f"""
        <div class="progress-report-card">
            <div class="progress-report-kicker">TutorAI Progress</div>
            <div class="progress-report-title">{escape(subject)}</div>
            <div class="progress-report-subtitle">
                Level: <strong>{escape(level)}</strong>
            </div>
            <div class="progress-report-bar">
                <div style="width: {progress_percent}%"></div>
            </div>
            <div class="progress-report-percent">{progress_percent}% complete</div>
            <div class="progress-report-grid">
                <div>
                    <span>Completed</span>
                    <strong>{completed_count}/{total_lessons}</strong>
                </div>
                <div>
                    <span>Remaining</span>
                    <strong>{remaining_count}</strong>
                </div>
            </div>
            <div class="progress-report-lesson">
                <span>Current lesson</span>
                <strong>{escape(current_lesson)}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_columns = st.columns(2)
    with score_columns[0]:
        st.caption(
            "Placement score: "
            + (f"{placement_score}%" if placement_score is not None else "Not taken")
        )
    with score_columns[1]:
        st.caption(
            "Level test score: "
            + (f"{level_test_score}%" if level_test_score is not None else "Not taken")
        )

    st.markdown(
        '<div class="continue-journey-button-wrap"></div>',
        unsafe_allow_html=True,
    )
    if st.button(
        "Continue my Learning Journey",
        use_container_width=True,
        key=f"continue_from_progress_{message.get('progress_id', 'current')}",
    ):
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": "Continue my Learning Journey.",
            }
        )
        st.session_state.chat_messages = [
            chat_message
            for chat_message in st.session_state.chat_messages
            if chat_message.get("type") != "lesson_box"
        ]
        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": "Continue with your current lesson.",
                "type": "lesson_box",
            }
        )
        st.rerun()


def initialize_chat():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "I am TutorAI. Are you ready for your Learning Journey?",
                "type": "start_prompt"
            }
        ]

    if "pending_user_message" not in st.session_state:
        st.session_state.pending_user_message = None

    if "journey_started" not in st.session_state:
        st.session_state.journey_started = False

    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = None

    if "pending_placement_subject" not in st.session_state:
        st.session_state.pending_placement_subject = None

    if "placement_score" not in st.session_state:
        st.session_state.placement_score = None

    if "student_level" not in st.session_state:
        st.session_state.student_level = None

    if "resolved_explanation_checks" not in st.session_state:
        st.session_state.resolved_explanation_checks = []

    if "pending_level_test" not in st.session_state:
        st.session_state.pending_level_test = None

    if "level_test_results" not in st.session_state:
        st.session_state.level_test_results = {}

    if "level_test_score" not in st.session_state:
        st.session_state.level_test_score = None

    if "lesson_quiz_results" not in st.session_state:
        st.session_state.lesson_quiz_results = {}

    if "learning_completed" not in st.session_state:
        st.session_state.learning_completed = False

    for message in st.session_state.chat_messages:
        if (
            message.get("type") == "journey_complete"
            and "completion_message" not in message
        ):
            message["completion_message"] = message.get("content", "")
            message["content"] = "Are you ready for another Learning Journey?"

    if st.session_state.learning_completed:
        completed_subject = st.session_state.selected_subject or "your subject"
        completed_level = st.session_state.student_level or "Advanced"
        finish_learning_journey(completed_subject, completed_level)


def get_backend_response(user_message: str) -> dict:
    try:
        response = requests.post(
            API_URL,
            json={
                "message": user_message,
                "lesson_id": st.session_state.get("current_lesson_id"),
                "current_lesson_id": st.session_state.get("current_lesson_id"),
                "selected_subject": st.session_state.get("selected_subject"),
                "student_level": st.session_state.get("student_level"),
                "completed_lessons": st.session_state.get("completed_lessons", []),
                "placement_score": st.session_state.get("placement_score"),
                "level_test_score": st.session_state.get("level_test_score"),
            },
            timeout=180,
        )
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.ConnectionError:
        return {
            "reply": "Cannot connect to TutorAI backend. Make sure FastAPI is running.",
            "response_type": "message",
        }

    except requests.exceptions.Timeout:
        return {
            "reply": "TutorAI model took too long to respond. Please try again.",
            "response_type": "message",
        }

    except requests.exceptions.RequestException as e:
        return {
            "reply": f"Backend connection error: {e}",
            "response_type": "message",
        }

    except Exception as e:
        return {
            "reply": f"Unexpected error: {e}",
            "response_type": "message",
        }


def get_placement_test(subject: str) -> dict:
    try:
        response = requests.post(
            PLACEMENT_TEST_URL,
            json={"subject": subject},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "reply": f"Could not load the placement test: {e}",
            "subject": subject,
            "questions": [],
        }


def get_level_test(subject: str, level: str) -> dict:
    try:
        response = requests.post(
            LEVEL_TEST_URL,
            json={"subject": subject, "level": level},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "reply": f"Could not load the level test: {e}",
            "subject": subject,
            "level": level,
            "questions": [],
            "passing_score": 70,
        }


def start_journey():
    start_message = "Let's start my learning journey 🚀"
    st.session_state.journey_started = True
    st.session_state.chat_messages = [
        message
        for message in st.session_state.chat_messages
        if message.get("type") != "journey_complete"
    ]
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": start_message,
        }
    )
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": "What subject would you like to study?",
            "type": "subject_selection",
        }
    )


def select_subject(subject: str):
    st.session_state.selected_subject = subject
    st.session_state.placement_score = None
    st.session_state.student_level = None
    st.session_state.pending_level_test = None
    st.session_state.level_test_results = {}
    st.session_state.level_test_score = None
    st.session_state.learning_completed = False
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": subject,
        }
    )
    st.session_state.pending_placement_subject = subject


def render_chat(
    chat_height: int = 360,
    show_header: bool = True,
    title: str = "TutorAI Chat",
    caption: str = "Ask questions about your current lesson.",
):
    initialize_chat()

    with st.container(border=True):
        st.markdown('<div class="chat-card-marker"></div>', unsafe_allow_html=True)

        if show_header:
            st.markdown(f"### {title}")
            st.caption(caption)
            st.divider()

        chat_area = st.container(height=chat_height)

        with chat_area:
            for message_index, message in enumerate(st.session_state.chat_messages):
                if message.get("type") == "journey_complete":
                    with st.chat_message("assistant"):
                        completion_message = message.get("completion_message")
                        if completion_message:
                            st.success(completion_message)
                        st.write(message["content"])
                        st.button(
                            "Start New Journey",
                            use_container_width=False,
                            key=f"restart_learning_journey_button_{message_index}",
                            on_click=start_journey,
                        )
                    continue

                if message.get("type") == "start_prompt":
                    with st.chat_message("assistant"):
                        st.write(message["content"])

                        if not st.session_state.journey_started:
                            st.markdown('<div class="start-button-wrap">', unsafe_allow_html=True)
                            st.button(
                                "Start",
                                use_container_width=False,
                                key=f"start_journey_button_{message_index}",
                                on_click=start_journey,
                            )
                            st.markdown('</div>', unsafe_allow_html=True)
                    continue

                if message.get("type") == "subject_selection":
                    with st.chat_message("assistant"):
                        st.write(message["content"])

                        if not st.session_state.selected_subject:
                            subjects = get_subjects()

                            if subjects:
                                subject_columns = st.columns(len(subjects))

                                for column, subject in zip(subject_columns, subjects):
                                    with column:
                                        st.button(
                                            subject,
                                            use_container_width=True,
                                            key=(
                                                f"subject_button_{message_index}_{subject}"
                                            ),
                                            on_click=select_subject,
                                            args=(subject,),
                                        )
                            else:
                                st.warning("No subjects are available.")
                    continue

                if message.get("type") == "placement_test":
                    with st.chat_message("assistant"):
                        render_placement_test(message)
                    continue

                if message.get("type") == "lesson_box":
                    with st.chat_message("assistant"):
                        st.write(message["content"])
                        render_lesson_box()
                    continue

                if message.get("type") == "explanation_check":
                    with st.chat_message("assistant"):
                        render_explanation_check(message)
                    continue

                if message.get("type") == "level_test":
                    with st.chat_message("assistant"):
                        render_level_test(message)
                    continue

                if message.get("type") == "lesson_quiz":
                    with st.chat_message("assistant"):
                        render_lesson_quiz(message)
                    continue

                if message.get("type") == "progress_report":
                    with st.chat_message("assistant"):
                        render_progress_report(message)
                    continue

                with st.chat_message(message["role"]):
                    st.write(message["content"])

            pending_placement_subject = st.session_state.pending_placement_subject
            if pending_placement_subject:
                with st.chat_message("assistant"):
                    with st.spinner("Preparing your placement test..."):
                        placement_test = get_placement_test(pending_placement_subject)

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": placement_test.get("reply", "Placement test"),
                        "type": "placement_test",
                        "subject": placement_test.get(
                            "subject",
                            pending_placement_subject,
                        ),
                        "questions": placement_test.get("questions", []),
                    }
                )
                st.session_state.pending_placement_subject = None
                st.rerun()

            pending_level_test = st.session_state.pending_level_test
            if pending_level_test:
                subject = pending_level_test["subject"]
                level = pending_level_test["level"]
                with st.chat_message("assistant"):
                    with st.spinner("Preparing your level test..."):
                        level_test = get_level_test(subject, level)

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": level_test.get("reply", "Level test"),
                        "type": "level_test",
                        "test_id": (
                            f"{subject}_{level}_{len(st.session_state.chat_messages)}"
                        ),
                        "subject": level_test.get("subject", subject),
                        "level": level_test.get("level", level),
                        "questions": level_test.get("questions", []),
                        "passing_score": level_test.get("passing_score", 70),
                    }
                )
                st.session_state.pending_level_test = None
                st.rerun()

            pending_user_message = st.session_state.pending_user_message
            if pending_user_message:
                with st.chat_message("assistant"):
                    with st.spinner("TutorAI is thinking..."):
                        backend_response = get_backend_response(pending_user_message)

                assistant_message = {
                    "role": "assistant",
                    "content": backend_response.get(
                        "reply",
                        "No reply received from backend.",
                    ),
                }

                reply_text = assistant_message["content"]
                is_error_reply = (
                    reply_text.startswith("LLM service error:")
                    or reply_text.startswith("LLM configuration error:")
                    or reply_text.startswith("Gemini configuration error:")
                    or reply_text.startswith("Gemini connection error:")
                    or reply_text.startswith("Unexpected response format from Gemini.")
                    or reply_text.startswith("Ollama connection error:")
                    or reply_text.startswith("Backend connection error:")
                    or reply_text.startswith("Cannot connect to TutorAI backend.")
                    or reply_text.startswith("TutorAI model took too long to respond.")
                    or reply_text.startswith("Unexpected response format from Ollama.")
                )

                if (
                    backend_response.get("response_type") == "explanation_check"
                    and not is_error_reply
                ):
                    assistant_message["type"] = "explanation_check"
                    assistant_message["explanation_request"] = pending_user_message
                    assistant_message["explanation_scope"] = backend_response.get(
                        "explanation_scope",
                        "specific_topic",
                    )
                    assistant_message["check_id"] = (
                        f"explanation_{len(st.session_state.chat_messages)}"
                    )

                if (
                    backend_response.get("response_type") == "lesson_quiz"
                    and not is_error_reply
                ):
                    assistant_message["type"] = "lesson_quiz"
                    assistant_message["lesson_id"] = backend_response.get("lesson_id")
                    assistant_message["questions"] = backend_response.get(
                        "questions",
                        [],
                    )
                    assistant_message["quiz_id"] = (
                        f"lesson_quiz_{len(st.session_state.chat_messages)}"
                    )

                if (
                    backend_response.get("response_type") == "progress_report"
                    and not is_error_reply
                ):
                    assistant_message["type"] = "progress_report"
                    assistant_message["progress"] = backend_response.get("progress", {})
                    assistant_message["progress_id"] = (
                        f"progress_{len(st.session_state.chat_messages)}"
                    )

                st.session_state.chat_messages.append(assistant_message)
                st.session_state.pending_user_message = None
                st.rerun()

        if not st.session_state.journey_started:
            return

        if not st.session_state.selected_subject:
            return

        if st.session_state.placement_score is None:
            return

        if user_input := st.chat_input("Ask TutorAI..."):
            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )
            st.session_state.pending_user_message = user_input
            st.rerun()
