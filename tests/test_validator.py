import unittest

from countdown import parse_steps, score


class ParseTest(unittest.TestCase):
    def test_parses_example(self):
        self.assertEqual(
            parse_steps("3 + 4 = 7, 7 * 2 = 14"), [(3, "+", 4, 7), (7, "*", 2, 14)]
        )

    def test_rejects_malformed_input(self):
        for bad in ["", "3 + 4", "a + b = c", "3 ^ 4 = 81", "3 + 4 = 7,"]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_steps(bad)


class ScoreTest(unittest.TestCase):
    nums = [2, 3, 3, 4, 7, 25]

    def test_exact(self):
        result = score(self.nums, 14, parse_steps("3 + 4 = 7, 7 * 2 = 14"))
        self.assertEqual((result.score, result.exact), (10, True))

    def test_near_miss_scores_partial(self):
        self.assertEqual(score(self.nums, 15, parse_steps("3 + 4 = 7")).score, 2)

    def test_too_far_scores_zero(self):
        self.assertEqual(score(self.nums, 500, parse_steps("3 + 4 = 7")).score, 0)

    def test_unavailable_number(self):
        self.assertEqual(score(self.nums, 9, parse_steps("9 + 0 = 9")).score, 0)

    def test_number_cannot_be_reused(self):
        self.assertEqual(score(self.nums, 8, parse_steps("4 + 4 = 8")).score, 0)

    def test_bad_arithmetic_and_inexact_division(self):
        self.assertEqual(score(self.nums, 8, parse_steps("3 + 4 = 8")).score, 0)
        self.assertEqual(score(self.nums, 3, parse_steps("7 / 2 = 3")).score, 0)

    def test_intermediate_results_are_reusable(self):
        steps = parse_steps("3 + 4 = 7, 7 + 7 = 14")  # second 7 is the original
        self.assertTrue(score(self.nums, 14, steps).exact)


if __name__ == "__main__":
    unittest.main()
