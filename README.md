# LeetCode Coach

A local, LLM-powered coding coach that helps users practice LeetCode
problems through guided problem analysis, progressive hints, answer
evaluation, and time/space complexity feedback.

The application is built as a stateful Python CLI using LangGraph,
LangChain, Ollama, Pydantic, and SQLite. It does not require an external
LLM API key because model inference runs locally through Ollama.

## Architecture

<img width="1222" height="1287" alt="architecture" src="https://github.com/user-attachments/assets/210e78e0-2be0-4df8-b788-9a3f2c04a52c" />


The system is organized into the following layers:

-   **CLI/Application Layer** --- handles menus, user input, session
    creation, session resume, and result display.
-   **Problem Data Layer** --- loads problem details from
    `problems.json`.
-   **LangGraph Workflow Layer** --- coordinates the coaching process
    through multiple stateful nodes and conditional routing.
-   **LLM Layer** --- uses LangChain and Ollama for local model
    inference.
-   **State Management Layer** --- stores the current problem, user
    answer, hint level, evaluation, solved status, and complexity
    information.
-   **Persistence Layer** --- uses SQLite checkpointing to preserve
    session state and enable resume functionality.

## Features

-   Supports **75+ LeetCode problems** through a JSON-based problem
    repository.
-   Interactive CLI-based coaching sessions.
-   Problem analysis and algorithm-pattern identification.
-   User-answer evaluation.
-   Contextual and progressive hints.
-   Strict **3-level hint limit** per session.
-   Time and space complexity analysis.
-   Conditional routing using LangGraph.
-   Local LLM inference using Ollama.
-   No external API key required.
-   SQLite-based graph checkpoint persistence.
-   UUID-based session IDs.
-   Resume interrupted sessions.
-   `interrupt()` and `Command(resume=...)` workflow support.
-   Automated tests using pytest.

## Main Workflow

``` text
START
  |
  v
Analyze Problem
  |
  v
Generate Hint
  |
  v
Wait for User Input
  |
  v
Evaluate Answer
  |
  +------------------------------+
  |                              |
  | User solved                  | User not solved
  v                              v
Complexity Analysis        Is hint_level < 3?
  |                              |
  v                              +----------------------+
 END                             |                      |
                                 | Yes                  | No
                                 v                      v
                           Generate Next Hint     Maximum Hints
                                 |                      |
                                 +----------+-----------+
                                            |
                                            v
                                           END
```

## Technology Stack

  Technology   Purpose
  ------------ ---------------------------------------------------------
  Python       Core application and CLI implementation
  LangGraph    Stateful workflow orchestration and conditional routing
  LangChain    Prompt and LLM integration
  Ollama       Local LLM inference
  Pydantic     Structured output validation
  SQLite       Checkpoint persistence and session recovery
  JSON         Problem data storage
  pytest       Automated testing
  Git/GitHub   Version control and project hosting

## Project Structure

``` text
leetcode-coach/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── nodes.py
│   └── problem_loader.py
│
├── problems/
│   └── problems.json
│
├── data/
│   └── coach.db
│
├── tests/
│   ├── test_problem_loader.py
│   ├── test_routing.py
│   └── test_hint_limit.py
│
├── docs/
│   └── architecture.png
│
├── requirements.txt
└── README.md
```

> `coach.db` is generated when the application uses SQLite
> checkpointing. It may not exist before the first session is created.

## Prerequisites

Install the following software before running the project:

1.  Python 3.10 or later
2.  Git
3.  Ollama
4.  A compatible local Ollama model

### Install Python

Verify your Python installation:

``` bash
python --version
```

or on some systems:

``` bash
python3 --version
```

### Install Ollama

Download and install Ollama from:

https://ollama.com/

Verify that Ollama is installed:

``` bash
ollama --version
```

## Download a Local Model

Pull the model configured in your application.

For example:

``` bash
ollama pull llama3.2:3b
```

Start Ollama if it is not already running:

``` bash
ollama serve
```

In another terminal, verify that the model is available:

``` bash
ollama list
```

> If your code uses a different model name, replace `llama3.2:3b` with
> the model name configured in your project.

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/<your-username>/leetcode-coach.git
cd leetcode-coach
```

Replace `<your-username>` with your GitHub username.

### 2. Create a virtual environment

#### Windows

``` cmd
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

