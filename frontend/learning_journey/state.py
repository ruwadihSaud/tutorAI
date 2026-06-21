def determine_level(score: int) -> str:
    if score >= 80:
        return "Advanced"

    if score >= 50:
        return "Intermediate"

    return "Beginner"
