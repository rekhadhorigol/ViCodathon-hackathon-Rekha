from app.services.candidate_service import get_candidate
from app.services.session_service import get_session


def start_interview(session_id: str, candidate_id: str, answer: str | None = None,):
    candidate = get_candidate(candidate_id)
    session = get_session(session_id)
    if answer:
        session["answers"].append(answer)

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

    question_number = session["current_question"] + 1

    if question_number == 1:
        question = (
            f"You completed '{latest['title']}'. "
            "Can you explain this concept in your own words?"
        )
    else:
        question = (
            f"Question {question_number}: "
            f"What were the biggest challenges while working on "
            f"'{latest['title']}'?"
        )

    session["questions"].append(question)
    session["current_question"] = question_number

    return {
        "question": question,
        "questionNumber": question_number
    }