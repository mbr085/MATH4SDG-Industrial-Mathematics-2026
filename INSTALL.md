# Start the MATH4SDG Python workshop

**For students on Windows or macOS.** You do not need Git, a GitHub account, or a separate Python installation. Internet access is needed for the initial download and setup.

## 1. Download the materials

**[Download the workshop ZIP](https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026/archive/refs/heads/main.zip)**

Extract the ZIP file to a normal folder on your computer. Do not try to run notebooks inside the ZIP.

## 2. Install uv

[uv](https://docs.astral.sh/uv/getting-started/installation/) manages Python and the workshop libraries.

**Windows — PowerShell:**

```powershell
winget install --id=astral-sh.uv -e
```

If WinGet is unavailable, follow the [official uv Windows installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

**macOS — Terminal:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If you already use Homebrew, `brew install uv` is another option.

Close and reopen PowerShell or Terminal, then verify:

```bash
uv --version
```

You should see a version number.

## 3. Open a terminal in the extracted folder

**Windows:** Open the extracted folder in File Explorer, type `powershell` in the address bar, and press Enter.

**macOS:** Open Terminal, type `cd ` (including the space), drag the extracted folder into Terminal, and press Enter.

## 4. Start JupyterLab

In that terminal run:

```bash
uv sync --locked
uv run jupyter lab
```

The first command installs Python 3.12 and the required libraries if necessary. The second starts JupyterLab. If no browser tab opens, follow the local URL printed in your terminal.

For Friday's guided activity, open `notebooks/clustering_investigation.ipynb` using the JupyterLab file browser. **Stop at the prediction checkpoint.** The facilitator will introduce part two after a short discussion.

For optional independent practice, open `reference/pandas_cheatsheet.ipynb`, `reference/matplotlib_cheatsheet.ipynb`, or `notebooks/synthetic_insurance_claims.ipynb` (entirely synthetic data). The main workshop activities address problems and datasets from the participating industrial partners.

## Troubleshooting

- **uv not found:** reopen the terminal; see the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).
- **Packages do not download:** check your Internet connection; the first setup needs it.
- **Notebook cannot find its files:** keep the extracted folder structure, and start JupyterLab in the repository root.
- **Cannot import a library:** use `uv run jupyter lab` rather than a different Python installation.
- **Setup is slow:** one working computer per student group is enough to begin.

**Partner data:** Do not upload restricted partner data to GitHub, cloud notebooks, or external AI services without explicit permission.

## Optional — use Git instead of the ZIP

Git is **not required**. On Windows, install [Git for Windows](https://git-scm.com/install/win) or use `winget install --id Git.Git -e --source winget`. On macOS, try `git --version` first; if unavailable, use `xcode-select --install` for Apple's Command Line Tools or `brew install git` with Homebrew.

In the parent folder where you want the project, run:

```bash
git clone https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026.git
cd MATH4SDG-Industrial-Mathematics-2026
uv sync --locked
uv run jupyter lab
```

For a **clean, unmodified** checkout, `git pull --ff-only` followed by `uv sync --locked` retrieves later updates. Keep copies of edited notebooks before updating and ask for help with conflicts.

A ZIP is a snapshot. To obtain updated materials without Git, download another ZIP, extract it to a **new folder**, and preserve your own notebook work.
