from app.problem_loader import get_problem


def test_load_existing_problem():

    problem = get_problem(1)

    assert problem["id"] == 1
    assert problem["title"] == "Two Sum"
    assert problem["description"]


def test_load_all_five_problems():

    problem_ids = [1, 200, 70, 322, 190]

    for problem_id in problem_ids:

        problem = get_problem(problem_id)

        assert problem["id"] == problem_id
        assert problem["title"]
        assert problem["description"]


def test_unknown_problem_raises_error():

    try:
        get_problem(999999)
        assert False, "Expected ValueError"

    except ValueError:
        assert True