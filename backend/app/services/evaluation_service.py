import json

from app.services.gemini_service import generate_question


def evaluate_answer(
    question: str,
    answer: str,
    topic: str,
    objectives: list[str],
    candidate_role: str,
    years_experience: int,
) -> dict:
    """Evaluate a candidate's technical interview answer."""

    prompt = f"""
You are an expert technical interviewer evaluating a candidate
for an AI engineering role.

Candidate:
Role: {candidate_role}
Experience: {years_experience} years

Curriculum topic:
{topic}

Learning objectives:
{objectives}

Interview question:
{question}

Candidate answer:
{answer}

Evaluate the candidate's answer based on:

1. Technical accuracy
2. Depth of understanding
3. Clarity of explanation
4. Relevance to the question
5. Appropriateness for the candidate's experience level

Return ONLY valid JSON in exactly this structure:

{{
  "score": 0,
  "verdict": "WEAK",
  "technicalAccuracy": 0,
  "depth": 0,
  "clarity": 0,
  "feedback": "",
  "strengths": [],
  "improvements": []
}}

Scoring rules:

- All scores must be integers from 0 to 10.
- "score" is the overall assessment.
- "verdict" must be exactly one of:
  "WEAK", "DEVELOPING", "STRONG", "EXCELLENT".
- Do not reward confident wording if the technical content is incorrect.
- Do not penalize concise answers when they correctly address the question.
- Judge the answer against the candidate's experience level.
- Do not provide information that was not asked for.
- Return ONLY the JSON object.
"""

    response = generate_question(prompt)

    # Remove Markdown code fences if Gemini adds them.
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Gemini returned invalid evaluation JSON"
        ) from exc