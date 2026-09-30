from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""Create a structured learning path for the topic: {topic}
Learner level: {level}

Include:
1. A short goal.
2. Beginner/foundation topics.
3. Intermediate topics.
4. Advanced topics.
5. A suggested timeline in weeks.
6. Practice ideas or projects.
7. Useful resource types (videos, articles, books, documentation). Do not invent specific URLs.

Make it practical and sequential. If the learner is intermediate or advanced, still briefly identify prerequisites that may need review.
"""
    return generate_text(prompt)
