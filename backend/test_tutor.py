# test_tutor_rag.py

from backend.tutor import detect_intent, generate_tutor_reply
from backend.rag.lesson_retriever import retrieve_lesson


def test_message(user_message: str, current_lesson_id: str | None = None):
    print("=" * 80)
    print("User message:", user_message)
    print("Current lesson ID:", current_lesson_id)

    intent = detect_intent(user_message)
    print("Detected intent:", intent)

    lesson = retrieve_lesson(
        user_message=user_message,
        current_lesson_id=current_lesson_id
    )

    if lesson:
        print("Retrieved lesson ID:", lesson.get("id"))
        print("Title:", lesson.get("title"))
        print("Method:", lesson.get("retrieval_method"))
        print("Score:", lesson.get("retrieval_score"))
    else:
        print("Retrieved lesson: None")

    print("-" * 80)
    reply = generate_tutor_reply(
        user_message=user_message,
        lesson_id=current_lesson_id
    )

    print("TutorAI reply:")
    print(reply)


test_message(
    user_message="اشرح لي هذا الدرس",
    current_lesson_id="lesson_03_regression"
)

test_message(
    user_message="explain classification",
    current_lesson_id="lesson_03_regression"
)

test_message(
    user_message="summarize supervised learning",
    current_lesson_id="lesson_03_regression"
)

test_message(
    user_message="اعمل اختبار عن overfitting",
    current_lesson_id="lesson_03_regression"
)

test_message(
    user_message="help me",
    current_lesson_id=None
)

test_message(
    user_message="اشرح لي موضوع غير موجود",
    current_lesson_id=None
)