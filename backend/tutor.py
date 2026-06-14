# backend/tutor.py

from backend.data.lesson_loader import get_lesson_by_id
from backend.rag.lesson_retriever import retrieve_lesson

from backend.generators.summary_generator import generate_summary
from backend.generators.quiz_generator import generate_quiz
from backend.generators.explanation_generator import generate_explanation
from backend.generators.help_generator import generate_help
from backend.generators.general_generator import generate_general


# يحدد نوع الطلب من رساله الطالب 
def detect_intent(user_message: str) -> str:
    message = user_message.lower().strip()

    summary_keywords = [
        "summarize", "summary", "summarise",
        "لخص", "لخصي", "تلخيص", "اختصر", "اختصري",
        "اهم النقاط", "أهم النقاط", "الزبدة"
    ]

    quiz_keywords = [
        "quiz", "test", "exam", "questions",
        "اختبار", "اختبرني", "اسئلة", "أسئلة",
        "سوي اختبار", "اعمل اختبار", "تدريب"
    ]

    explanation_keywords = [
        "explain", "explanation", "teach", "understand",
        "اشرح", "شرح", "فسر", "وضح", "فهمني",
        "ما فهمت"
    ]

    help_keywords = [
        "help", "support", "مساعدة", "ساعدني",
        "وش اقدر اسوي", "كيف استخدم"
    ]

    if any(keyword in message for keyword in summary_keywords):
        return "summary"

    if any(keyword in message for keyword in quiz_keywords):
        return "quiz"

    if any(keyword in message for keyword in explanation_keywords):
        return "explanation"

    if any(keyword in message for keyword in help_keywords):
        return "help"

    return "general"


def generate_tutor_reply(user_message: str,lesson_id: str | None = None) -> str:
    """
    Main TutorAI router.

    1. Detect the student intent.
    2. Use RAG to retrieve the relevant lesson.
    3. Send the lesson to the correct generator.
    """

    intent = detect_intent(user_message)

    if intent == "help":
        return generate_help(user_message)

    if intent == "general":
        return generate_general(user_message)

    lesson = retrieve_lesson(
        user_message=user_message,
        current_lesson_id=lesson_id
    )

    if lesson is None:
        return (
            "I could not find a suitable lesson for your request. "
            "Please open a lesson or mention the topic more clearly."
        )

    if intent == "summary":
        return generate_summary(lesson)

    if intent == "quiz":
        return generate_quiz(lesson)

    if intent == "explanation":
        return generate_explanation(lesson)

    return generate_general(user_message)