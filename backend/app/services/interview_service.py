from app.models.interview import InterviewResponse


def start_interview():
    return InterviewResponse(
        question="Welcome! Let's begin your AI technical interview.",
        interviewComplete=False
    )