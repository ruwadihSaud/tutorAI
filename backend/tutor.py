# backend/tutor.py

from backend.generators.explanation_generator import generate_explanation
from backend.generators.general_generator import generate_general
from backend.generators.help_generator import generate_help
from backend.generators.learning_plan_generator import generate_learning_plan
from backend.generators.progress_generator import generate_progress
from backend.generators.quiz_generator import generate_quiz
from backend.generators.summary_generator import generate_summary


def generate_tutor_reply(user_message: str) -> str:
    """
    Route the student's message to the correct response generator.
    """
    intent = detect_intent(user_message)

    if intent == "summary":
        return generate_summary(user_message)

    if intent == "quiz":
        return generate_quiz(user_message)

    if intent == "explanation":
        return generate_explanation(user_message)

    if intent == "progress":
        return generate_progress(user_message)

    if intent == "learning_plan":
        return generate_learning_plan(user_message)

    if intent == "help":
        return generate_help(user_message)

    return generate_general(user_message)


def detect_intent(user_message: str) -> str:
    """
    Detect the student's intent from the message.

    This is temporary rule-based logic. Later, it can be replaced with an LLM
    or classifier without changing the generator files.
    """
    message = user_message.lower()

    if any(word in message for word in ["quiz", "test", "exam", "question"]):
        return "quiz"

    if any(word in message for word in ["explain", "teach", "understand", "lesson"]):
        return "explanation"

    if any(word in message for word in ["summarize", "summary", "review"]):
        return "summary"

    if any(word in message for word in ["progress", "weak", "score", "performance"]):
        return "progress"

    if any(word in message for word in ["plan", "learning plan", "study plan", "schedule"]):
        return "learning_plan"

    if any(word in message for word in ["help", "how to use", "support"]):
        return "help"

    return "general"
