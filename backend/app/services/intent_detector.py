INTENT_KEYWORDS = {
    "summary": [
        "summary", "summarize", "summarise",
        "لخص", "تلخيص", "اختصر", "الزبدة", "اهم النقاط", "أهم النقاط",
    ],
    "quiz": [
        "quiz", "test", "exam", "questions", "practice",
        "اختبار", "اختبرني", "اسئلة", "أسئلة", "تدريب",
        "سوي اختبار", "اعمل اختبار",
    ],
    "help": [
        "help", "support", "how to use", "what can i do",
        "مساعدة", "ساعدني", "كيف استخدم", "كيف أستخدم", "وش اقدر اسوي",
    ],
    "progress": [
        "progress", "my progress", "how am i doing", "level",
        "تقدمي", "تقدمي الدراسي", "مستواي", "كيف مستواي",
    ],
    "learning_plan": [
        "learning plan", "study plan", "learning path", "plan", "path",
        "خطة تعلم", "خطة دراسة", "مسار تعلم", "خطة", "مسار",
    ],
    "explanation": [
        "explain", "explanation", "clarify", "teach", "what is",
        "what does", "how", "why", "اشرح", "شرح", "وضح", "فسر",
        "فهمني", "وش يعني", "ما معنى", "كيف", "ليش", "ما فهمت",
    ],
}


EXPLANATION_FOLLOW_UPS = (
    "simpler explanation",
    "still do not understand",
    "still don't understand",
    "need more explanation",
    "شرح ابسط",
    "شرح أبسط",
    "ما زلت لا افهم",
    "ما زلت لا أفهم",
)


EXPLANATION_COMMANDS = (
    "explain",
    "clarify",
    "teach me",
    "اشرح",
    "وضح",
    "فسر",
    "فهمني",
)


def detect_intent(message: str) -> str:
    text = (message or "").lower().strip()

    if not text:
        return "general_chat"

    if any(phrase in text for phrase in EXPLANATION_FOLLOW_UPS):
        return "explanation"

    if any(
        text == command or text.startswith(f"{command} ")
        for command in EXPLANATION_COMMANDS
    ):
        return "explanation"

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "general_chat"
