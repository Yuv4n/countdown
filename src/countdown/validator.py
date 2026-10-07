"""Parsing and scoring of a player's step-by-step answer.

Expected input form: ``3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Sequence, Tuple

Step = Tuple[int, str, int, int]

_STEP = re.compile(r"^\s*(\d+)\s*([+\-*/])\s*(\d+)\s*=\s*(\d+)\s*$")
_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b if b and a % b == 0 else None,
}


@dataclass(frozen=True)
class Result:
    score: int
    exact: bool
    message: str


def parse_steps(text: str) -> List[Step]:
    """Parse a comma-separated answer into steps. Raises ``ValueError`` on bad form."""
    steps = []
    for chunk in text.split(","):
        match = _STEP.match(chunk)
        if not match:
            raise ValueError(f"Could not parse step: {chunk.strip()!r}")
        left, op, right, result = match.groups()
        steps.append((int(left), op, int(right), int(result)))
    return steps


def score(numbers: Sequence[int], target: int, steps: Sequence[Step]) -> Result:
    """Check each step against the available numbers, then score the final result.

    Scoring: 10 for an exact hit, otherwise ``10 - distance`` (floored at 0).
    """
    pool = list(numbers)
    for left, op, right, result in steps:
        try:
            pool.remove(left)
            pool.remove(right)
        except ValueError:
            return Result(0, False, "Uses a number that is not available.")
        if _OPS[op](left, right) != result:
            return Result(0, False, "Contains incorrect arithmetic.")
        pool.append(result)

    final = steps[-1][3]
    if final == target:
        return Result(10, True, "Exact solution. Score: 10")
    points = max(0, 10 - abs(final - target))
    return Result(points, False, f"{abs(final - target)} away from the target. Score: {points}")
