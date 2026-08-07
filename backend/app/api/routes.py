from fastapi import APIRouter

from app.models.interview import InterviewRequest
from app.services.interview_service import start_interview

router = APIRouter()


@router.post("/api/interview")
def interview(request: InterviewRequest):
    return start_interview()