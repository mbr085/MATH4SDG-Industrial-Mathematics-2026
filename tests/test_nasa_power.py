# SPDX-License-Identifier: MIT
"""Offline tests for NASA POWER parsing and provenance rules."""
import unittest
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd

from tools.nasa_power import build_url, parse_daily_t2m
from tools.temperature_methods import annual_means, estimate_trend


class PowerTests(unittest.TestCase):
    def test_query_is_for_daily_utc_t2m_and_actual_coordinates(self):
        parsed = urlparse(build_url("dar_es_salaam", 1986, 2025))
        args = parse_qs(parsed.query)
        self.assertEqual(args["parameters"], ["T2M"])
        self.assertEqual(args["time-standard"], ["UTC"])
        self.assertEqual(args["latitude"], ["-6.7924"])
        self.assertEqual(args["start"], ["19860101"])
        self.assertEqual(args["end"], ["20251231"])

    def test_missing_sentinel_and_unreported_days(self):
        fake = {"header": {"fill_value": -999.0}, "properties": {
            "parameter": {"T2M": {"20200101": 26.0, "20200102": -999.0, "20201231": 26.1}}
        }}
        frame = parse_daily_t2m(fake, 2020, 2020)
        self.assertEqual(len(frame), 366)
        self.assertEqual(frame["temp"].notna().sum(), 2)
        self.assertTrue(np.isnan(frame.loc[1, "temp"]))
        self.assertEqual(str(frame.loc[0, "date"].date()), "2020-01-01")

    def test_invalid_payload_rejected(self):
        with self.assertRaises(ValueError):
            parse_daily_t2m({"error": "no weather here"}, 1986, 2025)
        with self.assertRaises(ValueError):
            build_url("dar_es_salaam", 1979, 2025)

    def test_complete_synthetic_response_allows_full_40_years(self):
        dates = pd.date_range("1986-01-01", "2025-12-31", freq="D")
        vals = {d.strftime("%Y%m%d"): float(24 + 0.03*(d.year-1986)) for d in dates}
        payload = {"properties": {"parameter": {"T2M": vals}}}
        daily = parse_daily_t2m(payload, 1986, 2025)
        annual, _ = annual_means(daily.set_index("date")["temp"])
        self.assertEqual(len(annual), 40)
        trend = estimate_trend(annual)
        self.assertAlmostEqual(trend["slope_c_decade"], 0.30, places=5)


if __name__ == "__main__":
    unittest.main()
