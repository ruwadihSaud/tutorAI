import streamlit as st


PAGE_TITLES = {
    "Dashboard": "Dashboard",
    "My_Learning": "My Learning",
    "QandA": "Q&A",
    "Help": "Help"
}


PAGE_DESCRIPTIONS = {
    "Dashboard": "Track your progress, scores, and recommended revision areas.",
    "My_Learning": "View your learning plan, lessons, mini-tests, and feedback.",
    "QandA": "Ask questions and review previous learning discussions.",
    "Help": "Learn how to use TutorAI effectively."
}


def render_page_title():
    current_page = st.session_state.current_page

    page_title = PAGE_TITLES.get(current_page, "My Learning")
    page_description = PAGE_DESCRIPTIONS.get(
        current_page,
        "Manage your personalized learning experience."
    )

    st.markdown(
        f"""
        <div class="page-title">
            <h2>{page_title}</h2>
            <p>{page_description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )