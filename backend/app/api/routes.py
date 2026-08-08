from fastapi import APIRouter, HTTPException

from app.models.interview import InterviewRequest
from app.services.interview_service import start_interview
from app.services.evaluation_service import evaluate_answer
from pydantic import BaseModel

router = APIRouter()

class EvaluationRequest(BaseModel):
    candidateId: str
    question: str
    answer: str
    topic: str
    objectives: list[str]
    role: str
    yearsExperience: int

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
    return evaluate_answer(
        question=request.question,
        answer=request.answer,
        topic=request.topic,
        objectives=request.objectives,
        candidate_role=request.role,
        years_experience=request.yearsExperience,
    )