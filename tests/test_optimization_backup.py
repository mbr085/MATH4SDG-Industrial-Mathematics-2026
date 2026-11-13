# SPDX-License-Identifier: MIT
"""Offline check for the entirely fictional worker-job assignment example."""
import itertools
import unittest

import numpy as np
from scipy.optimize import linear_sum_assignment


class AssignmentOptimizationBackupTests(unittest.TestCase):
    def test_example_is_feasible_optimal_and_not_unique(self):
        hours = np.array([
            [6, 4, np.inf, 7],
            [5, 8, 6, 5],
            [np.inf, 3, 7, 6],
            [7, np.inf, 4, 3],
        ])

        rows, cols = linear_sum_assignment(hours)
        self.assertEqual(sorted(rows.tolist()), [0, 1, 2, 3])
        self.assertEqual(sorted(cols.tolist()), [0, 1, 2, 3])
        self.assertTrue(np.isfinite(hours[rows, cols]).all())
        self.assertEqual(hours[rows, cols].sum(), 18.0)

        feasible_totals = [
            hours[range(4), assignment].sum()
            for assignment in itertools.permutations(range(4))
            if np.isfinite(hours[range(4), assignment]).all()
        ]
        self.assertEqual(min(feasible_totals), 18.0)
        self.assertGreaterEqual(feasible_totals.count(18.0), 2)


if __name__ == "__main__":
    unittest.main()
