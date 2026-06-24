# شرح مفهوم
# backend/generators/explanation_generator.py


from backend.generators.general_generator import generate_general_system_prompt
from backend.services.LLM import ask_llm, is_llm_error


def generate_explanation(
    user_message: str,
    lesson: dict | None = None,
    explanation_scope: str = "specific_topic",
    video: dict | None = None,
) -> str:
    if not lesson:
        return "I could not find the current lesson. Please select a lesson first."

    title = lesson.get("title", "Current Lesson")
    content = lesson.get("content", "")

    if not content or len(content.split()) < 20:
        return "The selected lesson does not have enough content to explain."

    if explanation_scope == "current_lesson":
        explanation_instruction = (
            "The student did not identify a specific point. Explain the complete "
            "lesson currently displayed, focusing on its main idea and key concepts."
        )
    else:
        explanation_instruction = (
            "The student identified a topic or point. Explain that exact topic and "
            "use the retrieved lesson as the main source."
        )

    video_instruction = ""
    if video:
        video_instruction = (
            "\n\nVerified video resource:\n"
            f"Title: {video.get('video_title', 'Video explanation')}\n"
            f"URL: {video.get('video_url', '')}\n"
            "Recommend this exact video at the end using a Markdown link. "
            "Do not change the URL or invent another link."
        )

    prompt = (
        f"Current lesson title: {title}\n\n"
        f"Current lesson content:\n{content}\n\n"
        f"Student question:\n{user_message}\n\n"
        f"Explanation mode:\n{explanation_instruction}\n\n"
        "Use simple language, explain briefly in 2-4 short points, and include "
        "one practical example. Do not discuss unrelated topics. The interface will ask whether "
        "the student understood, so do not add a separate understanding question."
        f"{video_instruction}"
    )

    feature_requirements = (
        "The student is viewing a specific lesson. Explain the requested concept "
        "from the supplied lesson context accurately and step by step. Adapt the "
        "explanation to the student's question."
        "Keep the answer focused, short, and relevant. Prefer concise replies "
        "unless the student asks for more detail. "
    )

    reply = ask_llm(
        prompt,
        system_prompt=generate_general_system_prompt(feature_requirements),
    )

    if (
        video
        and not is_llm_error(reply)
        and video.get("video_url")
        and video["video_url"] not in reply
    ):
        video_title = video.get("video_title", "Video explanation")
        return f"{reply}\n\nRecommended video: [{video_title}]({video['video_url']})"

    return reply
