# MATH4SDG — Industrial Mathematics Bootcamp and Workshop 2026

Python and computational teaching resources for the **University of Dar es Salaam (UDSM)** MATH4SDG industrial mathematics bootcamp (18–23 November 2026) and follow-up workshop (3–4 December 2026).

The bootcamp is principally **group work on industry-provided problems**. Facilitators circulate between groups; short morning demonstrations and end-of-day progress discussions support the investigations. Public backup projects (including East African temperature trends using NASA POWER and synthetic insurance-claims analysis) may be introduced if industry data are difficult to use.

## Getting started — Windows and macOS

Students need **uv**, an Internet connection for the initial installation, and a copy of this repository. **No separate workshop Python package is required.** The `uv.lock` file contains the resolved dependencies for the workshop, including JupyterLab, pandas, NumPy, Matplotlib, SciPy, scikit-learn, statsmodels and Meteostat.

### Windows (PowerShell)

Open **PowerShell** and install uv using Windows Package Manager:

```powershell
winget install --id=astral-sh.uv -e
```

If WinGet is unavailable, use the [official Windows installer](https://docs.astral.sh/uv/getting-started/installation/):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS (Terminal)

Open **Terminal** and install uv using its [official installer](https://docs.astral.sh/uv/getting-started/installation/):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you already use Homebrew, `brew install uv` is an alternative.

### Download the workshop and start JupyterLab

After installing uv, **open a new terminal**, verify `uv --version`, and clone the repository (or download the ZIP from GitHub and open a terminal in its extracted folder):

```sh
git clone https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026.git
cd MATH4SDG-Industrial-Mathematics-2026
uv sync --locked
uv run jupyter lab
```

The same last two commands work in PowerShell and macOS Terminal. uv automatically sets up a project-local `.venv` with the required **Python 3.12** and the locked dependencies. Use `uv run jupyter lab` rather than installing JupyterLab globally. If Git is not installed, the GitHub **Code → Download ZIP** option works as well.

See the [full student installation guide](INSTALL.md) for more detail, verification and troubleshooting. Complete the initial installation **while online**, before the workshop.

## Project data

**Do not commit confidential partner data to this public repository.** Dataset ownership, access conditions and publication permissions must be checked individually. In particular, making a dataset available for workshop analysis does not imply permission to publish it. Code is licensed [MIT](LICENSE); original teaching notes are [CC BY 4.0](LICENSE-CONTENT.md); datasets have [separate terms](DATA_LICENSES.md).

## Student quick references

These short **executable Jupyter notebooks** support students who are learning Python while investigating mathematical questions. They are **not additional compulsory lessons**. Each starts with a small, wholly invented dataset so students can run and edit examples without downloading data or executing another notebook; each also links to official documentation and suggests focused AI questions that students can independently verify.

- [pandas Jupyter cheat sheet](reference/pandas_cheatsheet.ipynb) — inspect tables, select data, handle missing values, group by sector, calculate exposure-adjusted rates, and summarize time series.
- [Matplotlib Jupyter cheat sheet](reference/matplotlib_cheatsheet.ipynb) — make labelled plots using explicit `Axes` objects, compare model outputs with observations, and choose plots that communicate units and data provenance.

The two optional backup notebooks link directly to both references. In JupyterLab, open the `.ipynb` file, run its setup cell, and then run examples as needed. Do not share restricted industry data with external AI services.

## Optional backup project: East African temperature trends

This repository now includes a **student-directed backup investigation**:
[Is Dar es Salaam warmer than forty years ago?](projects/nasa-power-temperature/README.md).
It is **not** a scheduled series of lectures. It supports partner-led problem
work when real industry datasets are delayed or too complex for inexperienced
groups. Morning tool demonstrations and end-of-day plenaries can draw on it.

The project adapts ideas from
[MAT102 weather-data and regression notebooks](https://github.com/mbr085/V26MAT102),
with NASA POWER gridded reanalysis as the primary real-data source and **explicitly labeled synthetic temperatures** as an offline fallback. It stresses source provenance, seasonality, serial dependence, missing observations, and scientific limitations. NASA POWER is a model-informed gridded product, **not** a weather-station record.

```sh
uv sync --locked
uv run jupyter lab
```

Open [the student notebook](notebooks/east_africa_temperature_trends.ipynb)
from JupyterLab. It runs **offline**, generating deterministic artificial data
in memory. Results in synthetic mode must not be reported as observations
of Tanzania's climate.

To download the primary real NASA POWER grid-cell estimates **while online**, before the event:

```sh
uv run python tools/download_nasa_power.py --location dar_es_salaam
# Optional comparison location:
uv run python tools/download_nasa_power.py --location dodoma
```

The NASA POWER grid-cell data and download metadata are stored under ignored `data/private/`; the main notebook uses the Dar es Salaam POWER download if available. It does not fill missing values or assert that the reanalysis history is homogeneous or independently observed. An instructor-run NASA POWER download produced full daily coverage for 1986–2025; inspect coverage and metadata again when retrieving the data locally. Check coverage, methodology and provenance before drawing scientific conclusions.

The temperature notebook has been revised to make **monthly completeness, annual aggregation, least-squares fitting and uncertainty calculations visible in short executable cells**, with explicitly labelled source-specific plots. The original helper functions remain for independent checking. The pandas and Matplotlib Jupyter cheat sheets linked near the top provide optional command references.

The original Meteostat station series was found to lack sufficient early observations for the intended 40-year comparison. We retain it **only as a secondary investigation of observational gaps**. For that optional exercise:

```sh
uv run python tools/download_meteostat.py --station 63894
```

Open [the station-missingness notebook](notebooks/meteostat_station_missingness.ipynb) and read the [station guidance](projects/meteostat-temperature/README.md).

For an offline smoke test:

```sh
uv run python -m unittest discover -s tests -v
```

See [the NASA POWER facilitator notes](projects/nasa-power-temperature/FACILITATOR_NOTES.md)
and [data policy](DATA_POLICY.md).


## Optional short optimization challenge

For groups wishing to explore a **non-statistical** industrial mathematics problem, see [Who should do which job?](projects/assignment-optimization/README.md). This is a single, wholly fictional worker–job assignment problem. Groups can formulate binary assignment variables and minimize total worker-hours; an optional `scipy.optimize.linear_sum_assignment` example allows them to verify a solution. The problem is short and open-ended, not a third substantial notebook or a compulsory lesson, and needs **no additional dependencies or external data**.

## Optional backup project: Synthetic workplace insurance claims

A second, complementary [student-led insurance investigation](projects/insurance-claims/README.md) works **completely offline** and requires no industry records. All establishment identifiers, sectors, zones, claim counts, and cost values are **invented** and are not statistics from WCF, TIRA, an insurer, or Tanzania.

The notebook asks how to estimate *expected claim counts* while accounting for exposure measured in worker-years. Students compare a transparent baseline with an exposure-weighted Poisson regression, train on 2021–2024 and evaluate on a held-out 2025, and discuss limitations of a fitted model.

```sh
uv sync --locked
uv run jupyter lab
```

Open [the student notebook](notebooks/synthetic_insurance_claims.ipynb). No download is needed; the notebook generates deterministic synthetic data in memory. See [facilitator guidance](projects/insurance-claims/FACILITATOR_NOTES.md). Run the [offline tests](tests/test_insurance_backup.py) with the existing `unittest` command above.

The artificial records may be regenerated as a **local ignored CSV** using `uv run python tools/synthetic_insurance.py`. These classroom values have no real-world insurance interpretation; they are offered under CC0 1.0 and are documented in [DATA_LICENSES.md](DATA_LICENSES.md).

### Insurance notebook presentation and editor setup

For the [synthetic insurance claims notebook](notebooks/synthetic_insurance_claims.ipynb), introductory calculations are broken into understandable pandas steps with a single conceptual purpose per cell; plots use explicit Matplotlib `Axes` methods. The notebook directly constructs the one-hot encoder, Poisson regression pipeline and exposure-weighted fit, then calls `mean_poisson_deviance` without a scoring wrapper. It evaluates predictions against 2025 and separately forecasts expected claims for a hypothetical 2026 scenario, with no 2026 outcomes supplied.

The notebook imports `bootstrap` from [notebooks/bootstrap.py](notebooks/bootstrap.py) to connect to the existing `tools` modules. Start JupyterLab from the project root and keep the supplied notebook inside the `notebooks/` directory. No local project package installation is required for now. The `[tool.pyright]` section in `pyproject.toml` points Neovim/Pyright at the uv-managed `.venv`.
