# frontend/data/lesson_loader.py

import json
from pathlib import Path


DATA_PATH = Path(__file__).parent / "lessons.json"


# يقرا ملف الدروس من lessons.json و يرجعهم كقائمه من القواميس
def load_lessons():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        lessons = json.load(file)

    lessons = sorted(lessons, key=lambda lesson: lesson["order"])
    return lessons


# يرجع الايدي للدرس
def get_lesson_by_id(lesson_id: str):
    lessons = load_lessons()

    for lesson in lessons:
        if str(lesson["id"]) == str(lesson_id):
            return lesson

    return None
