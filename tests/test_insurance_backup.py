# SPDX-License-Identifier: MIT
"""Offline tests for the wholly synthetic insurance teaching investigation.

The notebook shows data checks, temporal splitting, pooled rates, Poisson
intervals, model construction and scoring directly rather than importing
separate modelling helpers.
"""
import unittest

import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_poisson_deviance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from tools.synthetic_insurance import SEED, SYNTHETIC_MARKER, generate


class SyntheticInsuranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = generate(n_establishments=120, seed=SEED)

    @staticmethod
    def time_split(df):
        train = df.loc[df["year"] < 2025].copy()
        test = df.loc[df["year"] == 2025].copy()
        return train, test

    @staticmethod
    def pooled_rate(df):
        return df["claims_count"].sum() / df["worker_years"].sum()

    @staticmethod
    def example_model(train):
        """Mirror the model-fitting cells displayed in the notebook."""
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
        self.assertFalse(self.df.duplicated(["establishment_id", "year"]).any())
        self.assertTrue(np.isfinite(self.df["worker_years"]).all())
        self.assertTrue((self.df["worker_years"] > 0).all())
        self.assertTrue(np.isfinite(self.df["claims_count"]).all())
        self.assertTrue((self.df["claims_count"] >= 0).all())
        self.assertTrue((self.df["claims_count"] == self.df["claims_count"].astype(int)).all())
        self.assertTrue(np.isfinite(self.df["total_claim_cost_units"]).all())

    def test_split_reserves_later_year(self):
        train, test = self.time_split(self.df)
        self.assertEqual(sorted(train.year.unique()), [2021, 2022, 2023, 2024])
        self.assertEqual(test.year.unique().tolist(), [2025])
        self.assertEqual(len(train) + len(test), len(self.df))

    def test_aggregate_rate_is_exposure_weighted(self):
        sub = pd.DataFrame({"claims_count": [1, 1], "worker_years": [1., 9.]})
        self.assertAlmostEqual(self.pooled_rate(sub), 0.2)
        self.assertNotAlmostEqual(self.pooled_rate(sub), 0.5 * (1 + 1 / 9))

    def test_exact_poisson_interval_formula(self):
        # The chi-squared quantiles are computed explicitly in the notebook.
        lower0 = 0.0
        upper0 = chi2.ppf(0.975, 2) / (2 * 100)
        self.assertEqual(lower0, 0.0)
        self.assertGreater(upper0, 0)
        lower = chi2.ppf(0.025, 44) / (2 * 1000)
        upper = chi2.ppf(0.975, 46) / (2 * 1000)
        self.assertLess(lower, 0.022)
        self.assertGreater(upper, 0.022)

    def test_model_predicts_positive_counts_without_hidden_helper(self):
        train, test = self.time_split(self.df)
        model = self.example_model(train)
        test_features = test[["sector", "zone", "programme"]].fillna("Unreported")
        predicted_rate = model.predict(test_features)
        predicted_counts = predicted_rate * test["worker_years"].to_numpy()
        self.assertEqual(predicted_counts.shape, (len(test),))
        self.assertTrue(np.all(predicted_counts > 0))
        self.assertTrue(np.isfinite(mean_poisson_deviance(test.claims_count, predicted_counts)))
        baseline = self.pooled_rate(train) * test.worker_years.to_numpy()
        self.assertTrue(np.isfinite(mean_poisson_deviance(test.claims_count, baseline)))

    def test_exposure_weighted_rate_deviance_identity(self):
        train, test = self.time_split(self.df)
        predicted_counts = self.pooled_rate(train) * test.worker_years.to_numpy()
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
        scenario = self.df.loc[self.df["year"] == 2025, [
            "establishment_id", "sector", "zone", "programme", "worker_years"
        ]].copy()
        scenario["year"] = 2026
        self.assertNotIn("claims_count", scenario.columns)
        self.assertNotIn("total_claim_cost_units", scenario.columns)
        model = self.example_model(self.df)
        features = scenario[["sector", "zone", "programme"]].fillna("Unreported")
        future_rate = model.predict(features)
        forecast = future_rate * scenario["worker_years"].to_numpy()
        self.assertTrue(np.isfinite(forecast).all())
        self.assertTrue((forecast > 0).all())

    def test_visible_checks_catch_invalid_records(self):
        tampered = self.df.copy()
        tampered.loc[tampered.index[0], "dataset_status"] = "OBSERVED"
        self.assertFalse(tampered["dataset_status"].eq(SYNTHETIC_MARKER).all())
        duplicate = pd.concat([self.df, self.df.iloc[:1]], ignore_index=True)
        self.assertTrue(duplicate.duplicated(["establishment_id", "year"]).any())


if __name__ == "__main__":
    unittest.main()
