# Optional backup project — Synthetic workplace insurance claims

**Question:** Can a simple, exposure-aware model help anticipate the expected number of insurance claims from different types of establishments in a future year? What could make the model unreliable?

This investigation is intended for the **MATH4SDG UDSM bootcamp** as a fallback when an actual industry-provided problem or dataset is not suitable for inexperienced students. The workshop remains primarily student-led work on questions presented by NBS, TMA, insurers, WCF and other partners; this project **does not imply** their participation in its creation or use of their records.

## Important: this dataset is entirely invented

Every establishment, claim count, sector rate, programme assignment and cost is **synthetic**. The data do **not** come from the Workers Compensation Fund, TIRA, an insurance company or another Tanzanian institution. Synthetic costs are in arbitrary accounting units, **not Tanzanian shillings (TZS)**. No real people or businesses are represented.

The synthetic dataset is generated in Python on demand; no confidential or proprietary data is needed, and no external download is required. Its generated values are offered under CC0 1.0, code under MIT, and educational prose under CC BY 4.0 (see [dataset terms](../../DATA_LICENSES.md)). Never report model outputs as real insurance rates.

## Run on NixOS, Linux, macOS or Windows

From the repository root with the Python environment already prepared:

```sh
uv sync --locked
uv run jupyter lab
```

Open [the student notebook](../../notebooks/synthetic_insurance_claims.ipynb) directly inside `notebooks/`. It imports `bootstrap`, a small helper stored beside the notebook that makes the existing `tools/` functions accessible. No extra package installation is required. Start JupyterLab at the repository root; the notebook kernel normally starts in its own `notebooks/` folder. Moving a notebook into an arbitrary subfolder may require updating the imports.

Optional: create a CSV that can be opened in a spreadsheet (ignored by Git):

```sh
uv run python tools/synthetic_insurance.py
```

Run offline tests:

```sh
uv run python -m unittest discover -s tests -v
```

## Suggested group investigation

The **minimum** is an analysis of the fictional records, a transparent baseline for claims per worker-year, and a Poisson regression built directly in the notebook (one-hot encoding, `Pipeline`, `PoissonRegressor`, and exposure-weighted `fit`). Students evaluate predictions with scikit-learn's `mean_poisson_deviance` directly, then compare with held-out 2025. Then refit the chosen model on 2021–2025 and forecast expected 2026 claims under an explicitly hypothetical planning scenario, reusing 2025 exposure and predictors as assumptions. The dataset contains no 2026 outcomes. A useful result includes one explanation of why the model might be misleading.

The **extensions** can be divided between groups: investigate missing sector labels and reporting bias; study claim severity (costs are recorded *after* claims); examine model calibration by sector; explore alternate validation windows; or test whether apparent correlations with the programme can be interpreted causally.

The synthetic data deliberately contain persistent unobserved establishment risk, changes in incidence in the last year and selective programme uptake. Students are not expected to infer the precise hidden mechanism, but should ask whether simple estimates and narrow confidence intervals capture these sources of uncertainty.

## Facilitation and reporting

Facilitators circulate between groups and may introduce mathematical or computational tools in short morning plenaries when requested by the projects. The afternoon plenary can ask each group to report one finding, one source of uncertainty, and one next step.

A five-minute end-of-project presentation should include the held-out 2025 validation and an explicitly hypothetical 2026 forecast; no 2026 outcomes are supplied. It should cover:

- What is predicted, for whom, and in which units?
- Why do worker-years matter?
- Does a model beat the baseline **on future-year data**?
- Which assumptions are least credible in a real insurance context?
- What further information would be required from a partner before using the results?

AI tools may help students develop Python, explain the Poisson objective or uncover leakage. Students must verify their suggestions and must not upload confidential partner data to external AI services.

**No students or industry partners should use the synthetic output for real-world decisions** about insurance pricing, safety inspections, claims entitlement, worker compensation, or individual establishments.

### Technical reference

The exposure-weighted Poisson frequency method follows the [scikit-learn example on insurance claims](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html). This source explains modelling frequency as claims divided by exposure with exposure as sample weight; its examples use a different (real) insurance domain and are not data for this workshop.

## Notebook style

The student notebook favors short pandas steps rather than chains of operations, one conceptual step (and usually one visible output) per code cell, and explicit Matplotlib `Axes` methods rather than unnecessary `plt.show()` calls. The *model construction, fitting, prediction and scoring* are deliberately shown inside the notebook rather than hidden behind helper functions. A small optional activity shows why scoring counts or exposure-weighted rates by Poisson deviance produces identical model rankings on the same records (though the scales differ). These conventions are intended for students who are still learning scientific Python.
