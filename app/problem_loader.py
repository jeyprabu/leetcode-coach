import json
from pathlib import Path


PROBLEMS_FILE = (
    Path(__file__).parent.parent
    / "problems"
    / "problems.json"
)


def get_problem(problem_id: int) -> dict:

    with open(PROBLEMS_FILE, "r", encoding="utf-8") as file:
        problems = json.load(file)

    for problem in problems:
        if problem["id"] == problem_id:
            return problem

    raise ValueError(
        f"Problem {problem_id} not found"
    )