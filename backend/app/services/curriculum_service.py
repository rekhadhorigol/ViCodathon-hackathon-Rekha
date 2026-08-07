from pathlib import Path
import json
from typing import Any


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CURRICULUM_FILE = DATA_DIR / "curriculum.json"


def load_curriculum() -> dict[str, Any]:
    """
    Load and return the curriculum JSON data.

    Returns:
        Parsed curriculum as a dictionary.

    Raises:
        FileNotFoundError: If curriculum.json does not exist.
        ValueError: If curriculum.json contains invalid JSON.
    """

    if not CURRICULUM_FILE.exists():
        raise FileNotFoundError(
            f"Curriculum file not found: {CURRICULUM_FILE}"
        )

    try:
        with CURRICULUM_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

            required_keys = {"cohort", "modules", "days"}

            if not required_keys.issubset(data):
                raise ValueError("Invalid curriculum.json format")

            return data

    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON in curriculum.json") from e


def get_day(day_number: int) -> dict[str, Any]:
    curriculum = load_curriculum()

    for day in curriculum["days"]:
        if day["day"] == day_number:
            return day

    raise ValueError(f"Day {day_number} not found.")