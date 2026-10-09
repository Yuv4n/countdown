# Countdown numbers round

A Python command-line game with a solver for the Countdown numbers round. I represented each search state as a sorted multiset of available numbers. Combining a pair reduces the state by one; memoisation skips equivalent states reached by different paths.

The solver returns steps for an exact answer or the nearest reachable value. It uses positive integer results and exact division. A separate regex parser checks submitted arithmetic against available numbers, while a background thread searches during player input.

The 14 existing tests passed during this review. The previous timing and target-coverage table had no saved run record, so it has been removed. `scripts/benchmark.py` can generate new measurements.

## Play

Python 3.9+ and the standard library, from this folder:

```sh
PYTHONPATH=src python3 -m countdown
PYTHONPATH=src python3 -m unittest discover -s tests
```

Enter comma-separated arithmetic steps using the drawn numbers, such as `3 + 4 = 7, 7 * 2 = 14`. An exact result earns 10 points; otherwise the score is `max(0, 10 - distance)`. Optional installation with `python3 -m pip install -e .` adds the `countdown` command.

There is no player countdown timer. The validator can accept zero-valued intermediate results, unlike the solver's positive-integer rule. [Development notes](docs/development-log.md) explain the search and remaining checks.

[MIT licence](LICENSE)
