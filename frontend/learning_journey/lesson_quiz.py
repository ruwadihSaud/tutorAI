import streamlit as st


def continue_learning_journey(quiz_id: str) -> None:
    result = st.session_state.lesson_quiz_results[quiz_id]
    result["continued"] = True
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": "Continue my Learning Journey.",
        }
    )
    st.session_state.chat_messages = [
        message
        for message in st.session_state.chat_messages
        if message.get("type") != "lesson_box"
    ]
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": "Continue with your current lesson.",
            "type": "lesson_box",
        }
    )


def render_lesson_quiz(message: dict) -> None:
    st.write(message["content"])

    questions = message.get("questions", [])
    if not questions:
        st.warning("No quiz questions are available for this lesson.")
        return

    quiz_id = message["quiz_id"]
    result = st.session_state.lesson_quiz_results.get(quiz_id)

    if result:
        st.success(
            f"Quiz complete: {result['score']}% "
            f"({result['correct']}/{result['total']} correct)"
        )
        if not result.get("continued"):
            st.markdown(
                '<div class="continue-journey-button-wrap"></div>',
                unsafe_allow_html=True,
            )
            if st.button(
                "Continue my Learning Journey",
                use_container_width=True,
                key=f"continue_journey_{quiz_id}",
            ):
                continue_learning_journey(quiz_id)
                st.rerun()
        return

    with st.form(f"lesson_quiz_{quiz_id}"):
        st.markdown(
            '<div class="placement-test-marker lesson-quiz-marker"></div>',
            unsafe_allow_html=True,
        )
        answers = {}

        for index, question in enumerate(questions, start=1):
            answers[question["id"]] = st.radio(
                f"{index}. {question['question']}",
                question["options"],
                index=None,
                key=f"lesson_quiz_{quiz_id}_{question['id']}",
            )

        submitted = st.form_submit_button(
            "Submit Quiz",
            use_container_width=True,
        )

    if not submitted:
        return

    if any(answer is None for answer in answers.values()):
        st.warning("Please answer every question before submitting the quiz.")
        return

    correct = sum(
        answers[question["id"]] == question["correct_answer"]
        for question in questions
    )
    total = len(questions)
    score = round((correct / total) * 100)
    st.session_state.lesson_quiz_results[quiz_id] = {
        "score": score,
        "correct": correct,
        "total": total,
    }
    st.rerun()
