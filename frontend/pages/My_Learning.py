# frontend/pages/My_Learning.py

from html import escape
from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.data.lesson_loader import (
    load_lessons,
    get_lesson_by_order,
    get_first_lesson_order,
    get_last_lesson_order,
)


lessons = load_lessons()

first_order = get_first_lesson_order()
last_order = get_last_lesson_order()

if "current_lesson_order" not in st.session_state:
    st.session_state.current_lesson_order = first_order

current_lesson = get_lesson_by_order(st.session_state.current_lesson_order)

if current_lesson is None:
    st.session_state.current_lesson_order = first_order
    current_lesson = get_lesson_by_order(first_order)


# Important:
# The chat will send only current_lesson_id to the backend.
# The backend will use this ID to retrieve the full lesson information.
st.session_state.current_lesson_id = current_lesson["id"]
st.session_state.current_lesson_title = current_lesson["title"]


progress_value = current_lesson["order"] / last_order


lesson_title = escape(current_lesson["title"])
lesson_subject = escape(current_lesson["subject"])
lesson_level = escape(current_lesson["level"])
lesson_chapter = escape(current_lesson["chapter"])
lesson_section = escape(current_lesson["section"])
lesson_content = escape(current_lesson["content"])


st.markdown(
    f"""<div class="page-title">
<h2>My Learning</h2>
<div class="tutorai-title-meta">
<span><strong>Chapter:</strong> {lesson_chapter}</span>
<span><strong>Subject:</strong> {lesson_subject}</span>
<span><strong>Level:</strong> {lesson_level}</span>
</div>
<p>Follow your lessons step by step.</p>
</div>""",
    unsafe_allow_html=True
)


st.progress(progress_value)


st.markdown(
    f"""<div class="tutorai-card">
<div class="tutorai-section-title">Lesson {current_lesson["order"]}: {lesson_title}</div>
<hr>
<p class="lesson-content">{lesson_content}</p>
</div>""",
    unsafe_allow_html=True
)


prev_col, next_col = st.columns(2)

with prev_col:
    if st.button(
        "Previous Lesson",
        use_container_width=True,
        disabled=st.session_state.current_lesson_order == first_order
    ):
        st.session_state.current_lesson_order -= 1
        st.rerun()

with next_col:
    if st.button(
        "Next Lesson",
        use_container_width=True,
        disabled=st.session_state.current_lesson_order == last_order
    ):
        st.session_state.current_lesson_order += 1
        st.rerun()


st.markdown(
    f"""<div class="tutorai-card">
<div class="tutorai-section-title">Current Learning Status</div>
<div class="tutorai-muted tutorai-lesson-meta">
You are currently studying lesson {current_lesson["order"]} of {last_order}.
Ask TutorAI to summarize this lesson, explain it, or generate a quiz from it.
</div>
</div>""",
    unsafe_allow_html=True
)
