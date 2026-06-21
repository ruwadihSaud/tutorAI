# backend/tutor.py

from backend.data.lesson_loader import get_lesson_by_id

from backend.generators.summary_generator import generate_summary
from backend.generators.quiz_generator import generate_placement_test, generate_quiz
from backend.generators.explanation_generator import (
    generate_explanation,
    is_explanation_request,
)
from backend.generators.help_generator import generate_help
from backend.generators.general_generator import generate_general
from backend.services.ollama_service import ask_ollama, is_ollama_error


# يحدد نوع الطلب من رساله الطالب 
def detect_intent(user_message: str) -> str:
    message = user_message.lower().strip()

    if is_explanation_request(user_message):
        return "explanation"

    if any(
        keyword in message
        for keyword in ["لخص", "تلخيص", "اختصر", "أهم النقاط", "الزبدة"]
    ):
        return "summary"

    if any(
        keyword in message
        for keyword in ["اختبار", "اختبرني", "أسئلة", "تدريب"]
    ):
        return "quiz"

    if any(
        keyword in message
        for keyword in ["مساعدة", "ساعدني", "كيف أستخدم"]
    ):
        return "help"

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


def _message_response(reply: str) -> dict:
    return {
        "reply": reply,
        "response_type": "message",
    }


def _resolve_lesson(user_message: str, lesson_id: str | None) -> dict | None:
    if lesson_id:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            return lesson

    from backend.rag.lesson_retriever import retrieve_lesson

    return retrieve_lesson(
        user_message=user_message,
        current_lesson_id=lesson_id,
    )


def generate_tutor_reply(
    user_message: str,
    lesson_id: str | None = None,
) -> dict:
    """
    Main TutorAI router.

    1. Detect the student intent.
    2. Use RAG to retrieve the relevant lesson.
    3. Send the lesson to the correct generator.
    """

    intent = detect_intent(user_message)

    if intent == "general":
        return _message_response(ask_ollama(user_message))

    if intent == "help":
        return _message_response(generate_help(user_message))

    lesson = _resolve_lesson(user_message, lesson_id)

    if lesson is None:
        return _message_response(
            "I could not find a suitable lesson for your request. "
            "Please open a lesson or mention the topic more clearly."
        )

    if intent == "summary":
        return _message_response(generate_summary(lesson))

    if intent == "quiz":
        return _message_response(generate_quiz(lesson))

    if intent == "explanation":
        reply = generate_explanation(user_message, lesson)
        return {
            "reply": reply,
            "response_type": (
                "message" if is_ollama_error(reply) else "explanation_check"
            ),
        }

    return _message_response(generate_general(user_message))


def generate_placement_test_reply(subject: str) -> dict:
    return generate_placement_test(subject)
