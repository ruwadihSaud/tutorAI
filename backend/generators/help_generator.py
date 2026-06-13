# backend/generators/help_generator.py


def generate_help(user_message: str) -> str:
    """
    Generate a simple help message for the student.
    This function only depends on the student's message.
    """

    return (
        "I can help you use TutorAI in the following ways:\n\n"
        "1. Ask me to summarize the current lesson.\n"
        "   Example: summarize this lesson\n\n"
        "2. Ask me to generate a quiz from the current lesson.\n"
        "   Example: create a quiz for this lesson\n\n"
        "3. Ask for help if you are not sure what to do next.\n"
        "   Example: help me\n\n"
        "For now, TutorAI focuses on summaries and quizzes based on the lesson currently displayed on the screen."
    )