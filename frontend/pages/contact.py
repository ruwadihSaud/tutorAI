import re

import streamlit as st


def _is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email))


with st.container(border=True):
    st.markdown(
        """<div class="tutorai-card contact-card-marker"></div>
<div class="page-title contact-page-title">
<h2>Contact Information</h2>
<p>Choose the right support topic and send the TutorAI team a clear message.</p>
</div>""",
        unsafe_allow_html=True,
    )

    support_columns = st.columns(3, gap="medium")
    support_topics = (
        (
            "Learning Support",
            "Questions about lessons, quizzes, explanations, or your learning journey.",
        ),
        (
            "Technical Support",
            "Report an error or a problem with the interface, chat, or lesson content.",
        ),
        (
            "Feedback",
            "Share an idea that could make TutorAI clearer and more useful.",
        ),
    )

    for column, (title, description) in zip(support_columns, support_topics):
        with column:
            st.markdown(
                f"""<div class="contact-topic">
<strong>{title}</strong>
<p>{description}</p>
</div>""",
                unsafe_allow_html=True,
            )

    st.divider()
    st.markdown('<div class="contact-form-title">Send a message</div>', unsafe_allow_html=True)

    with st.form("contact_form", clear_on_submit=True, border=False):
        st.markdown('<div class="contact-form-marker"></div>', unsafe_allow_html=True)
        name_column, email_column = st.columns(2)

        with name_column:
            name = st.text_input("Name", placeholder="Your name")

        with email_column:
            email = st.text_input("Email", placeholder="name@example.com")

        topic = st.selectbox(
            "Topic",
            ["Learning Support", "Technical Support", "Feedback"],
        )
        message = st.text_area(
            "Message",
            placeholder="Describe your question or issue...",
            height=150,
        )
        submitted = st.form_submit_button("Prepare Message", use_container_width=True)

if submitted:
    clean_name = name.strip()
    clean_email = email.strip()
    clean_message = message.strip()

    if not clean_name or not clean_email or not clean_message:
        st.error("Please complete your name, email, and message.")
    elif not _is_valid_email(clean_email):
        st.error("Please enter a valid email address.")
    else:
        st.session_state.contact_message = {
            "name": clean_name,
            "email": clean_email,
            "topic": topic,
            "message": clean_message,
        }
        st.success(
            "Your message is ready. External delivery can be connected when "
            "the contact backend is added."
        )
