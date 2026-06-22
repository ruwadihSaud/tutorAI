LEVELS = ["Beginner", "Intermediate", "Advanced"]


def determine_level(score: int) -> str:
    if score >= 80:
        return "Advanced"

    if score >= 50:
        return "Intermediate"

    return "Beginner"


def get_next_level(level: str | None) -> str | None:
    if level not in LEVELS:
        return None

    next_index = LEVELS.index(level) + 1
    if next_index >= len(LEVELS):
        return None

    return LEVELS[next_index]
