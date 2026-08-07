from app.services.candidate_service import get_candidate


def start_interview(candidate_id: str):
    candidate = get_candidate(candidate_id)

    completed = [
        mission
        for mission in candidate["missions"]
        if mission.get("passed")
    ]

    if not completed:
        return {
            "question": "Tell me about yourself and your AI learning journey."
        }

    latest = completed[-1]

    return {
        "question": f"You completed '{latest['title']}'. Can you explain this concept in your own words?"
    }