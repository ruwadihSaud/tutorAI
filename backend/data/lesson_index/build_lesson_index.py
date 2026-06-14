# backend/rag/build_lesson_index.py
# يحول الكوس الى انبدنق بدال ما كل مره نحوله وياخذ معنا وقت 
import json
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer

from backend.data.lesson_loader import load_lessons


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

LESSON_INDEX_DIR = Path(__file__).resolve().parent

EMBEDDINGS_PATH = LESSON_INDEX_DIR / "lesson_embeddings.pt"
METADATA_PATH = LESSON_INDEX_DIR / "lesson_metadata.json"


def build_lesson_text(lesson: dict) -> str:
    return (
        f"Title: {lesson.get('title', '')}\n"
        f"Subject: {lesson.get('subject', '')}\n"
        f"Level: {lesson.get('level', '')}\n"
        f"Chapter: {lesson.get('chapter', '')}\n"
        f"Section: {lesson.get('section', '')}\n"
        f"Content: {lesson.get('content', '')}"
    )


def build_lesson_index() -> None:
    lessons = load_lessons()

    if not lessons:
        raise ValueError("No lessons found in lessons.json")

    lesson_texts = [build_lesson_text(lesson) for lesson in lessons]

    model = SentenceTransformer(MODEL_NAME)

    lesson_embeddings = model.encode(
        lesson_texts,
        convert_to_tensor=True,
        show_progress_bar=True
    )

    torch.save(lesson_embeddings, EMBEDDINGS_PATH)

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(lessons, file, ensure_ascii=False, indent=2)

    print("Lesson index built successfully.")
    print(f"Total lessons: {len(lessons)}")
    print(f"Embeddings saved to: {EMBEDDINGS_PATH}")
    print(f"Metadata saved to: {METADATA_PATH}")


if __name__ == "__main__":
    build_lesson_index()