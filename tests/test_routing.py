from app.graph import route_after_evaluation


def build_state(solved, hint_level):

    return {
        "problem": "Test problem",
        "pattern": "Hash Map",
        "difficulty": "Easy",
        "user_answer": "",
        "hint_level": hint_level,
        "current_hint": "",
        "evaluation": "",
        "solved": solved,
        "time_complexity": "",
        "space_complexity": ""
    }


def test_correct_answer_routes_to_complexity():

    state = build_state(
        solved=True,
        hint_level=1
    )

    assert route_after_evaluation(state) == "complexity"


def test_wrong_answer_before_three_hints_routes_to_hint():

    for hint_level in [0, 1, 2]:

        state = build_state(
            solved=False,
            hint_level=hint_level
        )

        assert route_after_evaluation(state) == "hint"


def test_wrong_answer_after_three_hints_routes_to_max_hints():

    state = build_state(
        solved=False,
        hint_level=3
    )

    assert route_after_evaluation(state) == "max_hints"