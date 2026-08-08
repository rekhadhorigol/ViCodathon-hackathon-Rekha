from app.services.candidate_service import get_candidate
from app.services.curriculum_service import load_curriculum
from app.services.session_service import get_session
from app.services.gemini_service import generate_question


MAX_QUESTIONS = 8


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

    # Do not generate more questions after the interview limit.
    if session["current_question"] >= MAX_QUESTIONS:
        session["completed"] = True

        return {
            "completed": True,
            "questionNumber": session["current_question"],
            "message": "Interview complete.",
            "evaluationsReady": len(session["evaluations"]) > 0,
        }

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

    # Find topics whose curriculum days have not yet been assessed.
    assessed_days = session.get("assessed_days", [])

    available_missions = [
        mission
        for mission in completed
        if mission["day"] not in assessed_days
    ]

    # If all completed days have been used, allow follow-ups.
    if not available_missions:
        available_missions = completed

    # Rotate through different completed curriculum topics.
    mission_index = session["current_question"] % len(available_missions)
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

    current_day = topic_details["day"]

    # Track this curriculum day as assessed.
    if current_day not in session["assessed_days"]:
        session["assessed_days"].append(current_day)

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

Generate EXACTLY ONE technical interview question.

Adaptive behavior:
1. If the latest answer is weak, incomplete, or incorrect,
   ask a focused follow-up that probes the weakness.
2. If the latest answer is strong, increase the difficulty
   or use a realistic engineering scenario.
3. Avoid repeating questions.
4. Prefer practical engineering questions over definitions.
5. Match the candidate's experience level.
6. Stay grounded in the candidate's completed curriculum.
7. Use previous answers to maintain conversational context.
8. Do not provide an answer.
9. Return ONLY the question text.
"""

    question = generate_question(prompt)

    question_number = session["current_question"] + 1

    session["questions"].append(question)

    session["question_topics"].append({
        "day": topic_details["day"],
        "title": topic_details["title"],
    })

    session["current_question"] = question_number

    return {
        "question": question,
        "questionNumber": question_number,
        "assessedDays": session["assessed_days"],
    }