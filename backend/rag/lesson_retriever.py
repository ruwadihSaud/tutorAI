# backend/rag/lesson_retriever.py

import json
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer, util

from backend.data.lesson_loader import get_lesson_by_id


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# مكان ملفات الانبدنق المحفوظه
BASE_DIR = Path(__file__).resolve().parents[1]
LESSON_INDEX_DIR = BASE_DIR / "data" / "lesson_index"

EMBEDDINGS_PATH = LESSON_INDEX_DIR / "lesson_embeddings.pt"
METADATA_PATH = LESSON_INDEX_DIR / "lesson_metadata.json"


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
    message = user_message.lower().strip()

    for keyword in CURRENT_LESSON_KEYWORDS:
        if keyword in message:
            return True

    return False


# تحميل الانبدنق الجاهز بدل مانسويه كل مره
def load_lesson_index() -> tuple[list[dict], torch.Tensor]:
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            f"Lesson embeddings file not found: {EMBEDDINGS_PATH}\n"
            "Run: python -m backend.data.lesson_index.build_lesson_index"
        )

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Lesson metadata file not found: {METADATA_PATH}\n"
            "Run: python -m backend.data.lesson_index.build_lesson_index"
        )

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        lessons = json.load(file)

    lesson_embeddings = torch.load(EMBEDDINGS_PATH)

    return lessons, lesson_embeddings


# بحث عن الدرس
def search_relevant_lesson(
    user_message: str,
    min_score: float = 0.25
) -> dict | None:
    lessons, lesson_embeddings = load_lesson_index()

    # نتاكد ان الملف فيه دروس
    if not lessons:
        return None

    # تحويل الرساله الي انبدنق
    query_embedding = model.encode(
        user_message,
        convert_to_tensor=True
    )

    # نحسب التشابه بين الرساله ومحتوى الدروس المحفوظ مسبقا
    scores = util.cos_sim(query_embedding, lesson_embeddings)[0]

    best_index = int(scores.argmax())
    best_score = float(scores[best_index])

    if best_score < min_score:
        return None

    best_lesson = lessons[best_index].copy()
    best_lesson["retrieval_score"] = round(best_score, 4)
    best_lesson["retrieval_method"] = "semantic_search"

    return best_lesson


# المين فنكشن للبحث عن الدرس المناسب حسب طلب الطالب
def retrieve_lesson(user_message: str,current_lesson_id: str | None = None,min_score: float = 0.25) -> dict | None:

    # اول شي يشيك هو يبي الدرس الحالي او لا
    if is_current_lesson_request(user_message):

        # اذا كان فيه درس حالي يرجعه
        if current_lesson_id:
            lesson = get_lesson_by_id(current_lesson_id)

            # في حال طلب الدرس الحالي يكون السكور 1
            if lesson:
                lesson = lesson.copy()
                lesson["retrieval_score"] = 1.0
                lesson["retrieval_method"] = "current_lesson"

            return lesson

        # اذا طلب الدرس الحالي وهو مو داخل صفحه فيها درس
        return None

    # اذا كان لا طالب موضوع ثاني يسوي سيرش
    return search_relevant_lesson(user_message=user_message,min_score=min_score)