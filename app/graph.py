from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from .state import State
from .nodes.analyze import analyze_problem
from .nodes.hint import give_hint
from .nodes.evaluate import evaluate_answer
from .nodes.complexity import explain_complexity
from .nodes.user_input import get_user_answer
from .nodes.max_hints import max_hints_reached

DB_PATH = "data/coach.db"


def route_after_evaluation(state: State):

    if state["solved"]:
        return "complexity"

    if state["hint_level"] < 3:
        return "hint"

    return "max_hints"


builder = StateGraph(State)


# Nodes

builder.add_node(
    "analyze",
    analyze_problem
)

builder.add_node(
    "hint",
    give_hint
)

builder.add_node(
    "user_input",
    get_user_answer
)

builder.add_node(
    "evaluate",
    evaluate_answer
)

builder.add_node(
    "complexity",
    explain_complexity
)

builder.add_node(
    "max_hints",
    max_hints_reached
)


# Initial flow

builder.add_edge(
    START,
    "analyze"
)

builder.add_edge(
    "analyze",
    "hint"
)

builder.add_edge(
    "hint",
    "user_input"
)

builder.add_edge(
    "user_input",
    "evaluate"
)


# Evaluation routing

builder.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "hint": "hint",
        "complexity": "complexity",
        "max_hints": "max_hints"
    }
)


# Terminal nodes

builder.add_edge(
    "complexity",
    END
)

builder.add_edge(
    "max_hints",
    END
)


# SQLite checkpointing

checkpointer_context = SqliteSaver.from_conn_string(
    DB_PATH
)

checkpointer = checkpointer_context.__enter__()

graph = builder.compile(
    checkpointer=checkpointer
)