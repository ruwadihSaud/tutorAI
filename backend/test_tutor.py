# test_tutor_rag.py

import unittest
from unittest.mock import patch

from backend.tutor import detect_explanation_scope, detect_intent, generate_tutor_reply


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

    def test_detects_explanation_scope(self):
        self.assertEqual(
            detect_explanation_scope("explain this lesson"),
            "current_lesson",
        )
        self.assertEqual(
            detect_explanation_scope("explain regularization"),
            "specific_topic",
        )

    @patch("backend.tutor._search_relevant_lesson", return_value=None)
    def test_missing_lesson_returns_friendly_message(self, _search_lesson):
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
