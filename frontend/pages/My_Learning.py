# frontend/pages/My_Learning.py

from html import escape

import streamlit as st

from data.lesson_loader import (
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

# مهم: هذا المحتوى راح يستخدمه الشات للتلخيص والاختبار
st.session_state.current_lesson_content = current_lesson["content"]
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
<p style="color:#000000; font-size:15px; line-height:1.7;">{lesson_content}</p>
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
Ask TutorAI to summarize this lesson or generate a quiz from it.
</div>
</div>""",
    unsafe_allow_html=True
)
