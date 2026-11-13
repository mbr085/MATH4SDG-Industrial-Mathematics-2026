# MATH4SDG — Industrial Mathematics Bootcamp and Workshop 2026

Python and computational teaching resources for the **University of Dar es Salaam (UDSM)** MATH4SDG industrial mathematics bootcamp (18–23 November 2026) and follow-up workshop (3–4 December 2026).

The bootcamp is principally **group work on industry-provided problems**. Facilitators circulate between groups; short morning demonstrations and end-of-day progress discussions support the investigations. Public backup projects (including East African temperature trends using NASA POWER and synthetic insurance-claims analysis) may be introduced if industry data are difficult to use.

## NixOS: Python, uv and JupyterLab

A Nix flake provides **Python 3.12** and **uv**. Python dependencies—including JupyterLab, NumPy, pandas, scikit-learn, statsmodels and Meteostat—are installed by uv into a project-local `.venv`. Do not separately install Python packages in the Nix shell.

From a NixOS machine with flakes enabled:

```sh
nix develop
uv sync
uv run jupyter lab
```

If you use Fish with **direnv and nix-direnv** already configured, entering the repository can load the Nix environment automatically:

```sh
direnv allow
uv sync
uv run jupyter lab
```

The `.envrc` file says `use flake`. The first Nix invocation may fetch packages; run setup while online **before** the bootcamp. Once the packages and datasets are present, the installed environment can be used without retrieving new data.

`UV_PYTHON` and `UV_PYTHON_DOWNLOADS=never` ensure that uv uses Nix's Python instead of a downloaded interpreter, which can fail on NixOS. Always use `uv run python` or `uv run jupyter lab` so code sees the dependencies in `.venv`.

### Dependency reproducibility

The committed `flake.lock` pins the same Nixpkgs revision used by [V26MAT102](https://github.com/mbr085/V26MAT102). The committed `uv.lock` pins the Python dependency set. Use `uv sync --locked` to restore it reproducibly.

For other operating systems, install Python 3.12 and uv independently, then use `uv sync` and `uv run jupyter lab` (the Nix flake is optional).

### KDE/Firefox browser launching on NixOS

The original flake exported a global `LD_LIBRARY_PATH` containing
`libstdc++.so.6`. That allowed compiled Python wheels such as NumPy to load,
but caused `xdg-open`/KDE to pick up an incompatible C++ runtime
(`GLIBCXX_3.4.35 not found`). Simply removing the library path repaired KDE
but caused NumPy and Jupyter's ZeroMQ extension to report that
`libstdc++.so.6` was missing. A first Python-only preload resolved that
dependency, but NumPy then reported `libz.so.1` as missing.

The development shell now injects a small Python `sitecustomize.py` module
through `PYTHONPATH`. At **Python process startup only**, it preloads Nix's
`libstdc++.so.6` and `libz.so.1` with
`ctypes.CDLL(..., mode=ctypes.RTLD_GLOBAL)`, allowing compiled Python
extensions to resolve these two dependencies. This does **not**
export `LD_LIBRARY_PATH` to Firefox, `xdg-open`, or KDE. The startup hook
is part of the flake and does not require changing the project-managed
`uv.lock`. It is a targeted workaround for Python wheels on NixOS; if
additional native libraries are missing, diagnose them separately.

After switching to this version of the flake, reload direnv. A **fresh terminal**
ensures there is no inherited global library override:

```sh
direnv reload
xdg-open https://www.python.org
uv run python -c 'import numpy, scipy, pandas, sklearn, statsmodels, zmq; print("Scientific Python OK")'
uv run jupyter lab
```

If Jupyter still does not open Firefox automatically, use the URL Jupyter
prints or run `env BROWSER=firefox uv run jupyter lab`.

**Note:** This mechanism uses Python's normal `sitecustomize` startup.
`python -S` or isolated Python startup modes which skip `PYTHONPATH`
do not load the helper. On non-NixOS hosts, the flake need not be used.


## Project data

**Do not commit confidential partner data to this public repository.** Dataset ownership, access conditions and publication permissions must be checked individually. In particular, making a dataset available for workshop analysis does not imply permission to publish it. Code is licensed [MIT](LICENSE); original teaching notes are [CC BY 4.0](LICENSE-CONTENT.md); datasets have [separate terms](DATA_LICENSES.md).

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
