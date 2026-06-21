# test_tutor.py

import unittest
from unittest.mock import patch

from backend.tutor import (
    UNCLEAR_REQUEST_MESSAGE,
    detect_explanation_scope,
    detect_intent,
    determine_student_intent,
    generate_tutor_reply,
)


class TutorRoutingTests(unittest.TestCase):
    def test_detects_supported_tasks(self):
        cases = {
            "explain this lesson": "explanation",
            "summarize this lesson": "summary",
            "create a quiz": "quiz",
            "help me": "help",
            "show my progress": "progress",
            "create a learning plan": "learning_plan",
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


if __name__ == "__main__":
    unittest.main()
