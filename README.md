# Countdown

A command-line version of the *Countdown* numbers round, with an exhaustive search solver that finds an exact solution or the closest reachable value.

Given six numbers and a target between 101 and 999, combine the numbers with `+ - × ÷` (positive integers only, each number used at most once) to reach the target.

## Highlights

- **Exhaustive solver** over a combinatorial search tree, with memoisation on sorted multisets to collapse equivalent states. It searches a full six-number draw in under 0.1 s on average.
- **Closest-answer fallback** when no exact solution exists.
- **Strict answer validation**: a regex parser plus checks for number availability, arithmetic correctness and exact division, with a distance-based score.
- **Background solving**: the solver runs on a separate thread while the player thinks.
- **Tested and dependency-free**: 14 unit tests, standard library only.

## Usage

Requires Python 3.9+.

```bash
pip install -e .
countdown            # or: PYTHONPATH=src python -m countdown
```

Enter answers as comma-separated steps:

```
3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42
```

Scoring: 10 for an exact hit, otherwise `10 − distance` (minimum 0).

As a library:

```python
from countdown import solve, closest

solve([1, 2, 3, 4, 25, 100], 142)
# ['2 - 1 = 1', '3 - 1 = 2', '25 + 4 = 29', '100 - 29 = 71', '71 * 2 = 142']
```

## Solver performance

Fraction of targets (101–999) reachable from a random draw, estimated from 200 random draws per configuration (`python scripts/benchmark.py --trials 200 --seed 1`):

| Large numbers | Targets reachable | Mean search time |
|---|---|---|
| 0 | 87.0% | 0.03 s |
| 1 | 97.7% | 0.05 s |
| 2 | 97.8% | 0.07 s |
| 3 | 94.4% | 0.09 s |
| 4 | 91.3% | 0.09 s |

## Project structure

```
src/countdown/
  solver.py       exhaustive search: solve(), closest(), reachable()
  validator.py    answer parsing and scoring
  game.py         interactive CLI round
tests/            unit tests for solver and validator
scripts/          Monte Carlo benchmark
docs/             development log: design decisions and fixes
```

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## License

MIT
