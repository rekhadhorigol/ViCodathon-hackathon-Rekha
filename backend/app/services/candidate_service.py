from pathlib import Path
import json
from typing import Any


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CANDIDATES_FILE = DATA_DIR / "candidates.json"


def load_candidates() -> list[dict[str, Any]]:
    """
    Load all candidates.

    Returns:
        List of candidate dictionaries.

    Raises:
        FileNotFoundError
        ValueError
    """

    if not CANDIDATES_FILE.exists():
        raise FileNotFoundError(
            f"Candidate file not found: {CANDIDATES_FILE}"
        )

    try:
        with CANDIDATES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if "candidates" not in data:
                raise ValueError("Invalid candidates.json format")

            return data

    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON in candidates.json") from e


def get_candidate(candidate_id: str) -> dict[str, Any]:
    """Retrieve a candidate by ID.

    Args:
        candidate_id: Candidate identifier.

    Returns:
        Candidate dictionary.

    Raises:
        ValueError: If candidate does not exist.
    """
    data = load_candidates()
    candidates = data["candidates"]

    for candidate in candidates:
        if candidate["member"]["id"] == candidate_id:
            return candidate

    raise ValueError(f"Candidate '{candidate_id}' not found.")