import streamlit as st


def render_header():
    st.markdown(
    """
    <div class="tutorai-header">
        <h1>TutorAI</h1>
        <p>An Adaptive AI Tutoring Agent for Personalized Learning</p>
    </div>
    """,
    unsafe_allow_html=True
)