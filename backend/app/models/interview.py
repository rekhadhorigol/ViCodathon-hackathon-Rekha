from typing import Any

from pydantic import BaseModel


class InterviewRequest(BaseModel):
    """Accepts both request shapes on the single POST /api/interview endpoint:

    - This project's own frontend: {sessionId, candidateId, answer}
    - technical-spec.md contract:  {sessionId, candidate}   (first turn)
                                    {sessionId, message}     (later turns)
    """

    sessionId: str
    candidateId: str | None = None
    answer: str | None = None
    candidate: dict[str, Any] | None = None
    message: str | None = None


class InterviewResponse(BaseModel):
    question: str
    interviewComplete: bool = False