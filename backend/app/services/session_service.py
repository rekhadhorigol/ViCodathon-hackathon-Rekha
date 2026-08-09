from typing import Any

# Temporary in-memory storage.
# A database can be added later.

sessions: dict[str, dict[str, Any]] = {}


def get_session(session_id: str) -> dict[str, Any]:
    """Return an existing interview session or create a new one."""

    if session_id not in sessions:
        sessions[session_id] = {
            "questions": [],
            "answers": [],
            "question_topics": [],
            "evaluations": [],
            "current_question": 0,
            "assessed_days": [],
            "completed": False,
            "feedback": None,
            "spec_candidate": None,
        }

    return sessions[session_id]


def save_answer(session_id: str, answer: str) -> None:
    """Save a candidate's answer to the interview session."""

    session = get_session(session_id)
    session["answers"].append(answer)