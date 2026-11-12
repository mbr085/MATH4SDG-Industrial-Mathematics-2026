# SPDX-License-Identifier: MIT
"""Generate synthetic daily temperatures for OFFLINE teaching (not climate observations).

The series deliberately mixes an artificial warming trend, annual seasonality,
serial dependence, missing days, and an unexplained 2008 discontinuity.
It is not intended to resemble any particular Tanzanian weather station.
"""
from pathlib import Path

import numpy as np
import pandas as pd

START = "1986-01-01"
END = "2025-12-31"
SEED = 20261111


def generate(seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(START, END, freq="D")
    n = len(dates)
    elapsed_years = np.arange(n) / 365.2425
    season = 1.8 * np.sin(2 * np.pi * elapsed_years + 0.5)
    innovations = rng.normal(0, 0.8, n)
    weather = np.empty(n)
    weather[0] = innovations[0]
    for i in range(1, n):
        weather[i] = 0.80 * weather[i - 1] + innovations[i]
    # NOT climate evidence: artificial station step and artificial trend.
    jump = 0.55 * (dates >= pd.Timestamp("2008-01-01"))
    temp = 26.0 + 0.020 * elapsed_years + season + weather + jump
    missing = rng.random(n) < 0.05
    # Missing entire seasonal blocks can strongly bias naive annual averages.
    missing |= (dates >= "1997-03-01") & (dates <= "1997-05-20")
    missing |= (dates >= "2010-08-01") & (dates <= "2010-10-20")
    temp = np.where(missing, np.nan, temp)
    return pd.DataFrame({"date": dates, "temp": temp})


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "data" / "synthetic_daily_temperature.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    generate().to_csv(path, index=False, float_format="%.3f")
    print(f"SYNTHETIC (NOT OBSERVED) temperatures written to {path}")


if __name__ == "__main__":
    main()
