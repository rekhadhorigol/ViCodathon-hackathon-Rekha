from app.services.candidate_service import get_candidate
from app.services.curriculum_service import load_curriculum
from app.services.session_service import get_session
from app.services.gemini_service import generate_question, GeminiServiceError
from app.services.evaluation_service import evaluate_answer
from app.services.overall_evaluation_service import generate_overall_evaluation


MAX_QUESTIONS = 8


def _generate_next_question(session: dict, candidate: dict, curriculum: dict, latest_answer: str | None) -> dict:
    """Core adaptive question generation, shared by both the legacy and
    technical-spec-compliant interview flows."""

    completed = [
        mission
        for mission in candidate["missions"]
        if mission.get("passed")
    ]

    if not completed:
        question = "Tell me about yourself and your AI learning journey."

        session["questions"].append(question)
        session["question_topics"].append({"day": 0, "title": "Introduction"})
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

    resolved_answer = latest_answer or "No answer provided yet."

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
{resolved_answer}

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


def start_interview(
    session_id: str,
    candidate_id: str,
    answer: str | None = None,
) -> dict:
    """Legacy/internal interview flow used by this project's own frontend.

    Kept separate from `handle_interview_turn` (the technical-spec-compliant
    flow) so the deployed frontend keeps working unchanged.
    """

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

    return _generate_next_question(session, candidate, curriculum, answer)


def _build_spec_feedback(overall: dict) -> dict:
    """Map this project's overall-evaluation shape onto the exact
    `feedback` shape required by technical-spec.md (summary/strengths/gaps/next)."""

    strengths = overall.get("strongestAreas") or []
    gaps = overall.get("technicalGaps") or []
    next_steps = list(overall.get("areasToImprove") or [])
    recommendation = overall.get("recommendation")

    if recommendation:
        next_steps.append(recommendation)

    summary = overall.get("technicalStrength") or overall.get("summary") or (
        f"Overall verdict: {overall.get('verdict', 'N/A')} "
        f"(score {overall.get('overallScore', 'N/A')}/10)."
    )

    return {
        "summary": summary,
        "strengths": strengths,
        "gaps": gaps,
        "next": next_steps,
    }


def handle_interview_turn(
    session_id: str,
    candidate: dict | None = None,
    message: str | None = None,
) -> dict:
    """Technical-spec-compliant POST /api/interview handler.

    First call:  {"sessionId": ..., "candidate": {...candidate.json}}
    Later calls: {"sessionId": ..., "message": "..."}
    Returns:     {"reply": ..., "done": bool, "feedback"?: {...}}
    """

    session = get_session(session_id)
    curriculum = load_curriculum()

    if candidate and not session.get("spec_candidate"):
        session["spec_candidate"] = candidate

    stored_candidate = session.get("spec_candidate")

    if not stored_candidate:
        raise ValueError(
            "A 'candidate' object is required to start a new interview session."
        )

    # A message means the candidate is answering the most recently asked question.
    if message:
        session["answers"].append(message)

        last_index = len(session["questions"]) - 1
        if 0 <= last_index < len(session.get("question_topics", [])):
            topic_info = session["question_topics"][last_index]
            curriculum_day = next(
                (day for day in curriculum["days"] if day["day"] == topic_info["day"]),
                None,
            )
            objectives = curriculum_day.get("objectives", []) if curriculum_day else []

            try:
                evaluation = evaluate_answer(
                    question=session["questions"][last_index],
                    answer=message,
                    topic=topic_info["title"],
                    objectives=objectives,
                    candidate_role=stored_candidate["member"]["jobRole"],
                    years_experience=stored_candidate["member"]["yearsExperience"],
                )
                session["evaluations"].append({
                    "questionNumber": last_index + 1,
                    "question": session["questions"][last_index],
                    "answer": message,
                    "evaluation": evaluation,
                })
            except (GeminiServiceError, ValueError):
                # Don't let a single evaluation hiccup break the interview flow.
                pass

    # Interview complete: generate feedback and return it in the same response.
    if session["current_question"] >= MAX_QUESTIONS:
        session["completed"] = True

        overall = generate_overall_evaluation(
            evaluations=session["evaluations"],
            candidate_role=stored_candidate["member"]["jobRole"],
            years_experience=stored_candidate["member"]["yearsExperience"],
        )
        session["feedback"] = overall

        return {
            "reply": "Interview completed. Thank you for your time.",
            "done": True,
            "feedback": _build_spec_feedback(overall),
        }

    result = _generate_next_question(session, stored_candidate, curriculum, message)

    return {
        "reply": result["question"],
        "done": False,
    }
