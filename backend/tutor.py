# backend/tutor.py

import re

from backend.data.lesson_loader import get_lesson_by_id
from backend.generators.explanation_generator import generate_explanation
from backend.generators.general_generator import generate_general
from backend.generators.help_generator import generate_help
from backend.generators.intent_generator import generate_intent_classification
from backend.generators.learning_plan_generator import generate_learning_plan
from backend.generators.progress_generator import generate_progress
from backend.generators.quiz_generator import generate_placement_test, generate_quiz
from backend.generators.summary_generator import generate_summary
from backend.services.LLM import is_llm_error

# يحدد نوع الطلب من رساله الطالب
from backend.services.intent_detector import (
    EXPLANATION_COMMANDS,
    EXPLANATION_FOLLOW_UPS,
    detect_intent,
)


SUPPORTED_INTENTS = (
    "explanation",
    "summary",
    "quiz",
    "help",
    "progress",
    "learning_plan",
    "general_chat",
)
LLM_CLASSIFICATION_OPTIONS = (*SUPPORTED_INTENTS, "unclear")

UNCLEAR_REQUEST_MESSAGE = (
    "I could not understand your request clearly. Please rephrase it or ask for "
    "an explanation, summary, quiz, help, progress, or learning plan."
)
MISSING_LESSON_MESSAGE = (
    "I could not find a suitable lesson for your request. "
    "Please open a lesson or mention the topic more clearly."
)


def _parse_llm_intent(classification: str) -> str:
    text = classification.lower().strip()
    options_pattern = "|".join(re.escape(intent) for intent in LLM_CLASSIFICATION_OPTIONS)
    match = re.search(rf"intent\s*=\s*({options_pattern})\b", text)

    if match:
        return match.group(1)

    cleaned_text = text.strip("`'\" .")
    if cleaned_text in LLM_CLASSIFICATION_OPTIONS:
        return cleaned_text

    return "unclear"


def determine_student_intent(user_message: str) -> tuple[str, str | None]:
    if not user_message or not user_message.strip():
        return "unclear", None

    rule_intent = detect_intent(user_message)
    if rule_intent != "general_chat":
        return rule_intent, None

    classification = generate_intent_classification(
        user_message,
        LLM_CLASSIFICATION_OPTIONS,
    )
    if is_llm_error(classification):
        return "llm_error", classification

    return _parse_llm_intent(classification), None


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


def _get_current_lesson(lesson_id: str | None) -> dict | None:
    if not lesson_id:
        return None

    return get_lesson_by_id(lesson_id)


def generate_tutor_reply(
    user_message: str,
    lesson_id: str | None = None,
) -> dict:
    """
    Main TutorAI router.

    1. Detect intent with simple rules.
    2. Use the LLM when rules cannot identify the request.
    3. Return an unclear message when classification still fails.
    4. Run the generator that owns the selected task.
    """
    intent, intent_error = determine_student_intent(user_message)

    if intent_error:
        return _message_response(intent_error)

    if intent == "unclear":
        return _message_response(UNCLEAR_REQUEST_MESSAGE)

    direct_generators = {
        "general_chat": generate_general,
        "help": generate_help,
        "progress": generate_progress,
        "learning_plan": generate_learning_plan,
    }
    if intent in direct_generators:
        return _message_response(direct_generators[intent](user_message))

    explanation_scope = (
        detect_explanation_scope(user_message)
        if intent == "explanation"
        else None
    )
    lesson = _get_current_lesson(lesson_id)

    if lesson is None:
        return _message_response(MISSING_LESSON_MESSAGE)

    if intent == "summary":
        return _message_response(generate_summary(lesson))

    if intent == "quiz":
        return _message_response(generate_quiz(lesson))

    reply = generate_explanation(
        user_message,
        lesson,
        explanation_scope=explanation_scope or "specific_topic",
    )
    return {
        "reply": reply,
        "explanation_scope": explanation_scope,
        "response_type": "message" if is_llm_error(reply) else "explanation_check",
    }


def generate_placement_test_reply(subject: str) -> dict:
    return generate_placement_test(subject)
