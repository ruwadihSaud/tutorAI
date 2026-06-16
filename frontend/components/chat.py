# frontend/components/chat.py

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"


def initialize_chat():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "I am TutorAI. Are you ready for your Learning Journey?"
            }
        ]

    if "pending_user_message" not in st.session_state:
        st.session_state.pending_user_message = None

    if "journey_started" not in st.session_state:
        st.session_state.journey_started = False


def get_backend_response(user_message: str) -> str:
    try:
        response = requests.post(
            API_URL,
            json={"message": user_message},
            timeout=180,
        )
        response.raise_for_status()
        data = response.json()

        return data.get("reply", "No reply received from backend.")

    except requests.exceptions.ConnectionError:
        return "Cannot connect to TutorAI backend. Make sure FastAPI is running."

    except requests.exceptions.Timeout:
        return "TutorAI is still waiting for Ollama. If this is the first request, the model may still be loading."

    except requests.exceptions.RequestException as e:
        return f"Backend connection error: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"


def start_journey():
    start_message = "Start my learning journey"
    st.session_state.journey_started = True
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": start_message,
        }
    )
    st.session_state.pending_user_message = start_message
    st.rerun()


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
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            if not st.session_state.journey_started and not st.session_state.pending_user_message:
                st.button(
                    "Start",
                    use_container_width=True,
                    key="start_journey_button",
                    on_click=start_journey,
                )

            pending_user_message = st.session_state.pending_user_message
            if pending_user_message:
                with st.chat_message("assistant"):
                    with st.spinner("TutorAI is thinking..."):
                        assistant_reply = get_backend_response(pending_user_message)

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_reply,
                    }
                )
                st.session_state.pending_user_message = None
                st.rerun()

        if not st.session_state.journey_started:
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
