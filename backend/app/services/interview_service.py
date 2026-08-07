from app.services.candidate_service import get_candidate
from app.services.session_service import get_session


def start_interview(candidate_id: str):
    candidate = get_candidate(candidate_id)
    session = get_session(candidate_id)

    completed = [
        mission
        for mission in candidate["missions"]
        if mission.get("passed")
    ]

    if not completed:
        question = "Tell me about yourself and your AI learning journey."

        session["questions"].append(question)
        session["current_question"] = 1

        return {
            "question": question,
            "questionNumber": 1
        }

    latest = completed[-1]

    question = (
        f"You completed '{latest['title']}'. "
        "Can you explain this concept in your own words?"
    )

    session["questions"].append(question)
    session["current_question"] = 1

    return {
        "question": question,
        "questionNumber": 1
    }