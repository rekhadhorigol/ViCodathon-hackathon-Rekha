import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


class GeminiServiceError(Exception):
    """Raised when Gemini content generation fails after retry."""


def generate_question(prompt: str) -> str:
    """Generate an adaptive technical interview question using Gemini."""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
    except Exception as first_error:
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
        except Exception as retry_error:
            raise GeminiServiceError(
                "Gemini question generation failed after retry: "
                f"{retry_error}"
            ) from retry_error

    return response.text.strip()