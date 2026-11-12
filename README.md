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

**Do not commit confidential partner data to this public repository.** Dataset ownership, access conditions and publication permissions must be checked individually. In particular, making a dataset available for workshop analysis does not imply permission to publish it. Separate MIT (code) and CC BY 4.0 (teaching content) licensing files will be added along with the substantive course materials.
