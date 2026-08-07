from fastapi import APIRouter, HTTPException

from app.models.interview import InterviewRequest
from app.services.interview_service import start_interview

router = APIRouter()


@router.post("/api/interview")
def interview(request: InterviewRequest):
    try:
        return start_interview(
            request.sessionId,
            request.candidateId
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))