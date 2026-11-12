# SPDX-License-Identifier: MIT
"""Offline checks: all data in these tests are invented, not partner records."""
import unittest

import numpy as np
import pandas as pd

from tools.insurance_methods import (
    aggregate_rate, expected_counts, fit_frequency_model, poisson_rate_interval,
    score_claim_counts, split_by_time, validate,
)
from tools.synthetic_insurance import SEED, SYNTHETIC_MARKER, generate


class SyntheticInsuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = generate(n_establishments=120, seed=SEED)

    def test_reproducible_and_explicitly_synthetic(self):
        pd.testing.assert_frame_equal(self.df, generate(120, seed=SEED))
        self.assertTrue(self.df["dataset_status"].eq(SYNTHETIC_MARKER).all())
        self.assertEqual(len(self.df), 120 * 5)
        self.assertEqual(len(self.df[["establishment_id", "year"]].drop_duplicates()), len(self.df))
        validate(self.df)
        self.assertTrue((self.df["worker_years"] > 0).all())
        self.assertTrue((self.df["claims_count"] >= 0).all())

    def test_split_reserves_later_year(self):
        train, test = split_by_time(self.df)
        self.assertEqual(sorted(train.year.unique()), [2021, 2022, 2023, 2024])
        self.assertEqual(test.year.unique().tolist(), [2025])
        self.assertEqual(len(train) + len(test), len(self.df))

    def test_aggregate_rate_is_exposure_weighted(self):
        sub = pd.DataFrame({"claims_count": [1, 1], "worker_years": [1., 9.]})
        self.assertAlmostEqual(aggregate_rate(sub), 0.2)
        self.assertNotAlmostEqual(aggregate_rate(sub), 0.5 * (1 + 1 / 9))

    def test_rate_interval_boundaries(self):
        lo, hi = poisson_rate_interval(0, 100)
        self.assertEqual(lo, 0.)
        self.assertGreater(hi, 0.)
        low, high = poisson_rate_interval(22, 1000)
        self.assertLess(low, 0.022)
        self.assertGreater(high, 0.022)
        with self.assertRaises(ValueError):
            poisson_rate_interval(-1, 10)

    def test_model_predicts_positive_counts(self):
        train, test = split_by_time(self.df)
        model = fit_frequency_model(train)
        expected = expected_counts(model, test)
        self.assertEqual(expected.shape, (len(test),))
        self.assertTrue(np.all(expected > 0))
        self.assertTrue(np.isfinite(score_claim_counts(test.claims_count, expected)))
        self.assertTrue(np.isfinite(score_claim_counts(test.claims_count,
                          aggregate_rate(train) * test.worker_years.to_numpy())))

    def test_rejects_unmarked_or_duplicate_records(self):
        tampered = self.df.copy()
        tampered.loc[tampered.index[0], "dataset_status"] = "OBSERVED"
        with self.assertRaises(ValueError):
            validate(tampered)
        with self.assertRaises(ValueError):
            validate(pd.concat([self.df, self.df.iloc[:1]], ignore_index=True))


if __name__ == "__main__":
    unittest.main()
