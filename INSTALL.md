# Install the MATH4SDG Python workshop tools

**For students on Windows and macOS.** The workshop uses Python **3.12**, but you do **not** need to install Python manually first: [uv](https://docs.astral.sh/uv/) can manage the interpreter and install the locked Python libraries.

You need an Internet connection for the initial installation. The repository includes the notebooks and synthetic examples, so many exercises can then be used offline.

## 1. Install uv

Choose the commands for your computer. You only need **one installation method**.

### Windows: PowerShell

Open **PowerShell** from the Start menu. Install uv with Windows Package Manager:

```powershell
winget install --id=astral-sh.uv -e
```

If `winget` is not available, the [official uv standalone installer](https://docs.astral.sh/uv/getting-started/installation/) is an alternative:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS: Terminal

Open the **Terminal** app and run the [official uv installer](https://docs.astral.sh/uv/getting-started/installation/):

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or, if you already use Homebrew:

```sh
brew install uv
```

**Close and reopen your terminal** after installing uv, then check:

```sh
uv --version
```

If it prints a version number, uv is available. If it cannot find the command, check the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/) for your system's PATH setup.

## 2. Get the repository

If Git is installed, use these commands in PowerShell or Terminal:

```sh
git clone https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026.git
cd MATH4SDG-Industrial-Mathematics-2026
```

If you do **not** have Git, open the [repository on GitHub](https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026), select **Code → Download ZIP**, extract it, and open a terminal inside the extracted folder. You do not need Git merely to run the notebooks.

## 3. Install all workshop Python tools

Run these two commands **from inside the repository folder**:

```sh
uv sync --locked
uv run jupyter lab
```

The first command creates the project-local `.venv` and installs the libraries listed in `pyproject.toml` at the versions resolved by `uv.lock`. These include **JupyterLab, ipykernel, NumPy, pandas, Matplotlib, SciPy, scikit-learn, statsmodels and Meteostat**. There is **no separate workshop Python package** to install, and no need to install the libraries individually.

The repository requests **Python 3.12** in `.python-version`. On typical Windows and macOS installations, uv can download this Python version as part of setup.

The second command starts JupyterLab using that environment. Open the address printed in the terminal if a browser tab does not open automatically.

## 4. Start exploring

Use the JupyterLab file browser to open:

- `reference/pandas_cheatsheet.ipynb` and `reference/matplotlib_cheatsheet.ipynb` — executable Python reference notebooks
- `notebooks/synthetic_insurance_claims.ipynb` — an **entirely invented** insurance dataset
- `notebooks/east_africa_temperature_trends.ipynb` — a NASA POWER grid-cell series **if downloaded locally**; otherwise explicitly synthetic practice data

Begin with a reference notebook if pandas or plotting is unfamiliar. The projects are **optional**, and the main workshop focuses on real problems posed by industry partners.

## 5. Check the installation (optional)

From the repository folder:

```sh
uv run python -c "import numpy, pandas, matplotlib, scipy, sklearn, statsmodels, meteostat; print('Scientific tools OK')"
uv run python -m unittest discover -s tests -v
```

## Troubleshooting

- **`uv` not found:** restart PowerShell or Terminal, then check `uv --version`. If necessary, follow the [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).
- **`git` not found:** use GitHub's **Download ZIP** option.
- **Python or package download fails:** verify your Internet connection; initial setup requires package downloads.
- **Jupyter kernel cannot import a library:** start JupyterLab with `uv run jupyter lab` from the repository folder and select the project's Python kernel.
- **Temperature data are unavailable:** the notebook transparently uses a **synthetic** fallback. Synthetic results are *not climate evidence*.

Keep confidential industry data out of this public repository and do not share partner data with external AI tools without permission.

**Reference:** [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) and [working with uv projects](https://docs.astral.sh/uv/guides/projects/).
