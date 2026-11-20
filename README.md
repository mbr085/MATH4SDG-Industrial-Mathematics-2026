# MATH4SDG — Industrial Mathematics Bootcamp and Workshop 2026

Python and computational teaching resources for the **University of Dar es Salaam (UDSM)** MATH4SDG industrial mathematics bootcamp (draft programme: 19–24 November 2026) and follow-up workshop (3–4 December 2026).

The bootcamp is principally **group work on industry-provided problems**. All industrial partners are expected to attend and provide data. Approximately **27 students and five facilitators** are expected; five groups of roughly five or six students may be a useful starting point, depending on the industrial problems. Facilitators circulate and share expertise. Check each partner's data-access and confidentiality conditions. Public synthetic investigations and climate-data examples remain optional teaching resources, not replacements for the industry problems.

## Getting started — Windows and macOS

1. **[Download the workshop materials (ZIP)](https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026/archive/refs/heads/main.zip)** and extract them. No Git installation or GitHub account is needed.
2. **[Install uv](https://docs.astral.sh/uv/getting-started/installation/)** for Windows or macOS. It manages Python 3.12 and the required packages.
3. Open PowerShell or Terminal **inside the extracted folder** and run:

```bash
uv sync --locked
uv run jupyter lab
```

For detailed Windows and macOS guidance, see [INSTALL.md](INSTALL.md). Git is optional. Download the ZIP and run the first setup while Internet access is available.

## Project data

**Do not commit confidential partner data to this public repository.** Dataset ownership, access conditions and publication permissions must be checked individually. In particular, making a dataset available for workshop analysis does not imply permission to publish it. Code is licensed [MIT](LICENSE); original teaching notes are [CC BY 4.0](LICENSE-CONTENT.md); datasets have [separate terms](DATA_LICENSES.md).

## Friday plenary — editable Quarto slides

The nine-slide presentation for **20 November 2026**, *From Industrial Problems to Mathematical Models — and Reliable Conclusions*, is maintained as editable [Quarto / Reveal.js source](presentations/2026-11-19/index.qmd), with [presentation instructions](presentations/2026-11-19/README.md). It introduces experimental design, transparent baselines, model validation, and the optional clustering activity; the data-generating reveal is deliberately kept outside this public repository.

After entering the repository's Nix development shell (via direnv or `nix develop`), preview it locally with:

```sh
quarto preview presentations/2026-11-19/index.qmd
```

The presentation is **not a compulsory machine-learning lesson**. Students work primarily on partner-provided problems; the slide source and synthetic exercises are open resources.

## Saturday workshop — AI as a mathematical collaborator (21 November)

The [two-station AI weather notebook](notebooks/ai_assisted_weather_modelling.ipynb) supports a **60-minute student-led exercise** in reconstructing missing temperatures from incomplete time series. All measurements are **entirely synthetic**; they are not data supplied by TMA or another industry partner.

Students inspect 270 days with missing temperatures at **both stations**. The helper constructs one prediction case per station/day, using the other station's **observed same-day** temperature when available and **yesterday's completed temperature** at either station (observed or provisionally estimated) as a historical feature. The first 210 days provide training examples and the next 60 days provide held-out validation examples; some originally observed validation values were deliberately concealed and are recorded in [validation answers](data/exercises/ai_weather_validation_answers.csv) for scoring only.

Students compare a simple baseline with **two different models constructed using generative AI**, ask AI to criticize both models, then **explicitly choose a prediction function** before independent testing. Each evaluation now supplies only **strictly earlier training observations** and **one station/day case at a time**, avoiding accidental future information in the provided inputs. The [final 60-day dataset](data/exercises/ai_weather_final.csv) is **obfuscated**, not securely encrypted. The instructor reveals a short deobfuscation function after the model decision. The notebook ends with a five-group comparison table. No new packages or plenary intervention are required.

**For students who already unpacked the original repository ZIP:** copy the updated notebook into `notebooks/`, and copy all **three** `ai_weather_*.csv` files into `data/exercises/` without replacing either folder. Start JupyterLab as before, double-click `notebooks`, and open `ai_assisted_weather_modelling.ipynb`. Do not reuse older weather workshop CSVs with this redesigned notebook.

Do not upload confidential or partner-provided data to an external AI assistant without authorization. These synthetic results do not demonstrate a validated real-world weather imputation system.

## Student quick references

These short **executable Jupyter notebooks** support students who are learning Python while investigating mathematical questions. They are **not additional compulsory lessons**. Each starts with a small, wholly invented dataset so students can run and edit examples without downloading data or executing another notebook; each also links to official documentation and suggests focused AI questions that students can independently verify.

- [pandas Jupyter cheat sheet](reference/pandas_cheatsheet.ipynb) — inspect tables, select data, handle missing values, group by sector, calculate exposure-adjusted rates, and summarize time series.
- [Matplotlib Jupyter cheat sheet](reference/matplotlib_cheatsheet.ipynb) — make labelled plots using explicit `Axes` objects, compare model outputs with observations, and choose plots that communicate units and data provenance.

The two optional backup notebooks link directly to both references. In JupyterLab, open the `.ipynb` file, run its setup cell, and then run examples as needed. Do not share restricted industry data with external AI services.

## Student investigations — apparent patterns and independent validation

Two **optional** Jupyter investigations invite students to propose candidate groups or distinguishing measurements and evaluate interpretations on fresh data. The clustering exercise is split into two notebooks, with a deliberate prediction-and-discussion checkpoint between them. They use entirely synthetic teaching measurements and only packages already included in the workshop environment. The data-generating mechanisms are deliberately withheld from the student notebooks and will be discussed with the facilitator after students record their initial interpretations.

- [Are these groups real? — clustering, part 1](notebooks/clustering_investigation.ipynb). Inspect 90 observations, apply the fixed sign rule and examine a silhouette score. **Stop and record a prediction** before the facilitator introduces the independent second notebook during the session. The samples are independent, not remeasurements or paired rows; K-means is optional.
- [Which measurement distinguishes the groups? — feature selection investigation](notebooks/feature_selection_investigation.ipynb). Start with 100 observations, two supplied labels, and 200 measurements, then select a distinguishing feature and test the **same selected feature** on independent measurements.

The pre-generated, wholly fictional CSV files are under [`data/exercises/`](data/exercises/). Keep the repository folder structure when opening the notebooks locally; they load their files using relative paths. **Run the discovery part and write down an interpretation before opening the fresh data.** These are independent exercises rather than a required sequence. They do not use data from any Tanzanian institution or industrial partner.

## Further learning and datasets — Kaggle

[Kaggle](https://www.kaggle.com/) offers optional, practical learning materials and a searchable [dataset collection](https://www.kaggle.com/datasets). Use these resources **on demand**, when they help answer a question arising from an industry-partner problem or an optional backup investigation. They are not required courses, a separate workshop project, or a replacement for this repository's Python/Jupyter environment.

- [Pandas](https://www.kaggle.com/learn/pandas) — explore, filter, clean and summarize tabular data.
- [Intro to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning) — build basic prediction models and understand validation and overfitting.
- [Time Series](https://www.kaggle.com/learn/time-series) — investigate trends, seasonality, lagged relationships and forecasting.
- [Kaggle Datasets](https://www.kaggle.com/datasets) — find illustrative or supplementary public datasets when appropriate.

**Evaluate data before using it:** check the original source, whether observations are real or synthetic, coverage and units, limitations, and the specific licence and permissions. Publicly downloadable does not necessarily mean reusable or redistributable. Do **not** upload restricted partner data to Kaggle or other external services, and do not commit downloaded data here without clear permission; see [Project data](#project-data), [DATA_POLICY.md](DATA_POLICY.md) and [DATA_LICENSES.md](DATA_LICENSES.md). The NASA POWER investigation remains our documented climate-data backup.

Kaggle competitions often focus on predictive scores. For this bootcamp, **problem formulation, transparent assumptions, appropriate mathematics and interpretation** matter at least as much as model accuracy. Students can work entirely with the provided local notebooks; Kaggle accounts and online lessons are optional.

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

The temperature notebook makes **one daily-completeness check**, then calculates **annual means directly from daily temperatures** before least-squares fitting and uncertainty analysis. Its synthetic offline fallback also has complete daily coverage; missing station observations are explored separately in the optional Meteostat investigation. The pandas and Matplotlib Jupyter cheat sheets linked near the top remain optional references.

The original Meteostat station series was found to lack sufficient early observations for the intended 40-year comparison. The optional station exercise focuses on **missing observations and their consequences**, rather than duplicating the complete-data trend analysis. For that optional exercise:

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

The notebook asks how to estimate *expected claim counts* while accounting for exposure measured in worker-years. Students compare a pooled constant-rate baseline, an exposure-adjusted rate for each sector–zone–programme profile (without smoothing), and a Poisson regression. All three are trained on 2021–2024 and evaluated on held-out 2025 data. The profile baseline uses the same recorded predictors but can be more flexible than the regression; students discuss what each comparison establishes.

```sh
uv sync --locked
uv run jupyter lab
```

Open [the student notebook](notebooks/synthetic_insurance_claims.ipynb). No download is needed; the notebook generates deterministic synthetic data in memory. See [facilitator guidance](projects/insurance-claims/FACILITATOR_NOTES.md). Run the [offline tests](tests/test_insurance_backup.py) with the existing `unittest` command above.

An [optional advanced companion notebook](notebooks/advanced_insurance_size_and_exposure.ipynb) investigates company size, exposure and observed claim frequency, including the integer-count hyperbolas and an exposure-offset Poisson model. It is intended for groups seeking a further mathematical challenge; the introductory notebook remains the starting point.

The artificial records may be regenerated as a **local ignored CSV** using `uv run python tools/synthetic_insurance.py`. These classroom values have no real-world insurance interpretation; they are offered under CC0 1.0 and are documented in [DATA_LICENSES.md](DATA_LICENSES.md).

### Insurance notebook presentation and editor setup

For the [synthetic insurance claims notebook](notebooks/synthetic_insurance_claims.ipynb), introductory calculations are broken into understandable pandas steps with a single conceptual purpose per cell; plots use explicit Matplotlib `Axes` methods. The notebook directly constructs the one-hot encoder, Poisson regression pipeline and exposure-weighted fit, then calls `mean_poisson_deviance` without a scoring wrapper. It evaluates predictions against 2025 and separately forecasts expected claims for a hypothetical 2026 scenario, with no 2026 outcomes supplied.

The notebook imports `bootstrap` from [notebooks/bootstrap.py](notebooks/bootstrap.py) to connect to the existing `tools` modules. Start JupyterLab from the project root and keep the supplied notebook inside the `notebooks/` directory. No local project package installation is required for now. The `[tool.pyright]` section in `pyproject.toml` points Neovim/Pyright at the uv-managed `.venv`.
