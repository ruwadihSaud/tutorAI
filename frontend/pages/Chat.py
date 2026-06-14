import streamlit as st

from components.chat import render_chat


st.markdown(
    """<div class="page-title">
<h2>TutorAI Chat</h2>
<p>Ask TutorAI to summarize, explain, quiz you, or help with your current lesson.</p>
</div>""",
    unsafe_allow_html=True
)

render_chat(
    chat_height=560,
    show_header=False,
    title="Conversation",
    caption="Continue your learning conversation with TutorAI.",
)
