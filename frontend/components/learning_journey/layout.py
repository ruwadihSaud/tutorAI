from html import escape

import streamlit as st

from components.learning_journey.lesson_data import calculate_progress


def render_page_title() -> None:
    st.markdown(
        """<div class="page-title">
<h2>My Learning</h2>
<p>Start your guided TutorAI learning journey and move step by step.</p>
</div>""",
        unsafe_allow_html=True,
    )


def render_status_cards() -> None:
    progress_percent = int(calculate_progress() * 100)
    subject = st.session_state.selected_subject or "Not selected"
    level = st.session_state.student_level or "Not assigned"
    stage = st.session_state.student_stage.replace("_", " ").title()

    st.markdown(
        f"""<div class="tutorai-card">
<div class="tutorai-section-title">Learning Journey Status</div>
<div class="tutorai-title-meta">
<span><strong>Stage:</strong> {escape(stage)}</span>
<span><strong>Subject:</strong> {escape(subject)}</span>
<span><strong>Level:</strong> {escape(level)}</span>
<span><strong>Progress:</strong> {progress_percent}%</span>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.progress(calculate_progress())
