# Facilitator notes — Synthetic insurance claims

**Role:** An optional, self-contained backup for the 18–23 November 2026 industry bootcamp; not a compulsory lesson and not an industry deliverable. Use only if one or more groups lack a tractable industry-supplied question. The group should choose a manageable question and proceed at its own pace.

## Core mathematical idea

If establishment $i$ has exposure $e_i$ measured in **worker-years** and claim count $N_i$, the simplest frequency estimator is

$$\widehat{\lambda} = \frac{\sum_i N_i}{\sum_i e_i}.$$

Expected counts are $e_i\widehat{\lambda}$. For a Poisson GLM, $\log E[N_i] = \log e_i + \beta_0 + x_i^\top\beta$; equivalently, scikit-learn's `PoissonRegressor` fits counts/exposure with `sample_weight=exposure`. Check that students keep **counts** (not rates) on the test-year Poisson-deviance scale.

A meaningful **baseline first** is more important than more complicated models. The notebook fits on 2021–2024 and tests on 2025, mimicking use of information available before a future year. No model feature includes same-year claims or total claim costs.

## Synthetic design, not factual claims

The generator creates fictitious establishments across fictional zones and broad sectors. The assumptions and all numerical choices are invented:

- Larger exposure tends to increase claim counts even at identical underlying frequency.
- Different sectors and zones have different *artificial* expected frequencies.
- Each establishment has persistent, unobserved risk, so repeated annual outcomes are not independent unconditional observations.
- Programme uptake is selective: higher-risk sectors and unobserved establishment traits affect it. **Associations with the programme are not causal estimates**, even though the simulation assigns an artificial effect to it.
- The baseline rate changes in **2025** (a 22% multiplier in the generator). This makes temporal generalization interesting; even a good feature model may systematically underpredict.
- A small fraction of sectors are missing, while skewed total claim costs are generated after the claims. Costs use arbitrary units, **not TZS**.

These are teaching mechanisms, not rates or policy effects at WCF, TIRA, any insurer, or anywhere in Tanzania.

## Suggested short interventions

**Data questions:** What is a worker-year? Is averaging row-wise frequencies appropriate? When do missing sector labels matter?

**Modelling:** Why does the baseline use a ratio of *sums*? Derive the log-likelihood derivative for the intercept-only Poisson model. What is the role of the offset $\log(e_i)$? Ask AI for an implementation, then verify it independently.

**Validation:** Keep 2025 as a held-out historical validation year and introduce 2026 only as a hypothetical forecast. Assume 2026 exposures, sectors, zones and programme statuses equal their 2025 values, explicitly labelled as planning assumptions, not observations. Refit using all 2021–2025 outcomes after evaluation and never invent 2026 claim outcomes. Why not split rows randomly when investigating the next year? Why can a model predict claim *expectations* but not exact individual annual counts? What changes in 2025? Could a model overfit to test-year results?

**Uncertainty:** Simple exact Poisson-rate intervals assume a count model with independent events and a stable common rate. The generator violates some of those assumptions. Encourage students to distinguish conditional statistical uncertainty from omitted establishment differences, reporting bias, synthetic assumptions and the 2025 change.

**Ethics:** No actual claims, person-level data, institutions or currency values are represented. Real-world pricing, safety and worker-compensation decisions require domain expertise, privacy safeguards, historical validation and fairness assessment. Do not upload real partner records to public GitHub or outside AI services without permission.

**Teaching-code style:** Use simple pandas operations, minimal chaining, one conceptual step and one meaningful output per cell, and the Matplotlib `Axes` interface. The notebook begins with `import bootstrap` from `notebooks/bootstrap.py` rather than displaying path-management code; packaging remains open for later consideration. Pyright is configured in `pyproject.toml` to use the uv `.venv`.

## Five-minute group update

Ask groups to state: their problem, baseline, model result **on held-out 2025**, a clearly hypothetical **2026** forecast, one uncertainty, and a next action or question for the partner. A justified conclusion that the model is not reliable enough is a useful scientific outcome.

Scikit-learn reference: [Tweedie regression on insurance claims](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html), especially the exposure-weighted Poisson frequency model.
