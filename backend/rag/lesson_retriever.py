from sentence_transformers import SentenceTransformer, util
from backend.data.lesson_loader import load_lessons, get_lesson_by_id

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

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

# من وورد معينه نحدد اذا يبي الدرس الحالي او درس ثاني 
def is_current_lesson_request(user_message: str) -> bool:
    message = user_message.lower()

    for keyword in CURRENT_LESSON_KEYWORDS:
        if keyword in message:
            return True

    return False



# يبني دايركتري على الدرس الي طلبه الطالب
def build_lesson_text(lesson: dict) -> str:
    """
    Combine lesson fields into one searchable text.
    """

    return (
        f"Title: {lesson.get('title', '')}\n"
        f"Subject: {lesson.get('subject', '')}\n"
        f"Level: {lesson.get('level', '')}\n"
        f"Chapter: {lesson.get('chapter', '')}\n"
        f"Section: {lesson.get('section', '')}\n"
        f"Content: {lesson.get('content', '')}"
    )


# بحث عن الدرس
def search_relevant_lesson(user_message: str, min_score: float = 0.25) -> dict | None:
    """
    Search all lessons using a pretrained embedding model.
    Returns the most relevant lesson if the similarity score is high enough.
    """

    lessons = load_lessons()

    # نتاكد ان الملف فيه دروس
    if not lessons:
        return None

    lesson_texts = [build_lesson_text(lesson) for lesson in lessons]

    #تحويل الرساله الي انبدنق
    query_embedding = model.encode(user_message, convert_to_tensor=True)

    # تحويل محتوى الدروس الى انبدنق
    lesson_embeddings = model.encode(lesson_texts, convert_to_tensor=True)

    # نحسب التشابه بين الرساله ومحتوى الدروس
    scores = util.cos_sim(query_embedding, lesson_embeddings)[0]

    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    if best_score < min_score:
        return None

    best_lesson = lessons[best_index]
    best_lesson["retrieval_score"] = round(best_score, 4)

    return best_lesson

# المين فنكشن للبحث عن الدرس المناسب حسب طلب الطالب
def retrieve_lesson(user_message: str,current_lesson_id: str | None = None,min_score: float = 0.25) -> dict | None:

    #   اول شي يشيك هو يبي الدرس الحالي او لا
    if is_current_lesson_request(user_message) and current_lesson_id:
        lesson = get_lesson_by_id(current_lesson_id)

        # في حال طلب الدرس الحالي يكون السكور 1
        if lesson:
            lesson["retrieval_score"] = 1.0
            lesson["retrieval_method"] = "current_lesson"

        return lesson

    # اذا كان لا طالب موضوع ثاني يسوي سيرش 
    lesson = search_relevant_lesson(
        user_message=user_message,
        min_score=min_score
    )

    if lesson:
        lesson["retrieval_method"] = "semantic_search"

    return lesson