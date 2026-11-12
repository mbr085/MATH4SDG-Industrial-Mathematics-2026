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

The committed `flake.lock` pins the same Nixpkgs revision used by [V26MAT102](https://github.com/mbr085/V26MAT102). The first `uv sync` will generate a `uv.lock` using the Python dependency requirements in `pyproject.toml`. **Commit that generated `uv.lock`** to freeze exact Python package versions for participants. A `uv.lock` is not included in this initial setup because dependency resolution could not be run in the authoring environment.

For other operating systems, install Python 3.12 and uv independently, then use `uv sync` and `uv run jupyter lab` (the Nix flake is optional).

### KDE/Firefox browser launching on NixOS

Do **not** export a global `LD_LIBRARY_PATH` from this flake. An older C++
runtime from the development environment can shadow the library needed by
`kde-open` and make `xdg-open` fail with a `GLIBCXX_...` error.

After updating your branch, unload any inherited old override with
`direnv reload` and a fresh terminal session if necessary. As an immediate
diagnostic, run `env -u LD_LIBRARY_PATH xdg-open https://www.python.org`.
If Jupyter still does not open Firefox automatically, use the URL it prints
or run `env BROWSER=firefox uv run jupyter lab`.

Verify that NumPy and scientific dependencies still import with:

```sh
uv run python -c 'import numpy, scipy, pandas, sklearn, statsmodels; print("scientific Python OK")'
```

Some PyPI wheels may require additional native runtime libraries on NixOS;
if this import check fails, address the missing library specifically (or use
`nix-ld`) instead of overriding the entire shell's library search path.


## Project data

**Do not commit confidential partner data to this public repository.** Dataset ownership, access conditions and publication permissions must be checked individually. In particular, making a dataset available for workshop analysis does not imply permission to publish it. Separate MIT (code) and CC BY 4.0 (teaching content) licensing files will be added along with the substantive course materials.
