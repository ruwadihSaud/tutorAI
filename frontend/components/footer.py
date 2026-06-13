import streamlit as st


def render_footer():
    st.markdown(
        """
        <div class="tutorai-footer">
            <span>TutorAI</span> — Adaptive AI Tutoring Agent | 2026
        </div>
        """,
        unsafe_allow_html=True
    )