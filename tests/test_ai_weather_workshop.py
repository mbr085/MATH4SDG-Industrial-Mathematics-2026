# SPDX-License-Identifier: MIT
"""Independent checks for the wholly synthetic two-station weather exercise."""

import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "exercises"
OBSERVED = ["station_a_temp_c", "station_b_temp_c"]


class TwoStationWorkshopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dev = pd.read_csv(DATA / "ai_weather_development.csv", parse_dates=["date"])
        cls.validation = pd.read_csv(
            DATA / "ai_weather_validation_answers.csv", parse_dates=["date"]
        )
        cls.final = pd.read_csv(DATA / "ai_weather_final.csv", parse_dates=["date"])

    def test_distinct_chronological_periods_and_incomplete_measurements(self):
        self.assertEqual(len(self.dev), 270)
        self.assertEqual(len(self.final), 60)
        self.assertEqual(
            self.dev.columns.tolist(),
            ["date", *OBSERVED, "humidity_pct", "wind_speed_m_s"],
        )
        self.assertEqual(
            self.final.columns.tolist(),
            ["date", *OBSERVED, "humidity_pct", "wind_speed_m_s", "masked_a_c", "masked_b_c"],
        )
        for frame in (self.dev, self.final):
            self.assertTrue(frame["date"].is_monotonic_increasing)
            self.assertTrue(frame["date"].is_unique)
            self.assertTrue(frame[["humidity_pct", "wind_speed_m_s"]].notna().all().all())
            self.assertGreater(int(frame[OBSERVED].isna().all(axis=1).sum()), 0)
            self.assertGreater(int(frame[OBSERVED[0]].notna().sum()), 0)
            self.assertGreater(int(frame[OBSERVED[1]].notna().sum()), 0)
        self.assertLess(self.dev["date"].max(), self.final["date"].min())
        self.assertLess(self.dev.iloc[209]["date"], self.dev.iloc[210]["date"])

    def test_validation_labels_are_not_visible_as_observations(self):
        self.assertGreaterEqual(len(self.validation), 30)
        self.assertEqual(
            self.validation.columns.tolist(), ["date", "station_code", "truth_temp_c"]
        )
        self.assertFalse(self.validation.duplicated(["date", "station_code"]).any())
        self.assertTrue(self.validation.station_code.isin([0, 1]).all())
        dates = self.dev.set_index("date")
        for row in self.validation.itertuples(index=False):
            self.assertGreater(row.date, self.dev.iloc[209].date)
            self.assertTrue(pd.isna(dates.loc[row.date, OBSERVED[row.station_code]]))
            self.assertTrue(np.isfinite(row.truth_temp_c))

    def test_final_masks_have_no_public_unmasked_targets(self):
        masked = [("station_a_temp_c", "masked_a_c"), ("station_b_temp_c", "masked_b_c")]
        self.assertGreaterEqual(int(self.final[[col for _, col in masked]].notna().sum().sum()), 30)
        for observed, hidden in masked:
            self.assertTrue(self.final.loc[self.final[hidden].notna(), observed].isna().all())
        self.assertTrue(self.final["masked_a_c"].notna().any())
        self.assertTrue(self.final["masked_b_c"].notna().any())

    def test_prepared_history_never_looks_ahead(self):
        notebook = json.loads(
            (ROOT / "notebooks" / "ai_assisted_weather_modelling.ipynb").read_text()
        )
        source = "".join(notebook["cells"][6]["source"])
        env = {"pd": pd, "development": self.dev, "display": lambda *_: None}
        exec(source, env)
        cases = env["make_cases"](self.dev)
        for t in [0, 1, 2, 15, 60, 209, 210, 225, 269]:
            day = self.dev.iloc[t]
            past = self.dev.iloc[:t]
            for station in (0, 1):
                case = cases.loc[
                    (cases["date"] == day.date) & (cases["station_code"] == station)
                ].iloc[0]
                own, other = OBSERVED[station], OBSERVED[1 - station]
                recent = past[own].dropna()
                if len(recent):
                    self.assertAlmostEqual(case["own_last_c"], recent.iloc[-1])
                else:
                    self.assertTrue(pd.isna(case["own_last_c"]))
                if pd.notna(day[other]):
                    self.assertAlmostEqual(case["other_today_c"], day[other])
                else:
                    self.assertTrue(pd.isna(case["other_today_c"]))


if __name__ == "__main__":
    unittest.main()
