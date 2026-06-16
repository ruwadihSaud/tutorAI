from html import escape

import streamlit as st

from components.learning_journey.lesson_data import (
    get_current_lesson,
    get_level_lessons,
    get_next_lesson,
    get_subjects,
    set_current_lesson,
)
from components.learning_journey.state import (
    PASSING_SCORE,
    determine_level,
    get_next_level,
    reset_for_subject,
    reset_journey,
)


def render_subject_selection() -> None:
    st.markdown(
        """<div class="tutorai-card">
<div class="tutorai-section-title">Choose Your Subject</div>
<p class="tutorai-muted">TutorAI will build a guided learning path after you choose a subject.</p>
</div>""",
        unsafe_allow_html=True,
    )

    subjects = get_subjects()
    selected_subject = st.radio(
        "Subject",
        subjects,
        label_visibility="collapsed",
        key="subject_selection_radio",
    )

    if st.button("Start Placement Test", use_container_width=True):
        reset_for_subject(selected_subject)
        st.rerun()


def render_placement_test() -> None:
    subject = st.session_state.selected_subject
    st.markdown(
        f"""<div class="tutorai-card">
<div class="tutorai-section-title">Placement Test</div>
<p class="tutorai-muted">Answer these quick questions so TutorAI can place you at the right level for <strong>{escape(subject or "")}</strong>.</p>
</div>""",
        unsafe_allow_html=True,
    )

    with st.form("placement_test_form"):
        q1 = st.radio(
            "How comfortable are you with the basic ideas in this subject?",
            ["I am new to it", "I know the basics", "I can explain advanced ideas"],
        )
        q2 = st.radio(
            "Can you apply this subject to solve a practical problem?",
            ["Not yet", "With guidance", "Yes, independently"],
        )
        q3 = st.radio(
            "How much support do you want from TutorAI?",
            ["Step-by-step support", "Some guidance", "Challenge me"],
        )

        submitted = st.form_submit_button("Submit Test", use_container_width=True)

    if submitted:
        score_map = {
            "I am new to it": 20,
            "I know the basics": 55,
            "I can explain advanced ideas": 90,
            "Not yet": 20,
            "With guidance": 55,
            "Yes, independently": 90,
            "Step-by-step support": 20,
            "Some guidance": 55,
            "Challenge me": 90,
        }
        score = round((score_map[q1] + score_map[q2] + score_map[q3]) / 3)
        level = determine_level(score)
        lessons = get_level_lessons(subject, level)

        st.session_state.placement_score = score
        st.session_state.student_level = level

        if lessons:
            set_current_lesson(lessons[0])

        st.session_state.student_stage = "learning"
        st.rerun()


def render_current_lesson() -> None:
    lesson = get_current_lesson()

    if not lesson:
        st.markdown(
            """<div class="tutorai-card">
<div class="tutorai-section-title">No Lessons Found</div>
<p class="tutorai-muted">TutorAI could not find lessons for this subject and level.</p>
</div>""",
            unsafe_allow_html=True,
        )
        return

    lessons = get_level_lessons(
        st.session_state.selected_subject,
        st.session_state.student_level,
    )
    completed_count = len(
        [
            item
            for item in lessons
            if item["id"] in st.session_state.completed_lessons
        ]
    )
    lesson_position = lessons.index(lesson) + 1

    set_current_lesson(lesson)

    title = escape(lesson["title"])
    subject = escape(lesson["subject"])
    level = escape(lesson["level"])
    chapter = escape(lesson["chapter"])
    section = escape(lesson["section"])
    content = escape(lesson["content"])

    st.markdown(
        f"""<div class="tutorai-card">
<div class="tutorai-section-title">Current Lesson</div>
<div class="tutorai-title-meta">
<span><strong>Lesson:</strong> {lesson_position} of {len(lessons)}</span>
<span><strong>Subject:</strong> {subject}</span>
<span><strong>Level:</strong> {level}</span>
<span><strong>Chapter:</strong> {chapter}</span>
<span><strong>Section:</strong> {section}</span>
</div>
<hr>
<h3>{title}</h3>
<p class="lesson-content">{content}</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""<div class="tutorai-card">
<div class="tutorai-section-title">Lesson Progress</div>
<p class="tutorai-muted">Completed {completed_count} of {len(lessons)} lessons in this level. Use the chat to ask about this lesson before moving on.</p>
</div>""",
        unsafe_allow_html=True,
    )

    action_col, next_col = st.columns(2)

    with action_col:
        if st.button("I Understand / تم الفهم", use_container_width=True):
            if lesson["id"] not in st.session_state.completed_lessons:
                st.session_state.completed_lessons.append(lesson["id"])

            st.session_state.lesson_ready_to_continue = True
            st.success("Lesson marked as completed.")

    with next_col:
        next_lesson = get_next_lesson(lesson)
        continue_disabled = not st.session_state.lesson_ready_to_continue

        label = "Continue to Next Lesson" if next_lesson else "Start Level Test"
        if st.button(label, use_container_width=True, disabled=continue_disabled):
            st.session_state.lesson_ready_to_continue = False

            if next_lesson:
                set_current_lesson(next_lesson)
                st.session_state.student_stage = "learning"
            else:
                st.session_state.student_stage = "level_test"

            st.rerun()


