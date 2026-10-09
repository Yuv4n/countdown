# Search and game notes

I kept solver, answer validation and interactive play in separate modules. The solver returns a path instead of storing a global result, so the game can print the arithmetic that produced the answer.

Search states are sorted tuples of the remaining numbers. A visited set removes equivalent states; duplicate pairs and identity operations are skipped. Each pair yields addition, multiplication, positive subtraction and exact division where legal. Search stops on an exact target, or keeps the nearest value if none is found.

The game starts the solver in a background thread while it waits for the player's answer. There is no timer on that answer; a 30-second join limits the later wait for the solver.

The regex parser accepts a list of arithmetic steps. Validation consumes operands from an available-number pool and appends each result. It checks reuse and arithmetic, but does not reject every non-positive intermediate result. That gap should be closed before describing validation as enforcing all game rules.

Run a seeded benchmark from the repository root with `PYTHONPATH=src python3 scripts/benchmark.py --trials 200 --seed 1`. It measures reachable targets for sampled draws, not the speed of every call to `solve()`. The earlier README table was removed because its run environment and raw output were not saved.

Possible next work: a player timer and further move ordering. These are not implemented features. Original development history remains in Git.
