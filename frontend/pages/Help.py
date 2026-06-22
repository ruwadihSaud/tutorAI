import streamlit as st


st.markdown(
    """<div class="page-title">
<h2>Frequently Asked Questions</h2>
</div>""",
    unsafe_allow_html=True,
)

questions = (
    (
        "How do I start a Learning Journey?",
        "Open My Learning, press Start, then choose the subject you want to study.",
    ),
    (
        "How is my starting level selected?",
        "TutorAI gives you a short placement test and assigns Beginner, "
        "Intermediate, or Advanced based on your score.",
    ),
    (
        "How do I move to the next lesson?",
        "Read the current lesson, then press I Understand - Continue. "
        "TutorAI will open the next lesson in order.",
    ),
    (
        "Can I ask TutorAI to explain the lesson?",
        "Yes. Ask for an explanation in the chat. You can also ask for a simpler "
        "explanation or request a video.",
    ),
    (
        "How do I take a quiz for the current lesson?",
        "Ask TutorAI for a quiz. The questions will be selected from the question "
        "bank for the lesson you are currently studying.",
    ),
    (
        "What happens after I complete a level?",
        "TutorAI gives you a level test. If you pass, you move to the next level. "
        "If you do not pass, you review the lessons in the same level.",
    ),
    (
        "What happens after I complete the Advanced level?",
        "TutorAI completes your current journey and lets you start a new Learning "
        "Journey with another subject.",
    ),
)

with st.container(border=True):
    st.markdown('<div class="help-faq-marker"></div>', unsafe_allow_html=True)

    for question, answer in questions:
        with st.expander(question):
            st.write(answer)
