import streamlit as st


def _resolve_check(check_id: str) -> None:
    if "resolved_explanation_checks" not in st.session_state:
        st.session_state.resolved_explanation_checks = []

    if check_id not in st.session_state.resolved_explanation_checks:
        st.session_state.resolved_explanation_checks.append(check_id)


def continue_current_lesson(check_id: str) -> None:
    _resolve_check(check_id)
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": "I understand the explanation.",
        }
    )
    st.session_state.chat_messages = [
        message
        for message in st.session_state.chat_messages
        if message.get("type") != "lesson_box"
    ]
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": "Great. Continue with your current lesson.",
            "type": "lesson_box",
        }
    )


def request_more_explanation(check_id: str) -> None:
    _resolve_check(check_id)
    follow_up = (
        "I still do not understand this point. Explain it more simply, "
        "step by step, using a different practical example."
    )
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": "I need a simpler explanation.",
        }
    )
    st.session_state.pending_user_message = follow_up


def render_explanation_check(message: dict) -> None:
    st.write(message["content"])

    check_id = message["check_id"]
    resolved_checks = st.session_state.get("resolved_explanation_checks", [])

    if check_id in resolved_checks:
        return

    st.caption("Did you understand the explanation?")
    understood_col, explain_more_col = st.columns(2)

    with understood_col:
        if st.button(
            "I Understand",
            use_container_width=True,
            key=f"understood_{check_id}",
        ):
            continue_current_lesson(check_id)
            st.rerun()

    with explain_more_col:
        if st.button(
            "Explain More",
            use_container_width=True,
            key=f"explain_more_{check_id}",
        ):
            request_more_explanation(check_id)
            st.rerun()
