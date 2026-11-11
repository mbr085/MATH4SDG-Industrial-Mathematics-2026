# MATH4SDG — Industrial Mathematics Bootcamp and Workshop 2026

Python and computational teaching resources for the **University of Dar es Salaam (UDSM)** MATH4SDG industrial mathematics bootcamp (18–23 November 2026) and follow-up workshop (3–4 December 2026).

The bootcamp is principally **group work on industry-provided problems**. Facilitators circulate between groups; short morning demonstrations and end-of-day progress discussions support the investigations. Public backup projects (including East African temperature trends using Meteostat) may be introduced if industry data are difficult to use.

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

The committed `flake.lock` pins the same Nixpkgs revision used by [V26MAT102](https://github.com/mbr085/V26MAT102). The committed `uv.lock` pins Python dependencies. Run `uv sync --locked` to prevent accidental lockfile changes.

For other operating systems, install Python 3.12 and uv independently, then use `uv sync` and `uv run jupyter lab` (the Nix flake is optional).

## Project data

**Do not commit confidential partner data to this public repository.** Dataset ownership, access conditions and publication permissions must be checked individually. In particular, making a dataset available for workshop analysis does not imply permission to publish it. Code is licensed [MIT](LICENSE); original teaching notes are [CC BY 4.0](LICENSE-CONTENT.md); datasets have [separate terms](DATA_LICENSES.md).

## Optional backup project: East African temperature trends

This repository now includes a **student-directed backup investigation**:
[Is Dar es Salaam warmer than forty years ago?](projects/meteostat-temperature/README.md).
It is **not** a scheduled series of lectures. It supports partner-led problem
work when real industry datasets are delayed or too complex for inexperienced
groups. Morning tool demonstrations and end-of-day plenaries can draw on it.

The project adapts ideas from
[MAT102 weather-data and regression notebooks](https://github.com/mbr085/V26MAT102),
but uses **synthetic temperatures by default** and stresses missingness,
seasonality, serial dependence, and scientific limitations.

```sh
uv sync --locked
uv run jupyter lab
```

Open [the student notebook](notebooks/east_africa_temperature_trends.ipynb)
from JupyterLab. It runs **offline**, generating deterministic artificial data
in memory. Results in synthetic mode must not be reported as observations
of Tanzania's climate.

To download optional real Meteostat station data **while online**, before the
event:

```sh
uv run python tools/download_meteostat.py --station 63894
uv run python tools/download_meteostat.py --station 63862
```

The actual observations and metadata are saved under ignored `data/private/`;
the notebook automatically uses the Dar es Salaam download if available.
It does not fill missing observations or assert that the record is homogeneous.
Confirm provenance, inventory, station history and provider licenses before
sharing data or drawing scientific conclusions.

For an offline smoke test:

```sh
uv run python -m unittest discover -s tests -v
```

See [the facilitator notes](projects/meteostat-temperature/FACILITATOR_NOTES.md)
and [data policy](DATA_POLICY.md).
