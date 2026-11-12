# Data for the East African temperature investigation

**No NASA POWER or Meteostat real-data CSVs are committed to the public repository.**
The project deliberately separates a data source from the analysis code and
preserves data provenance.

- **Primary real source:** `uv run python tools/download_nasa_power.py --location dar_es_salaam`. Requests daily `T2M` two-metre air temperature for a *NASA POWER gridded reanalysis cell* for 1986–2025, rather than direct observations at a weather station. The script saves `data/private/nasa_power_dar_es_salaam_1986_2025.csv` plus JSON metadata. Check coverage, calendar dates, `-999` fill values, source history, and metadata before analysis or redistribution.
- **Secondary station comparison:** `uv run python tools/download_meteostat.py --station 63894`. The station archive is saved in `data/private/`, with Meteostat model-data substitution disabled. The previously inspected series lacks sufficiently complete years in the early decade for a full 1986–2025 comparison; missingness is the point of this optional activity.
- **Offline demonstration:** If no NASA POWER CSV is present, the main notebook uses a reproducible **synthetic**, deliberately artificial series from `tools/generate_synthetic_temperature.py`. Such outputs are not climate evidence. These synthetic values are offered under CC0 1.0. To save them locally, run `uv run python tools/generate_synthetic_temperature.py`.

Download files and partner-provided datasets must remain private unless their
reuse and distribution are explicitly permitted. For provenance and attribution
see [DATA_LICENSES.md](../DATA_LICENSES.md), the
[NASA POWER referencing guide](https://power.larc.nasa.gov/docs/referencing/),
and the [Meteostat developer license page](https://dev.meteostat.net/license).
