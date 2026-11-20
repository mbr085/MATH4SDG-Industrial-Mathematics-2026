# SPDX-License-Identifier: MIT
"""Integrity checks for entirely synthetic AI weather workshop material."""
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "exercises"
FEATURES = ["nearby_temp_c", "humidity_pct", "wind_speed_m_s"]
TARGET = "target_temp_c"


class SyntheticWeatherWorkshopTests(unittest.TestCase):
    def test_datasets_are_complete_and_chronologically_separate(self):
        development = pd.read_csv(DATA / "ai_weather_development.csv", parse_dates=["date"])
        final = pd.read_csv(DATA / "ai_weather_final.csv", parse_dates=["date"])

        self.assertEqual(len(development), 270)
        self.assertEqual(len(final), 60)
        self.assertEqual(development.columns.tolist(), ["date", *FEATURES, TARGET])
        self.assertEqual(final.columns.tolist(), ["date", *FEATURES, TARGET])
        self.assertTrue(development["date"].is_unique)
        self.assertTrue(final["date"].is_unique)
        self.assertTrue(development[FEATURES + [TARGET]].notna().all().all())
        self.assertTrue(final[FEATURES + [TARGET]].notna().all().all())

        ordered_development = development.sort_values("date")
        training = ordered_development.iloc[:210]
        validation = ordered_development.iloc[210:]
        self.assertLess(training["date"].max(), validation["date"].min())
        self.assertLess(development["date"].max(), final["date"].min())


if __name__ == "__main__":
    unittest.main()
