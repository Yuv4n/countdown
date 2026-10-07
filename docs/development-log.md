# Development Log

Design decisions and lessons from building the project (June 2025).

## Design decisions

- **Functional over OOP.** The problem is a pipeline of pure transformations (draw → solve → validate → score), so plain functions fit better than classes.
- **`try/except` for input validation.** I prototyped a hand-rolled `is_number` check (O(n) time, O(1) space) to avoid exceptions. Re-assigning values to convert types was awkward and no clearer, so I reverted to `try/except`.
- **Solver as tree search.** Each node is a set of numbers; each edge merges two of them with one operator, shrinking the set by one. The branching factor is at most 6 per pair (`+`, `*`, two `-`, two `/`).
- **Track the path.** The first version returned only a boolean. Carrying the step history with each node lets the solver print a working solution.
- **Concurrency.** The solver runs in a background thread while the player thinks.

## Problems found and fixed

| Problem | Resolution |
|---|---|
| Recursion unwound step by step, so only the final step of a solution was returned | Pass the accumulated history down and return it on success |
| Global variable used to carry the result | Return values instead |
| No answer when an exact solution doesn't exist | Added `closest()`, which tracks the best reachable value |
| Duplicate states explored repeatedly (exponential blow-up) | Memoise on sorted tuples of the remaining numbers |
| Negative intermediates and `a / b` float checks via `str(n)` | Positive integers only, exact division with `%` |
| `break` on a failed division skipped the reverse-division case | Enumerate moves per ordered pair with `continue` semantics |
| Malformed input could raise `IndexError` | Regex-based parser raising `ValueError` |

## Ideas not yet done

- Enforce a countdown timer on the player's input.
- Prune symmetric moves further to speed up the exhaustive search.
- Learned or heuristic move ordering to reach a first solution faster.
