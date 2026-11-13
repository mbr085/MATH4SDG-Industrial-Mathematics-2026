# pandas cheat sheet — MATH4SDG 2026

*For students working with data in JupyterLab. This is a reference, not an additional lesson: find a command when you need it, run a small cell, and inspect the result.*

In the [insurance notebook](../notebooks/synthetic_insurance_claims.ipynb), `data` is a **DataFrame** (a table), and `data["claims_count"]` is a **Series** (one column). All insurance data are **synthetic**, not industry observations. The [temperature notebook](../notebooks/east_africa_temperature_trends.ipynb) also uses pandas, but its NASA POWER values are model-informed gridded estimates, not direct weather-station observations.

## Look at a dataset

| Question | Python expression | What you learn |
|---|---|---|
| What are the first rows? | `data.head()` | Default: five rows |
| How many rows and columns? | `data.shape` | A `(rows, columns)` pair |
| What are the column names? | `data.columns` | Names available to select |
| What types are the columns? | `data.dtypes` | Integer, float, object, etc. |
| How many values are missing? | `data.isna().sum()` | Missing entries per column |
| Which years appear? | `sorted(data["year"].unique().tolist())` | Ordinary Python integers, sorted |
| How many rows for each category? | `data["sector"].value_counts(dropna=False)` | Counts including missing values |

In a notebook, a **last expression is displayed automatically**. You normally do not need to write `print(data.head())` or `display(data.head())` if the expression is last in its cell.

## Select rows and columns

```python
# One column: produces a Series
data["claims_count"]
```

```python
# Two columns: produces a DataFrame
data[["year", "claims_count"]]
```

```python
# Rows satisfying a condition, with selected columns
data.loc[data["year"] == 2025, ["sector", "claims_count"]]
```

`data.loc[...]` selects by **labels and conditions**, while `data.iloc[...]` selects by **integer positions**. A column may contain missing values, written as `NaN` or `pd.NA`.

## Clean and transform carefully

To avoid changing the original table, first make a separate copy:

```python
clean_data = data.copy()
```

Then replace missing sector names in the **copy**:

```python
clean_data["sector"] = clean_data["sector"].fillna("Unreported")
```

`fillna()` returns values with missing entries filled. **Without the assignment**, `data["sector"].fillna("Unreported")` does not change the original column.

```python
# Create a derived column: synthetic claims per 100 worker-years
# Be careful: one small establishment can have a very noisy observed rate.
data["rate_per_100"] = 100 * data["claims_count"] / data["worker_years"]
```

`fillna()` and `dropna()` are **analysis choices**, not automatic repairs. Do not silently fill missing temperature observations, because doing so may change a trend estimate.

Some scientific-Python functions use NumPy arrays rather than pandas objects:

```python
exposure = data["worker_years"].to_numpy()
```

`to_numpy()` extracts the column's values as a NumPy array. It does **not** change the underlying data.

## Combine groups correctly

For insurance, a **sector-wide claim rate** must be total claims divided by total exposure, rather than an unweighted average of establishment rates.

**Step 1 —** Keep the original data unchanged and label missing categories:

```python
clean_data = data.copy()
clean_data["sector"] = clean_data["sector"].fillna("Unreported")
```

**Step 2 —** Group establishments by sector, and add claims and worker-years within each group:

```python
by_sector = clean_data.groupby("sector")[["claims_count", "worker_years"]].sum()
by_sector
```

Here, the *double brackets* `[["claims_count", "worker_years"]]` select **two columns**. `groupby("sector")` puts rows with the same sector together; `.sum()` adds each selected column within each group.

**Step 3 —** Compute the rate from the totals:

```python
by_sector["claims_per_100_worker_years"] = (
    100 * by_sector["claims_count"] / by_sector["worker_years"]
)
by_sector.round(2)
```

**Why the order matters:** Two establishments have 1 claim each, but exposures of 10 and 90 worker-years. Their rates are 10 and 1.11 claims per 100 worker-years. The combined rate is **2 claims per 100 worker-years**, not their unweighted average (5.56). Using totals respects the different exposures.

`groupby(...).mean()` is useful for other questions, but an unweighted mean of establishment-level rates answers a different question.

## Time series: one step at a time

In the temperature notebook, `data` already has a date index. Select the `temp` column and explicitly represent daily dates:

```python
daily = data["temp"].asfreq("D")
```

```python
# Monthly means; MS means "month start"
monthly = daily.resample("MS").mean()
monthly.head()
```

This example assumes a **datetime index**. `asfreq("D")` can reveal missing calendar dates as `NaN`; `resample("MS").mean()` groups days into calendar months, ignoring missing values when computing means. **Do not treat a month with one valid day as comparable with a complete month.** The temperature notebook has a separate completeness rule for its annual summaries.

## Ask AI to help you learn

Try one focused question at a time:

> Explain `data.loc[data["year"] == 2025, ["sector", "claims_count"]]` using a small invented three-row table. What type of object does it return?

> Explain why `sum(claims) / sum(exposure)` is different from the mean of `claims / exposure`. Construct a simple numerical counterexample.

> Suggest a clearer way to write this pandas operation without changing its result. What should I check to verify that the revised code behaves identically?

**Verify AI-generated suggestions:** inspect the first few rows, count missing values, compare aggregates, and check units. Never paste confidential industry records into an external AI tool without permission.

### Official learning resources

- [pandas: 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas: Group by — split, apply, combine](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas: Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [pandas: Time series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [pandas: Plotting](https://pandas.pydata.org/docs/user_guide/visualization.html)

*A short reference, not a complete API manual. Examples use the MATH4SDG notebooks. Teaching text: CC BY 4.0; code snippets: MIT.*
