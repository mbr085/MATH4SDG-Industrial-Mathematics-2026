# SPDX-License-Identifier: MIT
"""Download NASA POWER daily gridded temperature, 1986–2025 by default.

Run ONLINE before teaching:
    uv run python tools/download_nasa_power.py --location dar_es_salaam

The script stores CSV and provenance JSON under data/private/ (Git-ignored).
It does not generate station measurements, impute gaps, or publish datasets.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib import error, request
import time

try:
    from tools.nasa_power import LOCATIONS, build_url, parse_daily_t2m
except ModuleNotFoundError:
    # python tools/download_nasa_power.py from repository root.
    from nasa_power import LOCATIONS, build_url, parse_daily_t2m


def fetch_json(url: str, *, attempts: int = 3, timeout: int = 120) -> dict:
    """Retry temporary network failures; do not retry invalid requests."""
    for i in range(attempts):
        try:
            req = request.Request(url, headers={"User-Agent": "MATH4SDG-UDSM-teaching/2026"})
            with request.urlopen(req, timeout=timeout) as response:
                return json.load(response)
        except error.HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or i == attempts - 1:
                raise
        except (error.URLError, TimeoutError):
            if i == attempts - 1:
                raise
        time.sleep(2 ** i)
    raise RuntimeError("NASA POWER request failed after retries")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--location", choices=LOCATIONS, default="dar_es_salaam")
    parser.add_argument("--start", type=int, default=1986)
    parser.add_argument("--end", type=int, default=2025)
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing download")
    args = parser.parse_args()
    url = build_url(args.location, args.start, args.end)
    dest = Path(__file__).resolve().parents[1] / "data" / "private"
    output = dest / f"nasa_power_{args.location}_{args.start}_{args.end}.csv"
    if output.exists() and not args.overwrite:
        parser.error(f"{output} exists; use --overwrite to refresh")
    payload = fetch_json(url)
    daily = parse_daily_t2m(payload, args.start, args.end)
    dest.mkdir(parents=True, exist_ok=True)
    daily.to_csv(output, index=False)
    header = payload.get("header", {})
    provenance = {
        "source": "NASA Langley POWER daily T2M gridded reanalysis, NOT a weather station",
        "location": LOCATIONS[args.location],
        "time_standard": "UTC",
        "requested_years": [args.start, args.end],
        "query_url": url,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "api_header": header,
        "parameter_information": payload.get("parameters", {}),
        "record_count": len(daily),
        "nonmissing_days": int(daily["temp"].notna().sum()),
        "missing_days": int(daily["temp"].isna().sum()),
        "units_expected": "degrees Celsius (check API header/metadata)",
        "caveat": "These are model/reanalysis grid-cell estimates; not direct station observations or an independent validation of station climate trends.",
        "data_sources": "Typically MERRA-2 and/or GEOS-IT; inspect official POWER source history.",
    }
    output.with_suffix(".json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {output}: {provenance['nonmissing_days']} / {len(daily)} days with temperature")
    print("The data are GRIDDED REANALYSIS estimates, not weather-station measurements.")
    print("Inspect metadata and source history before publication or scientific claims.")


if __name__ == "__main__":
    main()
