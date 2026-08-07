from app.services.candidate_service import get_candidate
from app.services.curriculum_service import load_curriculum
from app.services.session_service import get_session
from app.services.gemini_service import generate_question


def start_interview(
    session_id: str,
    candidate_id: str,
    answer: str | None = None,
) -> dict:
    """Start or continue an adaptive technical interview."""

    candidate = get_candidate(candidate_id)
    curriculum = load_curriculum()
    session = get_session(session_id)

    if answer:
        session["answers"].append(answer)

    completed = [
        mission
        for mission in candidate["missions"]
        if mission.get("passed")
    ]

    if not completed:
        question = (
            "Tell me about yourself and your AI learning journey."
        )

        session["questions"].append(question)
        session["current_question"] = 1

        return {
            "question": question,
            "questionNumber": 1,
        }

    # Prefer completed topics that have not already been asked.
    asked_questions = session["questions"]

    available_missions = [
        mission
        for mission in completed
        if mission["title"] not in " ".join(asked_questions)
    ]

    if not available_missions:
        available_missions = completed

    # Move through the candidate's completed curriculum topics.
    mission_index = min(
        session["current_question"],
        len(available_missions) - 1,
    )

    mission = available_missions[mission_index]

    curriculum_day = next(
        (
            day
            for day in curriculum["days"]
            if day["day"] == mission["day"]
        ),
        None,
    )

    topic_details = curriculum_day or {
        "day": mission["day"],
        "title": mission["title"],
        "objectives": [],
        "tools": [],
    }

    previous_context = "\n".join(
        f"Q{i + 1}: {q}\nA{i + 1}: {a}"
        for i, (q, a) in enumerate(
            zip(session["questions"], session["answers"])
        )
    )

    prompt = f"""
You are conducting a realistic technical interview for an AI engineering cohort.

Candidate:
Name: {candidate["member"]["name"]}
Role: {candidate["member"]["jobRole"]}
Experience: {candidate["member"]["yearsExperience"]} years

Current curriculum topic:
Day {topic_details["day"]}: {topic_details["title"]}

Learning objectives:
{topic_details.get("objectives", [])}

Tools:
{topic_details.get("tools", [])}

Previous interview context:
{previous_context or "No previous answer yet."}

Generate exactly ONE technical interview question.

Rules:
- Assess the candidate's actual understanding.
- Use the previous answer to create a meaningful follow-up when appropriate.
- Do not repeat previous questions.
- Keep the question specific to the curriculum topic.
- Match the candidate's experience level.
- Prefer practical engineering questions over definitions.
- Do not provide an answer.
- Return ONLY the question text.
"""

    question = generate_question(prompt)

    question_number = session["current_question"] + 1

    session["questions"].append(question)
    session["current_question"] = question_number

    return {
        "question": question,
        "questionNumber": question_number,
    }