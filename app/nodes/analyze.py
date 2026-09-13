from pydantic import BaseModel, Field

from ..llm import llm


class ProblemAnalysis(BaseModel):

    pattern: str = Field(
        description="The primary algorithmic pattern"
    )

    difficulty: str = Field(
        description="Estimated difficulty: Easy, Medium, or Hard"
    )


def analyze_problem(state):

    prompt = f"""
You are a LeetCode algorithm coach.

Analyze this problem:

{state["problem"]}

Determine:

1. The primary algorithmic pattern.
2. The estimated difficulty.

Choose a pattern such as:

- Hash Map
- Two Pointers
- Sliding Window
- Binary Search
- Stack
- Linked List
- Tree
- DFS/BFS
- Dynamic Programming
- Greedy
- Backtracking
- Heap/Priority Queue
- Union Find
- Trie
- Graph

Return structured information.
"""

    structured_llm = llm.with_structured_output(
        ProblemAnalysis
    )

    result = structured_llm.invoke(prompt)

    return {
        "pattern": result.pattern,
        "difficulty": result.difficulty
    }