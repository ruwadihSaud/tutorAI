import streamlit as st

from styles.theme import get_global_styles
from components.footer import render_footer
from components.header import render_header
from components.navigation import render_nav
from components.chat import render_chat


st.set_page_config(
    page_title="TutorAI",
    page_icon="🎓",
    layout="wide"
)

st.markdown(get_global_styles(), unsafe_allow_html=True)

# ========================= Main Layout =========================

pages = [
    st.Page("pages/Dashboard.py", title="Dashboard", icon="🎯"),
    st.Page("pages/My_Learning.py", title="My Learning", icon="📖", default=True),
    st.Page("pages/contact.py", title="Contact Us", icon="📧"),
    st.Page("pages/Help.py", title="Help", icon="🛟"),
]

selected_page = st.navigation(pages, position="sidebar")

# ========================= Main Layout =========================

main_col ,chat_col = st.columns([4.0, 1.4], gap="large")

with main_col:
    render_header()

    st.divider()

    selected_page.run()

with chat_col:
    st.markdown('<div class="chat-sticky-marker"></div>', unsafe_allow_html=True)
    render_chat()

render_footer()