# Backup project: East African temperature trends

**Problem:** Is Dar es Salaam Airport warmer than forty years ago, and how confident should we be?

**Audience:** mixed undergraduate/MSc groups. **Status:** optional fallback for the industry bootcamp, **not** a prescribed lecture day or a substitute for a TMA project.

Start at the repository root:

```sh
uv sync --locked
uv run jupyter lab
```

Open `notebooks/east_africa_temperature_trends.ipynb`. It runs entirely offline with clearly identified **synthetic** data generated using `tools/generate_synthetic_temperature.py`. Synthetic results are NOT climate evidence.

To use **real observations**, before the bootcamp while connected:

```sh
uv run python tools/download_meteostat.py --station 63894
# Optional comparison (check inventory and source history):
uv run python tools/download_meteostat.py --station 63862
```

The download script writes the observational CSV and provenance JSON under `data/private/`, ignored by Git. It disables Meteostat model-derived values, does not impute gaps, and intentionally does not publish raw data. Before attributing warming to anything, check station history, coverage, data provider, and possible site/instrument changes with TMA when available.

**Minimal deliverable:** a plotted series, clear estimand, numerical estimate **if evidence permits**, uncertainty under stated assumptions, coverage checks, limitations, and one follow-up question. A justified “we cannot tell reliably from these data” is a valid result.

**Challenge:** Extend to Dodoma or Nairobi; contrast the conventional interval and the HAC sensitivity analysis; compare seasonality-adjusted monthly fitting and annual summaries.

Read [facilitator notes](FACILITATOR_NOTES.md), [dataset terms](../../DATA_LICENSES.md), and the [MAT102 antecedents](https://github.com/mbr085/V26MAT102).
