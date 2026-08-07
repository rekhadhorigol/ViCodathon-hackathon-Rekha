import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


def generate_question(prompt: str) -> str:
    """Generate an interview question using Gemini."""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()

if __name__ == "__main__":
    print(generate_question(
        "Ask one technical interview question about RAG."
    ))