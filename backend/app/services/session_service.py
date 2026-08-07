from typing import Any

# Temporary in-memory storage
# (Database can be added later)
sessions: dict[str, dict[str, Any]] = {}


def get_session(session_id: str) -> dict[str, Any]:
    if session_id not in sessions:
        sessions[session_id] = {
            "questions": [],
            "answers": [],
            "current_question": 0,
        }

    return sessions[session_id]

def save_answer(session_id: str, answer: str) -> None:
    session = get_session(session_id)
    session["answers"].append(answer)