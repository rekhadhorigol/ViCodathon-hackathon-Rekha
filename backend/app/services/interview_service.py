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

    # Store the candidate's latest answer.
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
            "questionNumber": 1,
        }

    # Prefer topics that have not already been used.
    asked_questions = session["questions"]

    available_missions = [
        mission
        for mission in completed
        if mission["title"] not in " ".join(asked_questions)
    ]

    if not available_missions:
        available_missions = completed

    # Move through completed curriculum topics.
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

    latest_answer = answer or "No answer provided yet."

    prompt = f"""
You are an adaptive technical interviewer for an AI engineering cohort.

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

Previous interview:
{previous_context or "No previous interview context."}

Candidate's latest answer:
{latest_answer}

Your task is to generate EXACTLY ONE next technical interview question.

Adaptive behavior:
1. If the latest answer shows uncertainty, misunderstanding,
   or an incomplete explanation, ask a focused follow-up question
   that probes the weak point.
2. If the latest answer is strong, increase the difficulty or
   move toward a practical engineering scenario.
3. If the topic has been sufficiently assessed, move to another
   completed curriculum topic.
4. Use information from the candidate's previous answer when
   creating follow-up questions.
5. Never repeat a previous question.

Interview requirements:
- Assess real technical understanding.
- Prefer practical engineering scenarios over simple definitions.
- Match the candidate's experience level.
- Stay grounded in the candidate's completed curriculum.
- Do not ask about topics the candidate has not completed.
- Do not provide an answer or explanation.
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