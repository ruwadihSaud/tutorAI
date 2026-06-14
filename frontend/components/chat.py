# frontend/components/Chat.py

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat"


def initialize_chat():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello! I am TutorAI. Ask me to summarize, explain, or quiz you on the current lesson."
            }
        ]


def get_backend_response(user_message: str, lesson_id: str | None) -> str:
    try:
        payload = {
            "message": user_message,
            "lesson_id": lesson_id,
        }

        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get("reply", "No reply received from backend.")

        return f"Backend error: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "Cannot connect to TutorAI backend. Make sure FastAPI is running."

    except requests.exceptions.Timeout:
        return "TutorAI backend took too long to respond."

    except Exception as e:
        return f"Unexpected error: {e}"


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

        if user_input := st.chat_input("Ask TutorAI..."):
            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            lesson_id = st.session_state.get("current_lesson_id")
            assistant_reply = get_backend_response(user_input, lesson_id)

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

            st.rerun()
