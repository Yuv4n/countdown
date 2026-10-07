"""Monte Carlo estimate of how often a Countdown round is fully solvable.

For each sampled draw, one exhaustive search yields every reachable value;
solve rate is the fraction of targets in 101-999 that are reachable.

Usage: python scripts/benchmark.py [--trials N] [--seed S]
"""
import argparse
import random
import statistics
import time

from countdown import reachable
from countdown.game import draw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=30, help="draws per configuration")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    print(f"{'large':>5} {'mean target coverage':>22} {'mean search time (s)':>22}")
    for large in range(5):
        coverage, times = [], []
        for _ in range(args.trials):
            numbers = draw(large, rng)
            start = time.perf_counter()
            values = reachable(numbers)
            times.append(time.perf_counter() - start)
            coverage.append(sum(t in values for t in range(101, 1000)) / 899)
        print(f"{large:>5} {statistics.mean(coverage):>21.1%} {statistics.mean(times):>22.2f}")


if __name__ == "__main__":
    main()
