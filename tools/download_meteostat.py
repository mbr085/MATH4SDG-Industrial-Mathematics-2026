# SPDX-License-Identifier: MIT
"""Retrieve real Meteostat DAILY station series before teaching, while online.

Usage: uv run python tools/download_meteostat.py --station 63894
Defaults to 1986–2025. Downloads are PRIVATE and Git-ignored by design.
This script never invents or fills observations, and does not certify
homogeneity of the station record. Check original provider attributions.
"""
import argparse
from datetime import date, datetime, timezone
import json
from pathlib import Path

import pandas as pd

STATIONS = {
    "63894": "Dar es Salaam Airport, Tanzania",
    "63862": "Dodoma, Tanzania",
    "63740": "Nairobi, Kenya",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--station", default="63894")
    parser.add_argument("--start", type=int, default=1986)
    parser.add_argument("--end", type=int, default=2025)
    args = parser.parse_args()
    if args.start > args.end:
        parser.error("--start must not be after --end")
    import meteostat as ms

    ms.config.include_model_data = False  # explicitly no model-derived fills
    ms.config.block_large_requests = False
    start, end = date(args.start, 1, 1), date(args.end, 12, 31)
    series = ms.daily(ms.Station(id=args.station), start, end)
    raw = series.fetch()
    if raw.empty:
        raise RuntimeError("No data: inspect station inventory and provider coverage.")
    raw = raw.rename(columns=lambda c: str(getattr(c, "value", c)))
    raw.index = pd.to_datetime(raw.index)
    data = raw.sort_index().rename_axis("date").reset_index()
    if "temp" not in data:
        raise RuntimeError(f"Missing expected temperature column; got {list(data.columns)}")
    folder = Path(__file__).resolve().parents[1] / "data" / "private"
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / f"meteostat_{args.station}_{args.start}_{args.end}.csv"
    data.to_csv(out, index=False)
    meta = {
        "type": "Meteostat station data (not synthetic)",
        "station_id": args.station,
        "name_hint_verify": STATIONS.get(args.station, "Unknown: verify metadata"),
        "period_requested": [str(start), str(end)],
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "include_model_data": False,
        "rows_returned": len(data),
        "temperature_observations_nonmissing": int(data["temp"].notna().sum()),
        "columns": list(data.columns),
        "documentation": "https://dev.meteostat.net/python/api/meteostat.daily",
        "caveat": "Do not interpret station trend before checking time coverage, station history, and actual provider metadata; downloading does not grant publication permission.",
    }
    out.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Saved {out}, records={len(data)}, nonmissing temp={meta['temperature_observations_nonmissing']}")
    print("PRIVATE OBSERVATIONS: source and underlying-provider rights must be checked before sharing.")


if __name__ == "__main__":
    main()
