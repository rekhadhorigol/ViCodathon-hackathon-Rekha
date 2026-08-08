import json

from app.services.gemini_service import generate_question


def generate_overall_evaluation(
    evaluations: list[dict],
    candidate_role: str,
    years_experience: int,
) -> dict:
    """Generate an overall assessment from all interview evaluations."""

    evaluation_summary = "\n\n".join(
        f"""
Question {item["questionNumber"]}:
{item["question"]}

Candidate Answer:
{item["answer"]}

Evaluation:
{json.dumps(item["evaluation"], indent=2)}
"""
        for item in evaluations
    )

    prompt = f"""
You are a senior technical interviewer reviewing a completed
AI engineering interview.

Candidate:
Role: {candidate_role}
Experience: {years_experience} years

The interview contained multiple technical questions.
Below are the individual evaluations:

{evaluation_summary}

Generate an overall interview assessment.

Evaluate:
1. Overall technical capability
2. Consistency across answers
3. Depth of engineering understanding
4. Strength in practical problem solving
5. Readiness for the candidate's experience level

Return ONLY valid JSON in exactly this structure:

{{
  "overallScore": 0,
  "verdict": "DEVELOPING",
  "technicalStrength": "",
  "technicalGaps": [],
  "strongestAreas": [],
  "areasToImprove": [],
  "recommendation": ""
}}

Rules:

- overallScore must be an integer from 0 to 10.
- verdict must be exactly one of:
  "WEAK", "DEVELOPING", "STRONG", "EXCELLENT".
- Base the assessment only on the interview evidence provided.
- Do not invent skills that were not demonstrated.
- Keep the assessment appropriate for the candidate's experience level.
- Return ONLY the JSON object.
"""

    response = generate_question(prompt).strip()

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
            "Gemini returned invalid overall evaluation JSON"
        ) from exc