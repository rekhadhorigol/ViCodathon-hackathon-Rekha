from fastapi import APIRouter, HTTPException

from app.models.interview import InterviewRequest
from app.services.candidate_service import get_candidate

router = APIRouter()


@router.post("/api/interview")
def interview(request: InterviewRequest):
    try:
        candidate = get_candidate(request.candidateId)

        return {
            "message": "Candidate loaded successfully",
            "candidate": candidate["member"]
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))