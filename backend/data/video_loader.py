import json
import re
from pathlib import Path


VIDEO_DATA_PATH = Path(__file__).parent / "video.json"

VIDEO_REQUEST_TERMS = (
    "video",
    "youtube",
    "watch",
    "فيديو",
    "يوتيوب",
    "مقطع شرح",
    "مقطع",
)


def load_videos() -> list[dict]:
    with open(VIDEO_DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def wants_video(user_message: str) -> bool:
    message = (user_message or "").lower()
    return any(term in message for term in VIDEO_REQUEST_TERMS)


def _normalize(text: str) -> str:
    normalized = re.sub(r"[^\w\s]", " ", (text or "").lower())
    return " ".join(normalized.split())


def _match_score(video: dict, user_message: str, lesson: dict | None) -> int:
    message = _normalize(user_message)
    lesson_id = str((lesson or {}).get("id", ""))
    lesson_title = _normalize((lesson or {}).get("title", ""))
    video_lesson_id = str(video.get("lesson_id", ""))
    video_title = _normalize(video.get("title", ""))
    keywords = [_normalize(keyword) for keyword in video.get("keywords", [])]
    score = 0

    if lesson_id and lesson_id == video_lesson_id:
        score += 100

    if video_title and message and video_title in message:
        score += 90

    for keyword in keywords:
        if keyword and keyword in message:
            score += 70

    if video_title and lesson_title:
        if video_title in lesson_title or lesson_title in video_title:
            score += 50

        title_overlap = set(video_title.split()) & set(lesson_title.split())
        score += len(title_overlap) * 10

    for keyword in keywords:
        if keyword and lesson_title and keyword in lesson_title:
            score += 25

    return score


def get_relevant_video(
    user_message: str,
    lesson: dict | None = None,
) -> dict | None:
    videos = load_videos()
    if not videos:
        return None

    ranked_videos = sorted(
        videos,
        key=lambda video: _match_score(video, user_message, lesson),
        reverse=True,
    )
    best_video = ranked_videos[0]

    if _match_score(best_video, user_message, lesson) <= 0:
        return None

    return best_video
