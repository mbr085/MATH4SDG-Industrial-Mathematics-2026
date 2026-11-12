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


## Insurance fallback data (entirely synthetic)

The second backup project uses `tools/synthetic_insurance.py` to invent an
establishment-by-year insurance dataset (2021–2025), requiring no internet or
third-party information. The notebook calls the generator directly. A CSV copy
can be generated with:

```sh
uv run python tools/synthetic_insurance.py
```

The CSV, `data/synthetic_insurance_claims.csv`, is ignored by Git. It must
never be described as real Tanzanian insurance or worker compensation data.
Synthetic monetary amounts use arbitrary accounting units, **not TZS**, and
the generated values are offered under CC0 1.0. See
[insurance project documentation](../projects/insurance-claims/README.md).
