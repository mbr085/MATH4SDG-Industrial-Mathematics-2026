# Primary backup investigation — NASA POWER East African temperature trends

**Question:** Has the estimated annual mean two-metre air temperature at the grid cell containing Dar es Salaam increased between 1986 and 2025, and how confident should we be?

**This is an optional student-led project**, used only when partner projects are unavailable or need a fallback. It is not an extra lecture day. Industry partners present problems on 18 November; group investigations take place principally from 19 November with morning tool demos and end-of-day progress summaries.

### Why NASA POWER?

The Meteostat record inspected by the instructor for Dar es Salaam (1986–2025) omitted roughly one-third of daily temperatures and offered **no sufficiently complete years in 1986–1995** under our monthly coverage rule. This makes the intended early-versus-late comparison impossible using that particular station series. **Do not fix this by forward-filling missing days or relaxing criteria to force an answer.**

NASA POWER provides gridded reanalysis estimates (from sources including MERRA-2) back to 1981. These are **not direct weather-station observations**. A gap-free time series does **not** guarantee scientific accuracy or independence from model choices. We compare with Meteostat only on overlapping observed dates; the comparison is not independent climate validation.

### Instructions

From the repository root (while **online before the workshop**):

```sh
uv sync --locked
uv run python tools/download_nasa_power.py --location dar_es_salaam
# Optional comparison grid cells:
uv run python tools/download_nasa_power.py --location dodoma
uv run python tools/download_nasa_power.py --location nairobi
uv run jupyter lab
```

Open `notebooks/east_africa_temperature_trends.ipynb`. The notebook looks for
`data/private/nasa_power_dar_es_salaam_1986_2025.csv`. If absent, it automatically runs with an **explicitly labeled synthetic dataset** for offline practice. Never report synthetic output as a real observation.

### Notebook conventions

The notebook follows a **step-by-step scientific Python style**. Technical input preparation (locating the CSV, choosing the synthetic fallback, checking duplicate dates and preparing the date index) now lives in `tools/temperature_data.py`, called with `load_temperature_data()`. The notebook still **prints the data-source and provenance messages** so synthetic data cannot be mistaken for NASA POWER reanalysis. Students see daily coverage, the 20-valid-days-per-month rule, the 12-month annual mean, the least-squares **design matrix and coefficients**, the conventional and HAC intervals, and nested-period sensitivity calculations **directly in Jupyter cells**. We retain the existing functions in `tools/temperature_methods.py` to independently check the outputs; they are **not** black boxes performing the notebook's main calculations. Figures identify whether the source is NASA POWER grid-cell reanalysis or **synthetic practice data**.

This means the revised notebook has more, shorter cells. The [pandas](../../reference/pandas_cheatsheet.ipynb) and [Matplotlib](../../reference/matplotlib_cheatsheet.ipynb) Jupyter cheat sheets are optional references, not compulsory extra exercises. Data are never silently imputed.

**Optional station-record exercise:** download `uv run python tools/download_meteostat.py --station 63894`, then open `notebooks/meteostat_station_missingness.ipynb`. It diagnoses station gaps and compares overlapping observed days with the NASA POWER reanalysis. It does not report a fictitious 40-year station trend.

For a quick test:
```sh
uv run python -m unittest discover -s tests -v
```

The NASA POWER download stores a daily CSV and provenance JSON inside Git-ignored `data/private/`. Check that it includes all years and no unexpected `-999` missing values **before** using the data. Exact dataset coverage has not yet been verified against a live API response in this repository.

### Deliverable

Each group produces a figure, precise estimand, trend estimate, uncertainty qualified by assumptions, completeness checks, explicit data provenance, limitations, and one question for TMA or another industry specialist. The team should distinguish **statistical uncertainty** from confidence in the data source and scientific interpretation.

Sources: [NASA POWER daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/), [meteorological source methodology](https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/), [referencing guide](https://power.larc.nasa.gov/docs/referencing/).
