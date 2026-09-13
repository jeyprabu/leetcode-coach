from pydantic import BaseModel, Field

from ..llm import llm


class HintResponse(BaseModel):
    hint: str = Field(
        description="A short hint that helps the student without revealing the solution"
    )


def give_hint(state):
    hint_level = state["hint_level"]

    prompt = f"""
You are a LeetCode coach.

Your job is to help a student solve a problem without
immediately giving them the solution.

Problem:
{state["problem"]}

Algorithmic pattern:
{state["pattern"]}

Current hint level:
{hint_level + 1}

Generate ONE hint.

Follow these rules:

Hint level 1:
Give a high-level conceptual direction.
Do not mention the exact data structure if possible.

Hint level 2:
Point toward the relevant data structure or technique.

Hint level 3:
Give a strong algorithmic hint that almost leads to the solution,
but do not provide code.

Never provide the complete solution.
Never provide code.
Never directly say "the answer is ...".

Keep the hint concise and educational.
"""

    structured_llm = llm.with_structured_output(HintResponse)

    result = structured_llm.invoke(prompt)

    return {
        "current_hint": result.hint,
        "hint_level": hint_level + 1
    }