# SPDX-License-Identifier: MIT
"""Load and validate the temperature exercise data without notebook plumbing.

This is only input preparation; scientific calculations remain in the notebook.
NASA POWER estimates and artificial fallback data are never conflated.
"""
from pathlib import Path

import pandas as pd

from tools.generate_synthetic_temperature import generate


DEFAULT_POWER_CSV = (
    Path(__file__).resolve().parents[1]
    / "data/private/nasa_power_dar_es_salaam_1986_2025.csv"
)


def load_temperature_data(
    power_csv: Path | None = None,
) -> tuple[pd.DataFrame, str, str, str]:
    """Return (daily table, source statement, short plot label, provenance).

    If the NASA POWER CSV exists, its values are gridded reanalysis estimates,
    NOT direct weather-station observations. Otherwise generate a completely
    synthetic practice dataset. Missing temperatures are not imputed.

    `power_csv` allows offline tests to supply a temporary input file.
    """
    csv_path = DEFAULT_POWER_CSV if power_csv is None else Path(power_csv)

    if csv_path.exists():
        data = pd.read_csv(csv_path, parse_dates=["date"])
        source = (
            "NASA POWER T2M — GRIDDED REANALYSIS ESTIMATES "
            "(NOT STATION OBSERVATIONS)"
        )
        figure_source = "NASA POWER GRID-CELL ESTIMATE"
        metadata_file = csv_path.with_suffix(".json")
        provenance = (
            f"Provenance JSON: {metadata_file}"
            if metadata_file.exists()
            else "Provenance JSON: MISSING — re-download recommended"
        )
    else:
        data = generate()
        source = "SYNTHETIC DATA ONLY — NOT EVIDENCE ABOUT CLIMATE"
        figure_source = "SYNTHETIC — NOT CLIMATE EVIDENCE"
        provenance = (
            "No external data or provenance file needed: synthetic practice only."
        )

    data = data.sort_values("date").copy()
    if data["date"].duplicated().any():
        raise ValueError("Duplicate dates: verify the source before proceeding.")

    data["temp"] = pd.to_numeric(data["temp"], errors="coerce")
    data = data.set_index("date").loc["1986":"2025"]
    if data.empty:
        raise ValueError("No data in the requested 1986–2025 period.")

    return data, source, figure_source, provenance
