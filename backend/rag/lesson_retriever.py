from backend.data.lesson_loader import load_lessons, get_lesson_by_id


# في حال كان الطالب يبي يسال عن الموضوع الحالي 
CURRENT_LESSON_KEYWORDS = [
    "this lesson",
    "current lesson",
    "this topic",
    "current topic",
    "هذا الدرس",
    "الدرس الحالي",
    "هذا الموضوع",
    "الموضوع الحالي",
]

def is_current_lesson_request(user_message: str) -> bool:
    message = user_message.lower()

    for keyword in CURRENT_LESSON_KEYWORDS:
        if keyword in message:
            return True

    return False