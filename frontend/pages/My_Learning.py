# frontend/pages/My_Learning.py

import streamlit as st

from components.chat import render_chat


st.markdown(
    """<div class="page-title">
<h2>My Learning</h2>
<p>Start with TutorAI chat. Your learning journey will be generated from the conversation.</p>
</div>""",
    unsafe_allow_html=True,
)

render_chat(
    chat_height=620,
    show_header=False,
)
