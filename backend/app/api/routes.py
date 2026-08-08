from fastapi import APIRouter, HTTPException

from app.models.interview import InterviewRequest
from app.services.interview_service import start_interview
from app.services.evaluation_service import evaluate_answer
from pydantic import BaseModel
from app.services.candidate_service import get_candidate
from app.services.curriculum_service import load_curriculum
from app.services.session_service import get_session

router = APIRouter()

class EvaluationRequest(BaseModel):
    sessionId: str
    candidateId: str
    questionNumber: int
    answer: str

@router.post("/api/interview")
def interview(request: InterviewRequest):
    try:
        return start_interview(
            request.sessionId,
            request.candidateId,
            request.answer
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/evaluate")
def evaluate(request: EvaluationRequest):
    candidate = get_candidate(request.candidateId)
    curriculum = load_curriculum()
    session = get_session(request.sessionId)

    question_index = request.questionNumber - 1

    if question_index < 0 or question_index >= len(session["questions"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid question number.",
        )

    question = session["questions"][question_index]

    if question_index >= len(session["question_topics"]):
        raise HTTPException(
            status_code=400,
            detail="Curriculum topic not found for this question.",
        )

    topic_info = session["question_topics"][question_index]

    curriculum_day = next(
        (
            day
            for day in curriculum["days"]
            if day["day"] == topic_info["day"]
        ),
        None,
    )

    topic = topic_info["title"]

    objectives = (
        curriculum_day.get("objectives", [])
        if curriculum_day
        else []
    )

    return evaluate_answer(
        question=question,
        answer=request.answer,
        topic=topic,
        objectives=objectives,
        candidate_role=candidate["member"]["jobRole"],
        years_experience=candidate["member"]["yearsExperience"],
    )