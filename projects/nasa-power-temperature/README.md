# Primary backup investigation — NASA POWER East African temperature trends

**Question:** Has the estimated annual mean two-metre air temperature at the grid cell containing Dar es Salaam increased between 1986 and 2025, and how confident should we be?

**This is an optional student-led project**, used only when partner projects are unavailable or need a fallback. It is not an extra lecture day. Under the draft programme, industry partners present problems on Thursday 19 November; group investigations take place principally on 21–23 November, with group presentations on Tuesday 24 November. Industry partners will provide datasets; this climate exercise remains optional.

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

The notebook uses short, visible pandas and NumPy calculations. Technical input preparation and source labelling remain in `tools/temperature_data.py`. **One check** ensures there is a finite temperature estimate for every calendar day of 1986–2025, including leap days; incomplete inputs are rejected rather than silently imputed. Annual means are then calculated **directly from daily estimates**, without intermediate monthly averaging or repeated coverage diagnostics. The regression design matrix, least-squares coefficients, conventional and HAC uncertainty intervals, and sensitivity to starting year remain visible in the student-facing cells.

The offline synthetic fallback now has **complete daily coverage** and deliberately includes seasonality, serial dependence and an artificial 2008 discontinuity. It is clearly labelled as **synthetic practice data, not climate evidence**. The pandas and Matplotlib Jupyter cheat sheets are optional references.

Missing station observations are handled by the separate Meteostat investigation; the older `tools/temperature_methods.annual_means` function remains available for that exercise, but is no longer used by the main NASA POWER notebook.

**Optional station-record exercise:** download `uv run python tools/download_meteostat.py --station 63894`, then open `notebooks/meteostat_station_missingness.ipynb`. It diagnoses station gaps and compares overlapping observed days with the NASA POWER reanalysis. It does not report a fictitious 40-year station trend.

For a quick test:
```sh
uv run python -m unittest discover -s tests -v
```

The NASA POWER download stores a daily CSV and provenance JSON inside Git-ignored `data/private/`. Check that it includes all years and no unexpected `-999` missing values **before** using the data. Exact dataset coverage has not yet been verified against a live API response in this repository.

### Deliverable

Each group produces a figure, precise estimand, trend estimate, uncertainty qualified by assumptions, completeness checks, explicit data provenance, limitations, and one question for TMA or another industry specialist. The team should distinguish **statistical uncertainty** from confidence in the data source and scientific interpretation.

Sources: [NASA POWER daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/), [meteorological source methodology](https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/), [referencing guide](https://power.larc.nasa.gov/docs/referencing/).
