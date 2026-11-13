# Matplotlib cheat sheet — MATH4SDG 2026

*For students using pandas and Matplotlib in JupyterLab. Make a figure answer a question, and use an `Axes` object to control its labels and appearance.*

## What is an `Axes`?

A **Figure** is the whole figure; an **Axes** (`ax`) is the plotting area with its title, x-axis, y-axis and plotted data. A pandas plotting method usually **returns an `Axes`** so we can modify it directly. The [insurance notebook](../notebooks/synthetic_insurance_claims.ipynb) follows this pattern.

## The recommended style: pandas produces the plot, `ax` controls it

```python
ax = data["claims_count"].plot.hist(
    bins=35,
    figsize=(8, 3),
    title="Invented claims per establishment-year",
)
ax.set_xlabel("Synthetic claim count")
ax.set_ylabel("Number of establishment-years");
```

In a Jupyter notebook using the inline backend, **the figure normally appears automatically**. You do not need `plt.show()` for this ordinary case. The final `;` tells Jupyter not to display the unhelpful `Text(...)` return value of the label-setting method. It does **not** hide the figure. It is optional.

### Common chart types

| Question | Example expression |
|---|---|
| How are numeric values distributed? | `ax = data["claims_count"].plot.hist(bins=35)` |
| How does a value change over time? | `ax = annual.plot(marker="o")` (temperature notebook) |
| How do categories compare? | `ax = by_sector["claims_per_100_worker_years"].plot.barh()` |
| Are two numeric variables related? | `ax = data.plot.scatter(x="worker_years", y="claims_count")` |

Always label the figure with the **actual units**. In the insurance backup, claims and cost values are synthetic; generated costs are **not Tanzanian shillings**. In the temperature backup, label NASA POWER temperatures as **gridded estimates**, not weather-station readings.

## Change labels, title and limits

```python
ax.set_xlabel("Worker-years")
ax.set_ylabel("Expected claims")
ax.set_title("Synthetic claim-count model")
ax.set_xlim(left=0)
ax.grid(alpha=0.3);
```

Use these on an existing `ax` rather than switching to global `plt.xlabel()` or `plt.title()`. `ax.set(xlabel="...", ylabel="...", title="...")` is a convenient alternative when several properties belong together.

## When you need a plot constructed from scratch

The insurance notebook stores observed 2025 claims in `y_test` and the model's expected counts in `model_predicted`:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(y_test, model_predicted, alpha=0.4)
ax.set_xlabel("Observed claims in 2025 (synthetic)")
ax.set_ylabel("Predicted mean claims in 2025")
ax.grid(alpha=0.3);
```

This compares observations against *expected values*, not exact predictions of random individual outcomes.

`plt.subplots()` **creates** the figure and axes. From then on we operate on `ax`. A model prediction plot should not suggest that an exact count for each establishment can be anticipated reliably.

## Compare several series on one `Axes`

In the temperature notebook, `annual` holds annual summaries and `results` contains the regression output:

```python
ax = annual.plot(marker="o", label="Annual temperature estimate")
ax.plot(results["years"], results["fitted"], label="Fitted trend")
ax.set_xlabel("Year")
ax.set_ylabel("Temperature (°C)")
ax.legend()
ax.grid(alpha=0.3);
```

The two data series must have compatible units and x-coordinates. If the data come from NASA POWER, say **grid-cell reanalysis estimate**, not direct weather-station measurement.

## Two panels: only when comparison helps

The next example assumes `years`, `temperatures` and `residuals` are arrays already calculated in earlier cells:

```python
fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 4))
ax_left.plot(years, temperatures)
ax_left.set_title("Annual temperature")
ax_right.plot(years, residuals)
ax_right.axhline(0, linestyle="--")
ax_right.set_title("Regression residuals")
fig.tight_layout();
```

Make separate cells and separate figures when the outputs answer independent questions. Do **not** make every small calculation into a subplot.

## Common mistakes

- **Missing labels or units:** a technically correct graph can still mislead.
- **Too many categories or bins:** detail can obscure the question.
- **Automatic axis scaling:** always inspect scales before comparing plots.
- **Confusing data and model:** give observed/reanalysis/synthetic data and fitted lines clear labels.
- **Using `plt.show()` everywhere:** usually unnecessary in notebook cells; useful in scripts or when display order needs explicit control.

## Ask AI to help you learn

> Explain what `ax = data["claims_count"].plot.hist(...)` returns and why we can then use `ax.set_xlabel(...)`.

> Show two ways to plot the same data: first with the global `plt` interface and then using an `Axes` object. Which is easier to extend and why?

> Review this plot for potentially misleading axis scales, missing units, or unclear labels. Do not change my data; explain each proposed change.

Try each suggestion, and verify visually that the plot answers the scientific question you intended. Never share confidential data or screenshots containing restricted records with external AI tools.

### Official learning resources

- [Matplotlib: Quick start (Figure and Axes)](https://matplotlib.org/stable/users/explain/quick_start.html)
- [Matplotlib: Axes API reference](https://matplotlib.org/stable/api/axes_api.html)
- [Matplotlib: Plot types](https://matplotlib.org/stable/plot_types/index.html)
- [pandas: Chart visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)

*Quick-reference draft, not a complete API manual. Teaching text: CC BY 4.0; code snippets: MIT.*
