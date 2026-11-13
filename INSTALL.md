# Student setup — Python, uv and JupyterLab

The workshop uses **Python 3.12**. You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and a copy of this repository. There is **no separate MATH4SDG package to install**: `pyproject.toml` and `uv.lock` already describe the scientific tools, and `uv sync --locked` installs them all into the project-local `.venv`.

## 1. Install uv and get the repository

Install [uv using its official instructions](https://docs.astral.sh/uv/getting-started/installation/) for your operating system. On a computer with Git, clone the public repository:

```sh
git clone https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026.git
cd MATH4SDG-Industrial-Mathematics-2026
```

Alternatively, download the repository as a ZIP from GitHub, extract it, and open a terminal in the extracted folder. **Git is convenient but not required to run the notebooks.**

## 2. Install the Python tools

With uv installed and a working Internet connection:

```sh
uv sync --locked
```

This creates/updates `.venv` and installs the versions already selected by `uv.lock`. The environment includes **JupyterLab, NumPy, pandas, Matplotlib, SciPy, scikit-learn, statsmodels, Meteostat, and ipykernel**, as well as their dependencies. The `.python-version` file asks uv for Python 3.12; on most systems uv can download the interpreter if it is not installed already. uv **does not install system Git**, and this is **not** a globally installed Python environment.

Start the notebook interface from the repository folder:

```sh
uv run jupyter lab
```

If the browser does not open automatically, follow the local URL printed in the terminal. The provided Jupyter notebooks are under `notebooks/` and `reference/`.

Try the fully synthetic, offline [insurance investigation](notebooks/synthetic_insurance_claims.ipynb) or the [pandas cheat sheet](reference/pandas_cheatsheet.ipynb) first. The [temperature investigation](notebooks/east_africa_temperature_trends.ipynb) uses a **local NASA POWER download if present**, otherwise an explicitly labelled synthetic substitute.

## 3. NixOS users

Use the repository's flake to provide **Python 3.12 and uv**, including the existing Python-only native-library workaround:

```sh
nix develop
uv sync --locked
uv run jupyter lab
```

If you already use Fish and direnv/nix-direnv, `direnv allow` can load the Nix environment on entering the repository. Do not set a global `LD_LIBRARY_PATH`; the flake deliberately avoids breaking Firefox/KDE. The Nix environment tells uv **not to download a different Python interpreter**.

## 4. Verify the setup

From the repository root:

```sh
uv run python -c "import numpy, pandas, matplotlib, scipy, sklearn, statsmodels, meteostat; print('Scientific tools OK')"
uv run python -m unittest discover -s tests -v
```

For a normal student investigation, there is no need to understand or install `tools/` as a separate package. The provided notebooks use the small `notebooks/bootstrap.py` helper where necessary, so notebooks under `notebooks/` can import the repository's scripts.

## Troubleshooting

- **`uv: command not found`**: complete the official uv installation and start a new terminal.
- **Python version error**: the project requires **Python 3.12**; make sure uv is allowed to install/select it, or enter `nix develop` on NixOS.
- **Network failure during `uv sync`**: complete setup while online. The workshop exercises themselves can be done offline after the environment is installed.
- **An import fails in JupyterLab**: start JupyterLab using `uv run jupyter lab` from the repository root and use the default kernel from this environment.
- **A dataset is missing**: the temperature notebook explicitly switches to synthetic data; this is **not evidence of climate**. Never confuse synthetic insurance records with real partner data.

For up-to-date uv usage, see the official [uv project guide](https://docs.astral.sh/uv/guides/projects/) and [uv sync documentation](https://docs.astral.sh/uv/reference/cli/#uv-sync).

**Data privacy:** Do not commit confidential partner data to this public repository or share it with external AI tools without permission.
