# Countdown numbers solver

A Python command-line version of the Countdown numbers round, with a solver that finds an exact answer or the nearest reachable value.

- **Search:** each state is a sorted multiset of the remaining numbers; combining a pair shrinks it by one, and memoisation skips equivalent states reached by different paths.
- **Rules:** positive integer results and exact division only.
- **Play:** a regex parser validates the player's arithmetic against the drawn numbers while a background thread searches.
- **Tests:** 14 unit tests; `scripts/benchmark.py` generates timing measurements.

## Run

Python 3.9+, standard library only:

```sh
PYTHONPATH=src python3 -m countdown
PYTHONPATH=src python3 -m unittest discover -s tests
```

Enter steps such as `3 + 4 = 7, 7 * 2 = 14`. An exact result scores 10; otherwise `max(0, 10 - distance)`.

## Limits

No player timer. The validator accepts zero-valued intermediate results, which the solver does not. See the [development notes](docs/development-log.md).

[MIT licence](LICENSE)
