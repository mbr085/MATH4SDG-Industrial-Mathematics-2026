# Secondary investigation: Meteostat station observation gaps

The original Meteostat backup was **not viable as the primary 40-year
temperature-trend project**: the Dar es Salaam Airport daily series inspected
by the instructor for 1986–2025 had too many gaps, especially in the early
years. Our completeness criterion gave no eligible years in 1986–1995,
preventing the intended early/late comparison.

This problem is scientifically useful and should be studied **as a missingness
case**, not concealed by forward-filling or changing criteria to force a trend.

**Primary temperature project:** [NASA POWER reanalysis](../nasa-power-temperature/README.md)
provides a longer, more complete **gridded model-derived temperature estimate**
for the Dar es Salaam location. These are **not** direct station observations.

### Optional hands-on exercise

```sh
uv sync --locked
uv run python tools/download_meteostat.py --station 63894
uv run jupyter lab
```

Open `notebooks/meteostat_station_missingness.ipynb`. It examines station
coverage and, if the NASA POWER data are also downloaded, compares the sources
only where station observations exist. It does not invent temperature readings
for the missing early years.

The station CSV and provenance JSON go to `data/private/` (Git-ignored).
No restricted industry data or unpublished observations should be committed.
See [facilitator guidance](FACILITATOR_NOTES.md),
[data terms](../../DATA_LICENSES.md), and the
[MAT102 antecedents](https://github.com/mbr085/V26MAT102).
