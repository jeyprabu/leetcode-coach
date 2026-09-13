from app.graph import route_after_evaluation


def test_hint_limit_is_three():
    state = {
        "solved": False,
        "hint_level": 3
    }

    result = route_after_evaluation(state)

    assert result == "max_hints"


def test_hint_is_allowed_below_three():
    state = {
        "solved": False,
        "hint_level": 2
    }

    result = route_after_evaluation(state)

    assert result == "hint"


def test_solved_user_goes_to_complexity():
    state = {
        "solved": True,
        "hint_level": 0
    }

    result = route_after_evaluation(state)

    assert result == "complexity"