from pydantic import BaseModel


class InterviewRequest(BaseModel):
    sessionId: str
    candidateId: str
    answer: str | None = None


class InterviewResponse(BaseModel):
    question: str
    interviewComplete: bool = False