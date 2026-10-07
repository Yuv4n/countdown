"""Interactive command-line Countdown numbers round."""
from __future__ import annotations

import random
import threading
from typing import List, Optional

from .solver import closest
from .validator import parse_steps, score

LARGE = [25, 50, 75, 100]
SMALL = [n for n in range(1, 11) for _ in range(2)]
SOLVER_TIMEOUT_S = 30


def _prompt_int(prompt: str, low: int, high: int) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if low <= value <= high:
            return value
        print(f"Please choose a number between {low} and {high}.")


def draw(large_count: int, rng: Optional[random.Random] = None) -> List[int]:
    """Draw six numbers: ``large_count`` large and the rest small."""
    rng = rng or random
    return rng.sample(LARGE, large_count) + rng.sample(SMALL, 6 - large_count)


def play() -> int:
    """Play one round and return the score."""
    large_count = _prompt_int("How many large numbers (0-4)? The rest will be small.\n", 0, 4)
    numbers = draw(large_count)
    target = random.randint(101, 999)
    print(f"Numbers: {numbers}  Target: {target}")

    # Solve in the background while the player thinks.
    outcome: dict = {}
    solver = threading.Thread(
        target=lambda: outcome.update(best=closest(numbers, target)), daemon=True
    )
    solver.start()

    while True:
        try:
            steps = parse_steps(input(
                "Enter your solution, e.g. 3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42\n"))
            break
        except ValueError as err:
            print(f"{err}. Please use the example format.")

    result = score(numbers, target, steps)
    print(result.message)

    solver.join(SOLVER_TIMEOUT_S)
    if "best" in outcome:
        value, solution = outcome["best"]
        label = "Solution" if value == target else f"Closest ({value})"
        print(f"{label}: {', '.join(solution) or 'no steps needed'}")
    return result.score
