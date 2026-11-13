# SPDX-License-Identifier: MIT
"""Transparent methods for a synthetic exposure-based claims exercise."""

import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_poisson_deviance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["sector", "zone", "programme"]


def validate(df: pd.DataFrame) -> None:
    required = set(FEATURES + ["year", "worker_years", "claims_count",
                               "total_claim_cost_units", "dataset_status", "establishment_id"])
    if required - set(df.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(df.columns))}")
    if not df["dataset_status"].eq("SYNTHETIC_NOT_REAL").all():
        raise ValueError("This exercise requires explicitly SYNTHETIC data")
    if df.duplicated(["establishment_id", "year"]).any():
        raise ValueError("Each establishment-year must occur at most once")
    if not np.isfinite(df["worker_years"]).all() or (df["worker_years"] <= 0).any():
        raise ValueError("Exposure must be finite and strictly positive")
    if (df["claims_count"] < 0).any() or not np.isfinite(df["claims_count"]).all():
        raise ValueError("Claim counts must be non-negative and finite")
    if not np.array_equal(df["claims_count"].to_numpy(),
                          df["claims_count"].to_numpy().astype(int)):
        raise ValueError("Claim counts must be integers")
    if (df["total_claim_cost_units"] < 0).any():
        raise ValueError("Claim cost must not be negative")


def split_by_time(df: pd.DataFrame, test_year: int = 2025) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Only earlier records may train a model evaluated in test_year."""
    validate(df)
    train = df.loc[df["year"] < test_year].copy()
    test = df.loc[df["year"] == test_year].copy()
    if train.empty or test.empty or (df["year"] > test_year).any():
        raise ValueError("Need historical records and the held-out test year")
    return train, test


def aggregate_rate(df: pd.DataFrame) -> float:
    """Claims / worker-years, not the mean of row-wise claim frequencies."""
    exposure = float(df["worker_years"].sum())
    if exposure <= 0:
        raise ValueError("Total exposure must be positive")
    return float(df["claims_count"].sum() / exposure)


def poisson_rate_interval(n_claims: int, exposure: float, alpha: float = 0.05) -> tuple[float, float]:
    """Exact count-based CI divided by exposure; valid only under Poisson assumptions."""
    if not isinstance(n_claims, (int, np.integer)) or n_claims < 0 or exposure <= 0:
        raise ValueError("Requires non-negative integer claims and positive exposure")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    lo = 0.0 if n_claims == 0 else chi2.ppf(alpha / 2, 2 * n_claims) / (2 * exposure)
    hi = chi2.ppf(1 - alpha / 2, 2 * (n_claims + 1)) / (2 * exposure)
    return float(lo), float(hi)


def fit_frequency_model(train: pd.DataFrame) -> Pipeline:
    """Poisson model of claim frequency per worker-year, weighted by exposure.

    Use only historical rows with known outcomes; never fit on forecast years.
    Claims and total cost are deliberately excluded
    from FEATURES to prevent label leakage. Category preprocessing is fitted on
    training data only; unseen categories in test are ignored.
    """
    validate(train)
    X = train[FEATURES].fillna("Unreported")
    rate = train["claims_count"] / train["worker_years"]
    encoder = ColumnTransformer(
        [("categories", OneHotEncoder(handle_unknown="ignore"), FEATURES)],
        remainder="drop",
    )
    model = Pipeline([
        ("features", encoder),
        ("poisson", PoissonRegressor(alpha=0.02, max_iter=1000)),
    ])
    model.fit(X, rate, poisson__sample_weight=train["worker_years"].to_numpy())
    return model


def expected_counts(model: Pipeline, df: pd.DataFrame) -> np.ndarray:
    """Return strictly positive predicted claim counts (rate times exposure)."""
    if not (df["worker_years"] > 0).all():
        raise ValueError("Exposure must be positive")
    predicted_rate = model.predict(df[FEATURES].fillna("Unreported"))
    predicted = predicted_rate * df["worker_years"].to_numpy()
    if not np.isfinite(predicted).all() or not (predicted > 0).all():
        raise ValueError("Predicted claim counts must be finite and positive")
    return predicted


def score_claim_counts(actual: pd.Series | np.ndarray, predicted: np.ndarray) -> float:
    """Unweighted mean Poisson deviance for count predictions (smaller is better)."""
    return float(mean_poisson_deviance(actual, predicted))
