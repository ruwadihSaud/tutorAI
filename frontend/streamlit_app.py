from pathlib import Path
import sys

import streamlit as st

from styles.theme import get_global_styles
from components.footer import render_footer
from components.header import render_header
from components.chat import render_chat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.data.lesson_loader import get_first_lesson_order, get_lesson_by_order


st.set_page_config(
    page_title="TutorAI",
    page_icon=":books:",
    layout="wide"
)

st.markdown(get_global_styles(), unsafe_allow_html=True)


if "current_lesson_id" not in st.session_state:
    first_lesson = get_lesson_by_order(get_first_lesson_order())

    if first_lesson:
        st.session_state.current_lesson_id = first_lesson["id"]
        st.session_state.current_lesson_title = first_lesson["title"]


pages = [
    st.Page("pages/My_Learning.py", title="My Learning", icon=":material/menu_book:", default=True),
    st.Page("pages/Dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    st.Page("pages/contact.py", title="Contact Us", icon=":material/mail:"),
    st.Page("pages/Help.py", title="Help", icon=":material/help:"),
]

selected_page = st.navigation(pages, position="sidebar")


if selected_page.title == "My Learning":
    render_header()
    st.divider()
    selected_page.run()
else:
    main_col, chat_col = st.columns([4.0, 1.4], gap="large")

    with main_col:
        render_header()
        st.divider()
        selected_page.run()

    with chat_col:
        st.markdown('<div class="chat-sticky-marker"></div>', unsafe_allow_html=True)
        render_chat()

render_footer()
