# SPDX-License-Identifier: MIT
"""Offline tests: no download or climate claims are involved."""
import unittest

import numpy as np
import pandas as pd

from tools.generate_synthetic_temperature import generate
from tools.temperature_methods import annual_means, estimate_trend


class BackupTests(unittest.TestCase):
    def test_synthetic_is_reproducible_and_has_gaps(self):
        a, b = generate(), generate()
        pd.testing.assert_frame_equal(a, b)
        self.assertGreater(a["temp"].isna().sum(), 0)
        self.assertEqual(str(a["date"].iloc[0].date()), "1986-01-01")
        self.assertEqual(str(a["date"].iloc[-1].date()), "2025-12-31")

    def test_incomplete_month_causes_year_exclusion(self):
        dates = pd.date_range("2000-01-01", "2002-12-31", freq="D")
        values = pd.Series(25.0, index=dates)
        values.loc["2001-04-01":"2001-04-25"] = np.nan
        years, table = annual_means(values)
        self.assertEqual(years.index.to_list(), [2000, 2002])
        self.assertTrue(pd.isna(table.loc[2001, 4]))

    def test_exact_linear_trend(self):
        years = np.arange(1986, 2026)
        annual = pd.Series(24.0 + 0.04 * (years - 1986), index=years)
        result = estimate_trend(annual)
        self.assertAlmostEqual(result["slope_c_decade"], 0.4, places=10)

    def test_synthetic_yields_usable_years(self):
        frame = generate().set_index("date")
        annual, table = annual_means(frame["temp"])
        self.assertGreaterEqual(len(annual), 15)
        self.assertLess(len(annual), len(table))
        estimate_trend(annual)


if __name__ == "__main__":
    unittest.main()
