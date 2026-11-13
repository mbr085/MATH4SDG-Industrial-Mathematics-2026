# SPDX-License-Identifier: MIT
"""Offline checks for an entirely synthetic insurance-claims exercise."""
import unittest

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_poisson_deviance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from tools.insurance_methods import (
    aggregate_rate, poisson_rate_interval, split_by_time, validate,
)
from tools.synthetic_insurance import SEED, SYNTHETIC_MARKER, generate


class SyntheticInsuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = generate(n_establishments=120, seed=SEED)

    @staticmethod
    def example_model(train):
        """Mirror the transparent fit that students see in the notebook."""
        features = ["sector", "zone", "programme"]
        X = train[features].fillna("Unreported")
        rate = train["claims_count"] / train["worker_years"]
        encoder = ColumnTransformer([
            ("categories", OneHotEncoder(handle_unknown="ignore"), features)
        ])
        model = Pipeline([
            ("features", encoder),
            ("poisson", PoissonRegressor(alpha=0.02, max_iter=1000)),
        ])
        model.fit(X, rate, poisson__sample_weight=train["worker_years"].to_numpy())
        return model

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

    def test_model_predicts_positive_counts_without_hidden_helper(self):
        train, test = split_by_time(self.df)
        model = self.example_model(train)
        predicted_rate = model.predict(test[["sector", "zone", "programme"]].fillna("Unreported"))
        predicted_counts = predicted_rate * test["worker_years"].to_numpy()
        self.assertEqual(predicted_counts.shape, (len(test),))
        self.assertTrue(np.all(predicted_counts > 0))
        self.assertTrue(np.isfinite(mean_poisson_deviance(test.claims_count, predicted_counts)))
        baseline = aggregate_rate(train) * test.worker_years.to_numpy()
        self.assertTrue(np.isfinite(mean_poisson_deviance(test.claims_count, baseline)))

    def test_exposure_weighted_rate_deviance_identity(self):
        train, test = split_by_time(self.df)
        predicted_counts = aggregate_rate(train) * test.worker_years.to_numpy()
        observed_counts = test.claims_count.to_numpy()
        exposures = test.worker_years.to_numpy()
        count_score = mean_poisson_deviance(observed_counts, predicted_counts)
        weighted_rate_score = mean_poisson_deviance(
            observed_counts / exposures,
            predicted_counts / exposures,
            sample_weight=exposures,
        )
        self.assertAlmostEqual(
            weighted_rate_score, count_score * len(test) / exposures.sum()
        )

    def test_2026_forecast_has_only_assumed_inputs(self):
        # The 2025 outcomes become historical training data for forecasting.
        scenario = self.df.loc[self.df["year"] == 2025, [
            "establishment_id", "sector", "zone", "programme", "worker_years"
        ]].copy()
        scenario["year"] = 2026
        self.assertNotIn("claims_count", scenario.columns)
        self.assertNotIn("total_claim_cost_units", scenario.columns)
        model = self.example_model(self.df)
        future_rate = model.predict(scenario[["sector", "zone", "programme"]].fillna("Unreported"))
        forecast = future_rate * scenario["worker_years"].to_numpy()
        self.assertEqual(forecast.shape, (len(scenario),))
        self.assertTrue(np.isfinite(forecast).all())
        self.assertTrue((forecast > 0).all())

    def test_rejects_unmarked_or_duplicate_records(self):
        tampered = self.df.copy()
        tampered.loc[tampered.index[0], "dataset_status"] = "OBSERVED"
        with self.assertRaises(ValueError):
            validate(tampered)
        with self.assertRaises(ValueError):
            validate(pd.concat([self.df, self.df.iloc[:1]], ignore_index=True))


if __name__ == "__main__":
    unittest.main()
