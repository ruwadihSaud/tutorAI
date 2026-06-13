import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

def initialize_chat():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello! I am TutorAI. Tell me your learning goal."
            }
        ]


def get_backend_response(user_message: str) -> str:
    try:
        response = requests.post(
            API_URL,
            json={"message": user_message},
            timeout=10
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


def render_chat():
    initialize_chat()

    with st.container(border=True):
        st.markdown('<div class="chat-card-marker"></div>', unsafe_allow_html=True)

        st.markdown("### TutorAI Chat")
        st.caption("Ask questions about your learning journey.")

        st.divider()

        chat_area = st.container(height=360)

        with chat_area:
            for message in st.session_state.chat_messages:
                if message["role"] == "assistant":
                    st.markdown(
                        f"""
                        <div class="chat-message assistant-message">
                            <strong>TutorAI</strong><br>
                            {message["content"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-message user-message">
                            <strong>You</strong><br>
                            {message["content"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Message",
                placeholder="Ask TutorAI...",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button("Send", use_container_width=True)

            if submitted and user_input.strip():
                st.session_state.chat_messages.append(
                    {
                        "role": "user",
                        "content": user_input
                    }
                )

                assistant_reply = get_backend_response(user_input)

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_reply
                    }
                )

                st.rerun()