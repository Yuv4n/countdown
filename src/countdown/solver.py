"""Exhaustive search solver for the Countdown numbers round.

The search space is a tree: each node is a multiset of numbers, and each edge
combines two of them with ``+ - * /`` into one, shrinking the multiset by one.
Depth is at most ``len(numbers) - 1``. Sorted-tuple memoisation collapses
permutations of the same multiset, which is what keeps six numbers tractable.

Rules follow the TV show: results must be positive integers (no negatives, no
fractions), and every number reachable along the way is a candidate answer.
"""
from __future__ import annotations

from typing import Iterator, List, Optional, Sequence, Tuple

State = Tuple[int, ...]
Move = Tuple[int, str, int, int]  # (left, operator, right, result)


def _moves(a: int, b: int) -> Iterator[Move]:
    """Yield every legal move on ``a >= b``. Identity moves (``* 1``, ``/ 1``) are pruned."""
    yield a, "+", b, a + b
    if b != 1:
        yield a, "*", b, a * b
        if a % b == 0:
            yield a, "/", b, a // b
    if a != b:
        yield a, "-", b, a - b


def _successors(state: State) -> Iterator[Tuple[State, Move]]:
    """Yield each state reachable by combining one pair, with the move used."""
    seen_pairs = set()
    for i in range(len(state) - 1):
        for j in range(i + 1, len(state)):
            pair = (state[i], state[j])  # sorted, so state[j] >= state[i]
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            rest = state[:i] + state[i + 1:j] + state[j + 1:]
            for move in _moves(state[j], state[i]):
                yield tuple(sorted(rest + (move[3],))), move


def _format(move: Move) -> str:
    left, op, right, result = move
    return f"{left} {op} {right} = {result}"


def closest(numbers: Sequence[int], target: int) -> Tuple[int, List[str]]:
    """Return the reachable value nearest ``target`` and the steps that build it.

    Stops as soon as an exact match is found. ``steps`` is empty if the best
    value is one of the starting numbers.
    """
    best_value = min(numbers, key=lambda n: abs(n - target))
    best_steps: List[str] = []
    visited = set()

    def dfs(state: State, moves: List[Move]) -> bool:
        nonlocal best_value, best_steps
        if state in visited:
            return False
        visited.add(state)
        for value in state:
            if abs(value - target) < abs(best_value - target):
                best_value, best_steps = value, [_format(m) for m in moves]
                if value == target:
                    return True
        if len(state) > 1:
            for nxt, move in _successors(state):
                moves.append(move)
                if dfs(nxt, moves):
                    return True
                moves.pop()
        return False

    dfs(tuple(sorted(numbers)), [])
    return best_value, best_steps


def solve(numbers: Sequence[int], target: int) -> Optional[List[str]]:
    """Return steps reaching ``target`` exactly, or ``None`` if impossible."""
    value, steps = closest(numbers, target)
    return steps if value == target else None


def reachable(numbers: Sequence[int]) -> set:
    """Return every value obtainable from ``numbers`` (used for benchmarking)."""
    values = set(numbers)
    visited = set()
    stack = [tuple(sorted(numbers))]
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        values.update(state)
        if len(state) > 1:
            stack.extend(nxt for nxt, _ in _successors(state))
    return values
