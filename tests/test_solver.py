import unittest

from countdown import closest, reachable, solve


def replay(numbers, steps):
    """Apply solver steps to the starting numbers; return the final pool."""
    pool = list(numbers)
    for step in steps:
        lhs, rhs = step.split(" = ")
        a, op, b = lhs.split()
        a, b, c = int(a), int(b), int(rhs)
        pool.remove(a)
        pool.remove(b)
        assert {"+": a + b, "-": a - b, "*": a * b, "/": a // b}[op] == c
        pool.append(c)
    return pool


class SolverTest(unittest.TestCase):
    def test_known_solution_is_valid(self):
        numbers, target = [1, 2, 3, 4, 25, 100], 142
        steps = solve(numbers, target)
        self.assertIsNotNone(steps)
        self.assertIn(target, replay(numbers, steps))

    def test_unsolvable_returns_none(self):
        self.assertIsNone(solve([1, 1], 5))

    def test_closest_when_no_exact_match(self):
        value, steps = closest([1, 1], 5)
        self.assertEqual(value, 2)
        self.assertIn(2, replay([1, 1], steps))

    def test_no_negative_or_fractional_intermediates(self):
        self.assertTrue(all(v > 0 for v in reachable([3, 5, 7, 8, 50, 100])))

    def test_division_must_be_exact(self):
        self.assertIsNone(solve([7, 2], 3))  # 7 / 2 is not an integer


if __name__ == "__main__":
    unittest.main()
