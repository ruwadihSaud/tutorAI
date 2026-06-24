# test_tutor.py

import unittest
from unittest.mock import patch

import backend.services.LLM as llm_service
from backend.data.lesson_loader import get_lesson_by_id
from backend.generators.progress_generator import generate_progress
from backend.generators.quiz_generator import generate_quiz
from backend.tutor import (
    UNCLEAR_REQUEST_MESSAGE,
    detect_explanation_scope,
    detect_intent,
    determine_student_intent,
    generate_level_test_reply,
    generate_tutor_reply,
)


class TutorRoutingTests(unittest.TestCase):
    def test_progress_reply_shows_subject_level_and_remaining_lessons(self):
        reply = generate_progress(
            "show my progress",
            lesson_id="lesson_01_what_is_machine_learning",
            progress_context={
                "selected_subject": "Machine Learning",
                "student_level": "Beginner",
                "current_lesson_id": "lesson_01_what_is_machine_learning",
                "completed_lessons": ["lesson_01_what_is_machine_learning"],
            },
        )

        self.assertIn("Subject: Machine Learning", reply["reply"])
        self.assertIn("Current level: Beginner", reply["reply"])
        self.assertIn("Lessons remaining in this level", reply["reply"])
        self.assertEqual(reply["progress"]["subject"], "Machine Learning")
        self.assertEqual(reply["progress"]["level"], "Beginner")

    def test_progress_route_returns_progress_report(self):
        response = generate_tutor_reply(
            "show my progress",
            lesson_id="lesson_01_what_is_machine_learning",
            progress_context={
                "selected_subject": "Machine Learning",
                "student_level": "Beginner",
                "current_lesson_id": "lesson_01_what_is_machine_learning",
                "completed_lessons": ["lesson_01_what_is_machine_learning"],
            },
        )

        self.assertEqual(response["response_type"], "progress_report")
        self.assertEqual(response["progress"]["subject"], "Machine Learning")

    def test_lesson_quiz_uses_only_questions_linked_to_current_lesson(self):
        lesson = get_lesson_by_id("lesson_01_what_is_machine_learning")
        quiz = generate_quiz(lesson)

        self.assertTrue(quiz["questions"])
        self.assertTrue(
            all(
                question["id_lesson"] == lesson["id"]
                for question in quiz["questions"]
            )
        )

    def test_level_test_uses_only_current_level_questions(self):
        level_test = generate_level_test_reply(
            "Machine Learning",
            "Intermediate",
        )

        self.assertTrue(level_test["questions"])
        self.assertEqual(level_test["passing_score"], 70)
        self.assertTrue(
            all(
                question["source_level"] == "Intermediate"
                for question in level_test["questions"]
            )
        )

    @patch.dict(
        llm_service.LLM_SERVICES,
        {
            "gemini": lambda **kwargs: "Gemini connection error: unavailable",
            "ollama": lambda **kwargs: "Fallback reply",
        },
    )
    def test_llm_uses_ollama_fallback(self):
        self.assertEqual(
            llm_service.ask_llm("hello", "system"),
            "Fallback reply",
        )

    @patch.dict(
        llm_service.LLM_SERVICES,
        {
            "gemini": lambda **kwargs: "Gemini connection error: unavailable",
            "ollama": lambda **kwargs: "Ollama connection error: unavailable",
        },
    )
    def test_llm_returns_error_only_when_both_services_fail(self):
        reply = llm_service.ask_llm("hello", "system")

        self.assertTrue(llm_service.is_llm_error(reply))
        self.assertIn("Gemini and Ollama", reply)

    def test_detects_supported_tasks(self):
        cases = {
            "explain this lesson": "explanation",
            "summarize this lesson": "summary",
            "create a quiz": "quiz",
            "help me": "help",
            "show my progress": "progress",
            "hello TutorAI": "general_chat",
        }

        for message, expected_intent in cases.items():
            with self.subTest(message=message):
                self.assertEqual(detect_intent(message), expected_intent)

    def test_simpler_explanation_keeps_explanation_task(self):
        message = (
            "I need a simpler explanation. I still do not understand "
            "test accuracy."
        )
        self.assertEqual(detect_intent(message), "explanation")

    @patch(
        "backend.tutor.generate_intent_classification",
        return_value="INTENT=summary",
    )
    def test_llm_understands_spelling_error(self, classify_intent):
        intent, error = determine_student_intent("summry the leson")

        self.assertEqual(intent, "summary")
        self.assertIsNone(error)
        classify_intent.assert_called_once()

    @patch(
        "backend.tutor.generate_intent_classification",
        return_value="INTENT=general_chat",
    )
    def test_llm_keeps_clear_general_chat(self, _classify_intent):
        intent, error = determine_student_intent("hello TutorAI")

        self.assertEqual(intent, "general_chat")
        self.assertIsNone(error)

    @patch(
        "backend.tutor.generate_intent_classification",
        return_value="INTENT=unclear",
    )
    def test_unclear_message_returns_friendly_reply(self, _classify_intent):
        response = generate_tutor_reply("asdf qwer zxcv")

        self.assertEqual(response["reply"], UNCLEAR_REQUEST_MESSAGE)
        self.assertEqual(response["response_type"], "message")

    @patch(
        "backend.tutor.generate_intent_classification",
        return_value="Gemini connection error: unavailable",
    )
    def test_intent_llm_error_is_returned(self, _classify_intent):
        intent, error = determine_student_intent("summryy")

        self.assertEqual(intent, "llm_error")
        self.assertEqual(error, "Gemini connection error: unavailable")

    def test_detects_explanation_scope(self):
        self.assertEqual(
            detect_explanation_scope("explain this lesson"),
            "current_lesson",
        )
        self.assertEqual(
            detect_explanation_scope("explain regularization"),
            "specific_topic",
        )

    def test_missing_lesson_returns_friendly_message(self):
        response = generate_tutor_reply("summarize this lesson")

        self.assertEqual(response["response_type"], "message")
        self.assertIn("could not find", response["reply"].lower())

    @patch("backend.tutor.generate_explanation", return_value="Simple explanation")
    @patch("backend.tutor.get_lesson_by_id")
    def test_routes_current_lesson_explanation(
        self,
        get_lesson_by_id,
        generate_explanation,
    ):
        get_lesson_by_id.return_value = {
            "id": "lesson_01",
            "title": "Current lesson",
            "content": "lesson content",
        }

        response = generate_tutor_reply(
            "explain this lesson",
            lesson_id="lesson_01",
        )

        self.assertEqual(response["reply"], "Simple explanation")
        self.assertEqual(response["response_type"], "explanation_check")
        generate_explanation.assert_called_once()

    @patch("backend.tutor.generate_explanation", return_value="Video explanation")
    @patch(
        "backend.tutor.get_relevant_video",
        return_value={
            "video_title": "Lesson video",
            "video_url": "https://example.com/video",
        },
    )
    @patch("backend.tutor.get_lesson_by_id")
    def test_video_request_passes_verified_video_to_explanation(
        self,
        get_lesson_by_id,
        get_relevant_video,
        generate_explanation,
    ):
        lesson = {
            "id": "lesson_01",
            "title": "Current lesson",
            "content": "lesson content",
        }
        get_lesson_by_id.return_value = lesson

        generate_tutor_reply(
            "explain this lesson with a video",
            lesson_id="lesson_01",
        )

        get_relevant_video.assert_called_once_with(
            "explain this lesson with a video",
            lesson,
        )
        self.assertEqual(
            generate_explanation.call_args.kwargs["video"]["video_url"],
            "https://example.com/video",
        )


if __name__ == "__main__":
    unittest.main()
