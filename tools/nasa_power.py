# SPDX-License-Identifier: MIT
"""Parse NASA POWER daily gridded 2-metre air temperature (T2M).

The output is a reanalysis estimate for a spatial grid cell, NOT a direct
weather-station observation. No missing values are silently imputed.
"""
from datetime import date
from urllib.parse import urlencode

import numpy as np
import pandas as pd

ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"
LOCATIONS = {
    # Approximate city centres, not station/airport coordinates.
    "dar_es_salaam": {"name": "Dar es Salaam", "latitude": -6.7924, "longitude": 39.2083},
    "dodoma": {"name": "Dodoma", "latitude": -6.1560, "longitude": 35.7503},
    "nairobi": {"name": "Nairobi", "latitude": -1.2864, "longitude": 36.8172},
}


def build_url(location: str, start_year: int = 1986, end_year: int = 2025) -> str:
    if location not in LOCATIONS:
        raise ValueError(f"Unknown location {location!r}; choose {list(LOCATIONS)}")
    if start_year < 1981 or end_year < start_year:
        raise ValueError("NASA POWER daily T2M starts in 1981 and end must follow start")
    point = LOCATIONS[location]
    params = {
        "parameters": "T2M", "community": "RE",
        "latitude": point["latitude"], "longitude": point["longitude"],
        "start": f"{start_year}0101", "end": f"{end_year}1231",
        "format": "JSON", "time-standard": "UTC",
    }
    return ENDPOINT + "?" + urlencode(params)


def parse_daily_t2m(payload: dict, start_year: int, end_year: int) -> pd.DataFrame:
    """Return every requested calendar day with date, temp; -999 becomes NA.

    Reject obviously incompatible JSON, duplicate keys are impossible in a
    decoded dictionary, and retain all original gaps for completeness checks.
    """
    try:
        observations = payload["properties"]["parameter"]["T2M"]
    except (KeyError, TypeError) as exc:
        raise ValueError("POWER payload missing properties.parameter.T2M") from exc
    if not isinstance(observations, dict) or not observations:
        raise ValueError("POWER did not return a daily T2M dictionary")
    try:
        index = pd.to_datetime(list(observations), format="%Y%m%d", errors="raise")
        values = pd.to_numeric(pd.Series(list(observations.values()), index=index), errors="coerce")
    except (TypeError, ValueError) as exc:
        raise ValueError("POWER T2M dates or values are malformed") from exc
    if index.has_duplicates:
        raise ValueError("Duplicated date in POWER T2M response")
    fill_value = payload.get("header", {}).get("fill_value", -999)
    values = values.replace([float(fill_value), -999.0], np.nan)
    values = values.mask(~np.isfinite(values))
    expected = pd.date_range(date(start_year, 1, 1), date(end_year, 12, 31), freq="D")
    if values.index.min() < expected.min() or values.index.max() > expected.max():
        raise ValueError("POWER response contains dates outside requested period")
    daily = values.reindex(expected)
    if daily.notna().sum() == 0:
        raise ValueError("POWER temperature series contains no finite values")
    return pd.DataFrame({"date": daily.index, "temp": daily.to_numpy(dtype=float)})
