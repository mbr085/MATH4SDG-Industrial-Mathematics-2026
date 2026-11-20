# SPDX-License-Identifier: MIT
"""Independent checks for the wholly synthetic two-station weather exercise."""

import json
import ast
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

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
        self.assertTrue(self.dev.loc[0, OBSERVED].notna().all())
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
        source_complete = "".join(notebook["cells"][6]["source"])
        source_cases = "".join(notebook["cells"][8]["source"])
        env = {"pd": pd, "np": np, "development": self.dev, "display": lambda *_: None}
        exec(source_complete, env)
        exec(source_cases, env)
        make_cases = env["make_cases"]
        cases = make_cases(self.dev)

        for t in [0, 1, 2, 15, 60, 209, 210, 225, 269]:
            day = self.dev.iloc[t]
            past = self.dev.iloc[:t]
            completed_a = past[OBSERVED[0]].fillna(past[OBSERVED[1]]).ffill()
            completed_b = past[OBSERVED[1]].fillna(past[OBSERVED[0]]).ffill()
            last_completed = [
                completed_a.iloc[-1] if len(completed_a) else np.nan,
                completed_b.iloc[-1] if len(completed_b) else np.nan,
            ]
            for station in (0, 1):
                case = cases.loc[
                    (cases["date"] == day.date) & (cases["station_code"] == station)
                ].iloc[0]
                other = OBSERVED[1 - station]
                expected_yesterday = last_completed[station]
                expected_other_yesterday = last_completed[1 - station]
                for actual, expected in (
                    (case["own_yesterday_c"], expected_yesterday),
                    (case["other_yesterday_c"], expected_other_yesterday),
                    (case["other_today_c"], day[other]),
                ):
                    if pd.isna(expected):
                        self.assertTrue(pd.isna(actual))
                    else:
                        self.assertAlmostEqual(actual, expected)

            # Appending future data may not change features of an earlier day.
            prefix_cases = make_cases(self.dev.iloc[: t + 1])
            earlier_rows = cases.loc[cases["date"] <= day.date].reset_index(drop=True)
            pd.testing.assert_frame_equal(prefix_cases, earlier_rows)

    def test_previous_day_can_itself_be_an_estimate(self):
        notebook = json.loads(
            (ROOT / "notebooks" / "ai_assisted_weather_modelling.ipynb").read_text()
        )
        source_complete = "".join(notebook["cells"][6]["source"])
        source_cases = "".join(notebook["cells"][8]["source"])
        toy = pd.DataFrame({
            "date": pd.date_range("2025-01-01", periods=6),
            "station_a_temp_c": [10.0, np.nan, np.nan, np.nan, 15.0, np.nan],
            "station_b_temp_c": [20.0, 24.0, np.nan, np.nan, np.nan, np.nan],
            "humidity_pct": [70.0] * 6,
            "wind_speed_m_s": [2.0] * 6,
        })
        env = {"pd": pd, "np": np, "development": toy, "display": lambda *_: None}
        exec(source_complete, env)
        exec(source_cases, env)
        cases = env["make_cases"](toy)
        def yesterday(day_idx, station):
            return cases.loc[
                (cases["date"] == toy.iloc[day_idx].date)
                & (cases["station_code"] == station), "own_yesterday_c"
            ].iloc[0]

        # Day 2: station A is estimated at 24 from same-day observed B.
        # Days 3-4: both temperatures are missing; carry forward that estimate.
        self.assertAlmostEqual(yesterday(2, 0), 24.0)
        self.assertAlmostEqual(yesterday(3, 0), 24.0)
        self.assertAlmostEqual(yesterday(3, 1), 24.0)
        # Day 5: observed A=15 provides a B estimate of 15, passed to day 6.
        self.assertAlmostEqual(yesterday(5, 1), 15.0)


    def test_score_restricts_training_dates_and_supplies_one_case(self):
        # Extract the real student's scoring function from the notebook.
        notebook = json.loads(
            (ROOT / "notebooks" / "ai_assisted_weather_modelling.ipynb").read_text()
        )
        code = "".join(notebook["cells"][10]["source"])
        tree = ast.parse(code)
        func = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "score"
        )
        namespace = {
            "np": np,
            "pd": pd,
            "mean_absolute_error": mean_absolute_error,
            "FEATURES": [
                "station_code", "other_today_c", "own_yesterday_c",
                "other_yesterday_c", "humidity_pct", "wind_speed_m_s",
                "day_of_year",
            ],
        }
        module = ast.fix_missing_locations(ast.Module(body=[func], type_ignores=[]))
        exec(compile(module, "workshop_score", "exec"), namespace)
        score = namespace["score"]

        train = pd.DataFrame({
            "date": pd.to_datetime(["2025-01-01", "2025-01-03", "2025-01-04", "2025-01-10"]),
            "target_temp_c": [10.0, 70.0, 40.0, 100.0],
        })
        cases = pd.DataFrame({
            "date": pd.to_datetime(["2025-01-03", "2025-01-09"]),
            "station_code": [0, 1],
            "other_today_c": [25.0, np.nan],
            "own_yesterday_c": [24.0, 28.0],
            "other_yesterday_c": [27.0, 25.0],
            "humidity_pct": [70.0, 75.0],
            "wind_speed_m_s": [1.0, 2.0],
            "day_of_year": [3, 9],
            "truth_temp_c": [10.0, 40.0],
        })

        calls = []
        def predictor(past, today):
            expected_date = cases.iloc[len(calls)]["date"]
            self.assertEqual(len(today), 1)
            self.assertEqual(today.columns.tolist(), namespace["FEATURES"])
            self.assertTrue((past["date"] < expected_date).all())
            self.assertEqual(past["date"].tolist(), train.loc[train.date < expected_date, "date"].tolist())
            calls.append(expected_date)
            return np.array([past["target_temp_c"].mean()])

        result = score(predictor, train, cases)
        self.assertAlmostEqual(result, 0.0)
        self.assertEqual(len(calls), 2)

        # Same-day and later training rows cannot change the earlier estimate.
        changed = train.copy()
        changed.loc[changed.date >= pd.Timestamp("2025-01-03"), "target_temp_c"] = 70000.0
        first_case = cases.iloc[[0]]
        def use_mean(past, today):
            return np.array([past["target_temp_c"].mean()])
        self.assertEqual(score(use_mean, train, first_case), score(use_mean, changed, first_case))

    def test_score_rejects_a_function_that_returns_multiple_predictions(self):
        notebook = json.loads((ROOT / "notebooks" / "ai_assisted_weather_modelling.ipynb").read_text())
        source = "".join(notebook["cells"][10]["source"])
        tree = ast.parse(source)
        func = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "score")
        context = {
            "np": np,
            "mean_absolute_error": mean_absolute_error,
            "FEATURES": ["station_code", "other_today_c", "own_yesterday_c", "other_yesterday_c", "humidity_pct", "wind_speed_m_s", "day_of_year"],
        }
        exec(compile(ast.fix_missing_locations(ast.Module(body=[func], type_ignores=[])), "score", "exec"), context)
        rows = pd.DataFrame({"date": [pd.Timestamp("2025-01-03")], "truth_temp_c": [25.0], **{c: [1.0] for c in context["FEATURES"]}})
        training = pd.DataFrame({"date": [pd.Timestamp("2025-01-01")], "target_temp_c": [23.0]})
        with self.assertRaisesRegex(ValueError, "one finite temperature prediction"):
            context["score"](lambda past, today: [1, 2], training, rows)


if __name__ == "__main__":
    unittest.main()
