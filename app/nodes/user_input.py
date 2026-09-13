from langgraph.types import interrupt


def get_user_answer(state):

    answer = interrupt(
        {
            "message": "Explain your approach to the problem.",
            "hint": state["current_hint"],
            "hint_level": state["hint_level"]
        }
    )

    return {
        "user_answer": answer
    }