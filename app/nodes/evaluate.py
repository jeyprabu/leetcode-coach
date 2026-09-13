from pydantic import BaseModel, Field

from ..llm import llm


class EvaluationResponse(BaseModel):
    evaluation: str = Field(
        description="Concise feedback about the student's approach"
    )

    solved: bool = Field(
        description="True if the student's approach is correct and sufficiently efficient"
    )


def evaluate_answer(state):

    prompt = f"""
You are a LeetCode coach evaluating a student's approach.

Problem:
{state["problem"]}

Expected algorithmic pattern:
{state["pattern"]}

Student's answer:
{state["user_answer"]}

Evaluate the student's approach.

Determine:

1. Is the core algorithm correct?
2. Does it solve the problem?
3. Is it reasonably efficient?
4. Has the student identified the important technique?

Set solved=true ONLY when the student has identified
a correct and sufficiently efficient approach.

If the approach is wrong or incomplete:
- Explain what is wrong.
- Give useful feedback.
- Do NOT provide the complete solution.
- Do NOT provide code.

If the approach is correct:
- Tell the student that the approach is correct.
- Briefly explain why.
- Do NOT provide code.

Keep the feedback concise.
"""

    structured_llm = llm.with_structured_output(
        EvaluationResponse
    )

    result = structured_llm.invoke(prompt)

    return {
        "evaluation": result.evaluation,
        "solved": result.solved
    }