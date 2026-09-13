from typing import TypedDict


class State(TypedDict):

    problem: str
    pattern: str
    difficulty: str
    
    user_answer: str

    hint_level: int
    current_hint: str

    evaluation: str
    solved: bool

    time_complexity: str
    space_complexity: str