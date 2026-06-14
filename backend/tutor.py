# backend/tutor.py

from backend.data.lesson_loader import get_lesson_by_id

from backend.generators.summary_generator import generate_summary
from backend.generators.quiz_generator import generate_quiz
from backend.generators.explanation_generator import generate_explanation
from backend.generators.help_generator import generate_help
from backend.generators.general_generator import generate_general


# يحدد نوع الطلب من رساله الطالب 
def detect_intent(user_message: str) -> str:
    message = user_message.lower()

    if any(word in message for word in ["summarize", "summary", "تلخيص", "لخص", "لخصي"]):
        return "summary"

    if any(word in message for word in ["quiz", "test", "exam", "اختبار", "اسئلة", "أسئلة"]):
        return "quiz"

    if any(word in message for word in ["explain", "explanation", "teach", "شرح", "اشرح", "فسر"]):
        return "explanation"

    if any(word in message for word in ["help", "support", "مساعدة", "ساعدني", "كيف"]):
        return "help"

    return "general"


def generate_tutor_reply(user_message: str, lesson_id: str | None = None) -> str:
    #تحديد الطلب 
    intent = detect_intent(user_message)

    lesson = None

    # حسب الطلب يستدعي اي  من البرومبتات
    if lesson_id:
        lesson = get_lesson_by_id(lesson_id)

    if intent == "summary":
        return generate_summary(lesson)

    if intent == "quiz":
        return generate_quiz(lesson)

    if intent == "explanation":
        return generate_explanation(lesson)

    if intent == "help":
        return generate_help(user_message)

    return generate_general(user_message)