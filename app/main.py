import uuid

from langgraph.types import Command
from .graph import graph
from .problem_loader import get_problem

def main():

    print("=" * 60)
    print("                  LEETCODE COACH")
    print("=" * 60)

    while True:

        print("\n1. New Session")
        print("2. Resume Session")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            start_new_session()

        elif choice == "2":
            resume_session()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


def start_new_session():

    try:
        problem_id = int(
            input("\nEnter problem ID: ")
        )

    except ValueError:
        print("Please enter a valid number.")
        return

    try:
        problem = get_problem(problem_id)

    except ValueError as e:
        print(e)
        return

    thread_id = str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("\n" + "=" * 60)
    print(f"SESSION ID: {thread_id}")
    print("=" * 60)

    print("Save this ID if you want to resume later.")

    print("\n" + "=" * 60)
    print(problem["title"])
    print("=" * 60)

    print(f"Difficulty: {problem['difficulty']}")

    print("\nProblem:")
    print(problem["description"])

    state = {
        "problem": problem["description"],
        "pattern": "",
        "difficulty": problem["difficulty"],

        "user_answer": "",

        "hint_level": 0,
        "current_hint": "",

        "evaluation": "",
        "solved": False,

        "time_complexity": "",
        "space_complexity": ""
    }

    run_graph(
        state,
        config
    )


def run_graph(state, config):

    result = graph.invoke(
        state,
        config
    )

    handle_result(config)
    

def handle_result(config):
    while True:

        checkpoint = graph.get_state(config)

        # GRAPH IS WAITING FOR USER INPUT
        
        if checkpoint.interrupts:

            interrupt_data = checkpoint.interrupts[0].value

            print("\n" + "-" * 60)
            print("COACH")
            print("-" * 60)

            print(
                f"\nHint #{interrupt_data['hint_level']}:"
            )

            print(interrupt_data["hint"])

            print("\nExplain your approach.")
            print("Type 'quit' to save and exit.")

            answer = input("\nYou: ")

            if answer.lower() == "quit":

                print("\nSession saved.")

                print(
                    f"Resume using: "
                    f"{config['configurable']['thread_id']}"
                )

                return
            
            # Resume the interrupted graph
            
            graph.invoke(
                Command(resume=answer),
                config
            )

            continue

        # GRAPH HAS FINISHED
    
        state = checkpoint.values

        # SOLVED

        if state["solved"]:

            print("\n" + "-" * 60)
            print("COACH")
            print("-" * 60)

            print(state["evaluation"].capitalize())

            print("\n🎉 Excellent!")

            print(
                f"\nTime Complexity: "
                f"{state['time_complexity']}"
            )

            print(
                f"Space Complexity: "
                f"{state['space_complexity']}"
            )

            return

        # MAX HINTS
 
        if state["hint_level"] >= 3:

            print("\n" + "-" * 60)
            print("COACH")
            print("-" * 60)

            print(state["evaluation"])

            print("\nMaximum of 3 hints reached.")
            print("This session has ended.")

            return

        # SAFETY FALLBACK

        return


def resume_session():

    thread_id = input(
        "\nEnter your session ID: "
    ).strip()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        checkpoint = graph.get_state(
            config
        )

    except Exception as e:

        print("\nCould not load session.")
        print(e)
        return

    if not checkpoint.values:

        print("\nSession not found.")
        return

    print("\n" + "=" * 60)
    print("SESSION RESUMED")
    print("=" * 60)

    state = checkpoint.values

    print("\nProblem:")
    print(state["problem"])


    # Resume from exactly where LangGraph stopped

    handle_result(config)


if __name__ == "__main__":
    main()