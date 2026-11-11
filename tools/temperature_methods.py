# SPDX-License-Identifier: MIT
"""Small transparent functions for annual temperature summaries and regression."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


def annual_means(daily_temp: pd.Series, min_days_per_month: int = 20) -> tuple[pd.Series, pd.DataFrame]:
    """Equal-weight 12 calendar months; omit any year with an inadequate month.

    A missing month is NEVER replaced by the previous day or the model estimate.
    This conservative rule can itself select particular years: inspect exclusions.
    """
    if not isinstance(daily_temp.index, pd.DatetimeIndex):
        raise TypeError("daily_temp must have a DatetimeIndex")
    if not 1 <= min_days_per_month <= 28:
        raise ValueError("min_days_per_month must be between 1 and 28")
    daily_temp = pd.to_numeric(daily_temp, errors="coerce").sort_index()
    if daily_temp.index.has_duplicates:
        raise ValueError("duplicate dates: resolve explicitly before analysis")
    daily_temp = daily_temp.asfreq("D")
    monthly = daily_temp.resample("MS").agg(["mean", "count"])
    monthly["qualified"] = monthly["mean"].where(monthly["count"] >= min_days_per_month)
    table = monthly["qualified"].groupby(
        [monthly.index.year, monthly.index.month]
    ).mean().unstack().reindex(columns=range(1, 13))
    table.columns.name = "month"
    table.index.name = "year"
    annual = table.mean(axis=1).where(table.notna().sum(axis=1) == 12).dropna()
    annual.name = "mean_temp"
    return annual, table


def estimate_trend(annual: pd.Series, maxlags: int = 3) -> dict:
    """Slope in °C/decade with conventional and HAC 95% intervals.

    HAC is a sensitivity analysis, not a remedy for station changes, biased
    missingness, non-linearity, or an invalid data-generating model.
    """
    if len(annual) < 15:
        raise ValueError("At least 15 eligible annual means are required for this exercise.")
    years = annual.index.to_numpy(dtype=float)
    values = annual.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Annual means must be finite.")
    design = np.column_stack([np.ones(len(years)), years - years.min()])
    intercept, slope = np.linalg.lstsq(design, values, rcond=None)[0]
    fitted = design @ np.array([intercept, slope])
    check = stats.linregress(years, values)
    if not np.isclose(slope, check.slope, atol=1e-10):
        raise AssertionError("Independent regression implementations disagree")
    tcrit = stats.t.ppf(0.975, df=len(years) - 2)
    classical = np.array([slope - tcrit * check.stderr,
                          slope + tcrit * check.stderr])
    hac = sm.OLS(values, design).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    robust = np.asarray(hac.conf_int(alpha=0.05))[1]
    return {
        "slope_c_decade": float(slope * 10),
        "conventional_ci_c_decade": (classical * 10).tolist(),
        "hac_ci_c_decade": (robust * 10).tolist(),
        "years": years, "fitted": fitted,
        "residual_lag1": float(pd.Series(values - fitted).autocorr(lag=1)),
    }
