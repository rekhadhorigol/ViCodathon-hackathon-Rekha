from fastapi import APIRouter, HTTPException

from app.models.interview import InterviewRequest
from app.services.interview_service import start_interview
from app.services.evaluation_service import evaluate_answer
from pydantic import BaseModel
from app.services.candidate_service import get_candidate
from app.services.curriculum_service import load_curriculum
from app.services.session_service import get_session
from app.services.overall_evaluation_service import generate_overall_evaluation
from app.services.gemini_service import GeminiServiceError

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

    except GeminiServiceError:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again.",
        )


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

    try:
        evaluation = evaluate_answer(
            question=question,
            answer=request.answer,
            topic=topic,
            objectives=objectives,
            candidate_role=candidate["member"]["jobRole"],
            years_experience=candidate["member"]["yearsExperience"],
        )
    except GeminiServiceError:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again.",
        )

    session["evaluations"].append({
        "questionNumber": request.questionNumber,
        "question": question,
        "answer": request.answer,
        "evaluation": evaluation,
    })

    return evaluation

@router.post("/evaluate/overall")
def evaluate_overall(request: EvaluationRequest):
    candidate = get_candidate(request.candidateId)
    session = get_session(request.sessionId)

    if not session["completed"]:
        raise HTTPException(
            status_code=400,
            detail="Interview is not completed yet.",
        )

    if len(session["evaluations"]) < 8:
        raise HTTPException(
            status_code=400,
            detail="All 8 question evaluations must be completed first.",
        )

    try:
        overall_evaluation = generate_overall_evaluation(
            evaluations=session["evaluations"],
            candidate_role=candidate["member"]["jobRole"],
            years_experience=candidate["member"]["yearsExperience"],
        )
    except GeminiServiceError:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again.",
        )

    session["feedback"] = overall_evaluation

    return overall_evaluation

@router.get("/api/interview/{session_id}/result")
def get_interview_result(session_id: str):
    session = get_session(session_id)

    if not session["completed"]:
        raise HTTPException(
            status_code=400,
            detail="Interview is not completed yet.",
        )

    if not session["feedback"]:
        raise HTTPException(
            status_code=400,
            detail="Overall evaluation has not been generated yet.",
        )

    return {
        "sessionId": session_id,
        "completed": session["completed"],
        "questionCount": len(session["questions"]),
        "evaluations": session["evaluations"],
        "overallEvaluation": session["feedback"],
    }