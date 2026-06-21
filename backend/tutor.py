# backend/tutor.py

# يحدد نوع الطلب من رساله الطالب
from backend.app.services.intent_detector import (
    EXPLANATION_COMMANDS,
    EXPLANATION_FOLLOW_UPS,
    detect_intent,
)
from backend.data.lesson_loader import get_lesson_by_id

from backend.generators.explanation_generator import generate_explanation
from backend.generators.general_generator import generate_general
from backend.generators.help_generator import generate_help
from backend.generators.learning_plan_generator import generate_learning_plan
from backend.generators.progress_generator import generate_progress
from backend.generators.quiz_generator import generate_placement_test, generate_quiz
from backend.generators.summary_generator import generate_summary
from backend.services.LLM import is_llm_error


def detect_explanation_scope(user_message: str) -> str:
    message = user_message.lower().strip()
    current_lesson_phrases = (
        "this lesson", "current lesson", "this topic", "current topic",
        "this content", "this point", "explain it", "explain more",
        "هذا الدرس", "الدرس الحالي", "هذا الموضوع", "الموضوع الحالي",
        "هذا المحتوى", "هذه النقطة", "اشرحه", "اشرح اكثر", "اشرح أكثر",
    )
    general_requests = (
        "explain please", "explain the lesson",
        "i do not understand", "i don't understand",
        "اشرح لي", "اشرح الدرس", "وضح لي", "ما فهمت",
    )

    if message in EXPLANATION_COMMANDS:
        return "current_lesson"

    if message in EXPLANATION_FOLLOW_UPS:
        return "current_lesson"

    if message in general_requests:
        return "current_lesson"

    if any(phrase in message for phrase in current_lesson_phrases):
        return "current_lesson"

    return "specific_topic"


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

    return _search_relevant_lesson(user_message, lesson_id)


def _search_relevant_lesson(
    user_message: str,
    lesson_id: str | None,
) -> dict | None:
    try:
        from backend.rag.lesson_retriever import retrieve_lesson

        return retrieve_lesson(
            user_message=user_message,
            current_lesson_id=lesson_id,
        )
    except Exception:
        return None


def _resolve_explanation_lesson(
    user_message: str,
    lesson_id: str | None,
    explanation_scope: str,
) -> dict | None:
    current_lesson = get_lesson_by_id(lesson_id) if lesson_id else None

    if explanation_scope == "current_lesson":
        return current_lesson

    relevant_lesson = _search_relevant_lesson(user_message, lesson_id)
    return relevant_lesson or current_lesson


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

    if intent == "general_chat":
        return _message_response(generate_general(user_message))

    if intent == "help":
        return _message_response(generate_help(user_message))

    if intent == "progress":
        return _message_response(generate_progress(user_message))

    if intent == "learning_plan":
        return _message_response(generate_learning_plan(user_message))

    explanation_scope = None
    if intent == "explanation":
        explanation_scope = detect_explanation_scope(user_message)
        lesson = _resolve_explanation_lesson(
            user_message,
            lesson_id,
            explanation_scope,
        )
    else:
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
        reply = generate_explanation(
            user_message,
            lesson,
            explanation_scope=explanation_scope or "specific_topic",
        )
        return {
            "reply": reply,
            "explanation_scope": explanation_scope,
            "response_type": (
                "message" if is_llm_error(reply) else "explanation_check"
            ),
        }

    return _message_response(generate_general(user_message))


def generate_placement_test_reply(subject: str) -> dict:
    return generate_placement_test(subject)