def render_level_test() -> None:
    level = st.session_state.student_level
    subject = st.session_state.selected_subject
    score = st.session_state.level_test_score

    st.markdown(
        f"""<div class="tutorai-card">
<div class="tutorai-section-title">Level Completion Test</div>
<p class="tutorai-muted">Complete this test to move beyond <strong>{escape(level or "")}</strong> in <strong>{escape(subject or "")}</strong>.</p>
</div>""",
        unsafe_allow_html=True,
    )

    if score is None:
        with st.form("level_test_form"):
            q1 = st.radio(
                "Can you summarize the main ideas from this level?",
                ["Not yet", "Partly", "Yes"],
            )
            q2 = st.radio(
                "Can you answer questions about the lessons without help?",
                ["Not yet", "Sometimes", "Yes"],
            )
            q3 = st.radio(
                "Are you ready for harder material?",
                ["No", "Maybe", "Yes"],
            )

            submitted = st.form_submit_button("Submit Test", use_container_width=True)

        if submitted:
            score_map = {
                "Not yet": 30,
                "Partly": 60,
                "Yes": 90,
                "Sometimes": 60,
                "No": 30,
                "Maybe": 60,
            }
            st.session_state.level_test_score = round(
                (score_map[q1] + score_map[q2] + score_map[q3]) / 3
            )
            st.rerun()

        return

    if score >= PASSING_SCORE:
        st.success(f"You passed with {score}%.")
        next_level = get_next_level(level)

        if next_level:
            if st.button("Move to Next Level", use_container_width=True):
                lessons = get_level_lessons(subject, next_level)
                st.session_state.student_level = next_level
                st.session_state.completed_lessons = []
                st.session_state.lesson_ready_to_continue = False
                st.session_state.level_test_score = None

                if lessons:
                    set_current_lesson(lessons[0])

                st.session_state.student_stage = "learning"
                st.rerun()
        else:
            if st.button("Finish Learning Journey", use_container_width=True):
                st.session_state.student_stage = "completed"
                st.rerun()
    else:
        st.warning(f"Your score is {score}%. TutorAI recommends revision.")
        if st.button("Review Weak Lessons", use_container_width=True):
            st.session_state.student_stage = "revision"
            st.rerun()


def render_revision() -> None:
    lessons = get_level_lessons(
        st.session_state.selected_subject,
        st.session_state.student_level,
    )
    weak_lessons = [
        lesson
        for lesson in lessons
        if lesson["id"] not in st.session_state.completed_lessons
    ] or lessons[:2]

    st.markdown(
        """<div class="tutorai-card">
<div class="tutorai-section-title">Revision Plan</div>
<p class="tutorai-muted">Review the weak or unfinished lessons, then try the level test again.</p>
</div>""",
        unsafe_allow_html=True,
    )

    for lesson in weak_lessons:
        st.markdown(
            f"""<div class="tutorai-card">
<div class="tutorai-section-title">{escape(lesson["title"])}</div>
<p class="tutorai-muted">{escape(lesson["chapter"])} - Section {escape(lesson["section"])}</p>
</div>""",
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Review Weak Lessons", use_container_width=True):
            if weak_lessons:
                set_current_lesson(weak_lessons[0])

            st.session_state.student_stage = "learning"
            st.rerun()

    with col2:
        if st.button("Start Level Test", use_container_width=True):
            st.session_state.student_stage = "level_test"
            st.rerun()


def render_completed() -> None:
    st.markdown(
        """<div class="tutorai-card">
<div class="tutorai-section-title">Journey Completed</div>
<p class="tutorai-muted">Great work. You completed all available levels for your selected subject.</p>
</div>""",
        unsafe_allow_html=True,
    )

    if st.button("Choose Another Subject", use_container_width=True):
        reset_journey()
        st.rerun()
