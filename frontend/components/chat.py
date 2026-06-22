# frontend/components/chat.py

import requests
import streamlit as st

from learning_journey.explanation_check import render_explanation_check
from learning_journey.level_test import finish_learning_journey, render_level_test
from learning_journey.lesson_box import render_lesson_box
from learning_journey.lesson_data import get_subjects
from learning_journey.placement_test import render_placement_test


API_URL = "http://127.0.0.1:8000/chat"
PLACEMENT_TEST_URL = "http://127.0.0.1:8000/placement-test"
LEVEL_TEST_URL = "http://127.0.0.1:8000/level-test"


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
            for message in st.session_state.chat_messages:
                if message.get("type") == "journey_complete":
                    with st.chat_message("assistant"):
                        completion_message = message.get("completion_message")
                        if completion_message:
                            st.success(completion_message)
                        st.write(message["content"])
                        st.button(
                            "Start New Journey",
                            use_container_width=False,
                            key="restart_learning_journey_button",
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
                                key="start_journey_button",
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
                                            key=f"subject_button_{subject}",
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