If `requirements.txt` does not yet contain pytest, install it with:

``` bash
pip install pytest
```

## Example Requirements

Your `requirements.txt` may contain packages similar to:

``` text
langchain
langchain-ollama
langgraph
pydantic
pytest
```

The exact versions should match the versions used in your development
environment.

## Running the Application

Run the application from the project root.

### Option 1: Run as a Python module

``` bash
python -m app.main
```

### Option 2: Run the file directly

``` bash
python app/main.py
```

The module-based command is generally recommended when your application
uses package-relative imports such as:

``` python
from .graph import graph
from .problem_loader import get_problem
```

## Application Menu

When the application starts, it displays a menu similar to:

``` text
============================================================
                  LEETCODE COACH
============================================================

1. New Session
2. Resume Session
0. Exit

Choose an option:
```

### Start a New Session

1.  Select `1`.
2.  Enter a problem ID.
3.  Read the problem analysis.
4.  Provide your solution approach.
5.  Receive evaluation or a hint.
6.  Continue until:
    -   The answer is considered solved.
    -   The maximum of 3 hints is reached.
    -   You choose to quit.

Example:

``` text
Choose an option: 1

Enter problem ID: 1

============================================================
SESSION ID: <generated-session-id>
============================================================
Save this ID if you want to resume later.
```

Save the generated session ID if you want to resume the session later.

### Resume a Session

1.  Select `2`.
2.  Enter the previously generated session ID.
3.  The application loads the saved checkpoint from SQLite.
4.  Continue the coaching workflow.

Example:

``` text
Choose an option: 2

Enter session ID: <previous-session-id>
```

## Testing

Run all tests from the project root:

``` bash
pytest tests -v
```

Run the hint-limit tests only:

``` bash
pytest tests/test_hint_limit.py -v
```

Run the routing tests only:

``` bash
pytest tests/test_routing.py -v
```

Run the problem-loader tests only:

``` bash
pytest tests/test_problem_loader.py -v
```

## Current Test Coverage

The project includes automated tests for:

-   Hint limit enforcement.
-   Hint routing when the hint level is below 3.
-   Routing solved answers to complexity analysis.
-   Problem loading by problem ID.
-   Problem lookup behavior.

The current hint-limit test suite validates these scenarios:

``` python
def test_hint_limit_is_three():
    state = {
        "solved": False,
        "hint_level": 3
    }

    result = route_after_evaluation(state)

    assert result == "max_hints"
```

``` python
def test_hint_is_allowed_below_three():
    state = {
        "solved": False,
        "hint_level": 2
    }

    result = route_after_evaluation(state)

    assert result == "hint"
```

``` python
def test_solved_user_goes_to_complexity():
    state = {
        "solved": True,
        "hint_level": 0
    }

    result = route_after_evaluation(state)

    assert result == "complexity"
```

## Routing Logic

The main routing rule is:

``` python
def route_after_evaluation(state):
    if state["solved"]:
        return "complexity"

    if state["hint_level"] < 3:
        return "hint"

    return "max_hints"
```

This ensures:

-   Solved problems go to complexity analysis.
-   Unsolved problems below hint level 3 receive another hint.
-   Unsolved problems at hint level 3 go to the maximum-hints terminal
    state.
-   A fourth hint is not generated.

## Example Graph Configuration

The graph uses conditional edges similar to:

``` python
builder.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "hint": "hint",
        "complexity": "complexity",
        "max_hints": "max_hints",
    },
)

builder.add_edge("complexity", END)
builder.add_edge("max_hints", END)
```

## Session Persistence

The application uses SQLite checkpointing to preserve graph state.

The saved state may contain information such as:

``` text
problem
pattern
difficulty
user_answer
hint_level
current_hint
evaluation
solved
time_complexity
space_complexity
```

This allows the application to recover an interrupted session and
continue from the saved workflow state.

## Design Decisions

### Why LangGraph?

LangGraph is used because the application requires:

-   Stateful execution.
-   Conditional routing.
-   Multiple workflow nodes.
-   Interrupt-and-resume behavior.
-   Persistent checkpoints.
-   Explicit terminal states.

### Why Ollama?

Ollama allows the application to run an LLM locally:

