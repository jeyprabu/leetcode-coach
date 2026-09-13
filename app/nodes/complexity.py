from pydantic import BaseModel, Field

from ..llm import llm


class ComplexityResponse(BaseModel):

    time_complexity: str = Field(
        description="Time complexity such as O(n), O(n log n), etc."
    )

    space_complexity: str = Field(
        description="Space complexity such as O(1), O(n), etc."
    )

    explanation: str = Field(
        description="Short explanation of the time and space complexity"
    )


def explain_complexity(state):

    prompt = f"""
You are a LeetCode coach.

Problem:
{state["problem"]}

Algorithmic pattern:
{state["pattern"]}

Student's approach:
{state["user_answer"]}

The student's approach has been judged correct.

Determine:

1. Time complexity
2. Space complexity

Explain briefly why.

Do not provide code.
"""

    structured_llm = llm.with_structured_output(
        ComplexityResponse
    )

    result = structured_llm.invoke(prompt)

    return {
        "time_complexity": result.time_complexity,
        "space_complexity": result.space_complexity
    }