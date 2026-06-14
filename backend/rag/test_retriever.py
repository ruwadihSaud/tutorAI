# test_retriever.py

from backend.rag.lesson_retriever import retrieve_lesson


def test_query(user_message: str, current_lesson_id: str | None = None):
    lesson = retrieve_lesson(
        user_message=user_message,
        current_lesson_id=current_lesson_id
    )

    print("=" * 70)
    print("User message:", user_message)
    print("Current lesson ID:", current_lesson_id)

    if lesson is None:
        print("Retrieved lesson: None")
        return

    print("Retrieved lesson ID:", lesson.get("id"))
    print("Title:", lesson.get("title"))
    print("Level:", lesson.get("level"))
    print("Chapter:", lesson.get("chapter"))
    print("Method:", lesson.get("retrieval_method"))
    print("Score:", lesson.get("retrieval_score"))


test_query(
    user_message="اشرح لي هذا الدرس",
    current_lesson_id="lesson_03_regression"
)

test_query(
    user_message="explain classification",
    current_lesson_id="lesson_03_regression"
)

test_query(
    user_message="summarize supervised learning",
    current_lesson_id="lesson_03_regression"
)

test_query(
    user_message="اعمل اختبار عن overfitting",
    current_lesson_id="lesson_03_regression"
)

test_query(
    user_message="explain clustering",
    current_lesson_id="lesson_03_regression"
)

test_query(
    user_message="اشرح لي موضوع غير موجود",
    current_lesson_id= None
)