-   No external API key.
-   No cloud inference dependency.
-   Better control over local development.
-   Useful for experimenting with LLM workflows.

### Why SQLite?

SQLite provides a lightweight persistence layer for:

-   Session checkpoints.
-   Workflow state.
-   Resume functionality.
-   Local development without a separate database server.

### Why JSON for Problems?

JSON keeps problem data separate from application code and makes it easy
to:

-   Add new problems.
-   Update descriptions.
-   Store difficulty and metadata.
-   Load problems by ID.

## Error Handling

The application handles common user-input scenarios such as:

-   Invalid menu choices.
-   Unknown problem IDs.
-   Invalid session IDs.
-   User quit commands.
-   Missing session checkpoints.
-   Maximum hint limit reached.

## Metrics

Current project metrics include:

-   **75+ LeetCode problems** in the problem repository.
-   **5+ workflow nodes**, depending on the final graph configuration.
-   **3 conditional execution paths** after answer evaluation.
-   **3-level hint system**.
-   **SQLite-based session persistence**.
-   **UUID-based session identification**.
-   **3 automated pytest scenarios** for core routing and hint-limit
    behavior.
-   **100% pass rate** for the currently executed 3 routing tests.

## Limitations

-   The application currently runs as a CLI rather than a web
    application.
-   Response quality depends on the selected local Ollama model.
-   Local inference may be slower on systems with limited RAM or CPU/GPU
    resources.
-   The project does not currently include authentication or multi-user
    access control.
-   SQLite persistence is intended for local usage and development.
-   Model output quality may vary for complex algorithmic problems.

## Future Improvements

-   Add a web interface using FastAPI and React.
-   Add REST APIs for problem sessions and user progress.
-   Add authentication and user profiles.
-   Add difficulty-based problem recommendations.
-   Add topic-based filtering.
-   Add session history and progress dashboards.
-   Add model response caching.
-   Add automated integration tests with mocked LLM responses.
-   Add latency and token-usage metrics.
-   Add Docker support.
-   Add CI/CD using GitHub Actions.
-   Add support for multiple local Ollama models.
-   Add code submission and test-case execution.
-   Add personalized learning plans.
-   Add a PostgreSQL persistence option for multi-user deployments.

## Troubleshooting

### `ModuleNotFoundError` when running the application

Run the application from the project root:

``` bash
python -m app.main
```

Do not run it from inside the `app` directory when using relative
imports.

### Ollama connection error

Make sure Ollama is running:

``` bash
ollama serve
```

Also verify that the configured model is installed:

``` bash
ollama list
```

### Model not found

Pull the required model:

``` bash
ollama pull llama3.2:3b
```

Then update the model name in your code if necessary.

### Tests cannot import the `app` package

Make sure:

-   You are running pytest from the project root.
-   `app/__init__.py` exists.
-   The virtual environment is activated.
-   Dependencies are installed.

Run:

``` bash
pytest tests -v
```

### Session cannot be resumed

Check that:

-   The session ID was copied correctly.
-   The SQLite database still exists.
-   The application is using the same checkpoint database.
-   The session was created using the current application configuration.

## GitHub Setup

Initialize Git if needed:

``` bash
git init
```

Add files:

``` bash
git add .
```

Create the first commit:

``` bash
git commit -m "Initial commit for LeetCode Coach"
```

Authenticate with GitHub CLI:

``` bash
gh auth login
```

Create the GitHub repository and push:

``` bash
gh repo create leetcode-coach --public --source=. --remote=origin --push
```

For later changes:

``` bash
git status
git add .
git commit -m "Update coaching workflow"
git push
```

## Recommended `.gitignore`

Create a `.gitignore` file in the project root:

``` gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.env
data/*.db
.idea/
.vscode/
.DS_Store
```

Do not commit secrets, virtual environments, cache folders, or local
SQLite databases unless you intentionally want to share them.

## Project Status

The project currently provides:

-   Local LLM-powered coaching.
-   Stateful LangGraph orchestration.
-   Conditional hint and complexity routing.
-   Three-level hint enforcement.
-   SQLite session checkpointing.
-   New-session and resume-session support.
-   Automated routing tests.

## License

This project is available for educational and portfolio use. Add a
license file if you plan to distribute or reuse the project publicly.
