# backend/tutor.py

from backend.data.lesson_loader import get_lesson_by_id

from backend.generators.explanation_generator import generate_explanation
from backend.generators.general_generator import generate_general
from backend.generators.help_generator import generate_help
from backend.generators.learning_plan_generator import generate_learning_plan
from backend.generators.progress_generator import generate_progress
from backend.generators.quiz_generator import generate_placement_test, generate_quiz
from backend.generators.summary_generator import generate_summary
from backend.services.LLM import is_llm_error


INTENT_KEYWORDS = {
    "summary": [
        "summarize", "summary", "summarise",
        "لخص", "لخصي", "تلخيص", "اختصر", "اختصري",
        "اهم النقاط", "أهم النقاط", "الزبدة",
    ],
    "quiz": [
        "quiz", "test", "exam", "questions",
        "اختبار", "اختبرني", "اسئلة", "أسئلة",
        "سوي اختبار", "اعمل اختبار", "تدريب",
    ],
    "explanation": [
        "explain", "explanation", "teach me", "teach", "clarify",
        "what does", "what is", "what is meant", "why", "how does",
        "understand", "اشرح", "شرح", "وضح", "فسر", "فهمني",
        "ما معنى", "وش يعني", "ليش", "كيف", "ما فهمت",
    ],
    "help": [
        "help", "support", "مساعدة", "ساعدني",
        "وش اقدر اسوي", "كيف استخدم", "كيف أستخدم",
    ],
    "progress": [
        "progress", "my progress", "how am i doing",
        "تقدمي", "تقدمي الدراسي", "مستواي", "كيف مستواي",
    ],
    "learning_plan": [
        "learning plan", "study plan", "learning path",
        "خطة تعلم", "خطة دراسة", "مسار تعلم",
    ],
}


CURRENT_LESSON_EXPLANATION_PHRASES = [
    "this lesson",
    "current lesson",
    "this topic",
    "current topic",
    "this content",
    "this point",
    "explain it",
    "explain more",
    "هذا الدرس",
    "الدرس الحالي",
    "هذا الموضوع",
    "الموضوع الحالي",
    "هذا المحتوى",
    "هذه النقطة",
    "اشرحه",
    "اشرح اكثر",
    "اشرح أكثر",
]


GENERAL_EXPLANATION_REQUESTS = {
    "explain",
    "explain please",
    "explain the lesson",
    "i do not understand",
    "i don't understand",
    "اشرح",
    "اشرح لي",
    "اشرح الدرس",
    "وضح",
    "وضح لي",
    "فهمني",
    "ما فهمت",
}


EXPLANATION_FOLLOW_UP_PHRASES = [
    "i need a simpler explanation",
    "simpler explanation",
    "explain it more simply",
    "explain more simply",
    "still do not understand",
    "still don't understand",
    "need more explanation",
    "احتاج شرح ابسط",
    "أحتاج شرح أبسط",
    "اشرح بشكل ابسط",
    "اشرح بشكل أبسط",
    "ما زلت لا افهم",
    "ما زلت لا أفهم",
]


EXPLANATION_COMMAND_PREFIXES = (
    "explain ",
    "clarify ",
    "teach me ",
    "اشرح ",
    "وضح ",
    "فسر ",
    "فهمني ",
)


# يحدد نوع الطلب من رساله الطالب 
def detect_intent(user_message: str) -> str:
    message = user_message.lower().strip()

    if any(phrase in message for phrase in EXPLANATION_FOLLOW_UP_PHRASES):
        return "explanation"

    if message.startswith(EXPLANATION_COMMAND_PREFIXES):
        return "explanation"

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in message for keyword in keywords):
            return intent

    return "general"


def detect_explanation_scope(user_message: str) -> str:
    message = user_message.lower().strip()

    if message in GENERAL_EXPLANATION_REQUESTS:
        return "current_lesson"

    if any(phrase in message for phrase in CURRENT_LESSON_EXPLANATION_PHRASES):
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

    from backend.rag.lesson_retriever import retrieve_lesson

    return retrieve_lesson(
        user_message=user_message,
        current_lesson_id=lesson_id,
    )


def _resolve_explanation_lesson(
    user_message: str,
    lesson_id: str | None,
    explanation_scope: str,
) -> dict | None:
    current_lesson = get_lesson_by_id(lesson_id) if lesson_id else None

    if explanation_scope == "current_lesson":
        return current_lesson

    from backend.rag.lesson_retriever import retrieve_lesson

    relevant_lesson = retrieve_lesson(
        user_message=user_message,
        current_lesson_id=lesson_id,
    )
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

    if intent == "general":
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
