# Facilitator notes — primary NASA POWER temperature exercise

**Context:** A flexible fallback for groups, not a six-day teaching schedule. Morning discussions should respond to problems encountered the preceding day. Invite groups to finish the day with one finding, one uncertainty, and one next step.

**Data source:** NASA POWER T2M is the daily average two-metre air temperature estimated for a coarse **reanalysis grid cell**, drawing principally on MERRA-2; it is **not a point observation from Dar es Salaam Airport**. NASA's method documentation records transitions between MERRA-2 and GEOS-IT near real time; this investigation ends in 2025, but users should still check source history and metadata. Do not imply independent observational confirmation from reanalysis.

**Plenary possibilities (10–20 minutes):**
- Data lineage and annual aggregation (12 adequately observed months, no forward-filling).
- Least squares from a NumPy design matrix, then cross-check with SciPy.
- Why the conventional confidence interval differs from a HAC/Newey–West interval; both are conditional on model assumptions.
- Gridded estimates versus station observations: using their common observation dates, gaps and sampling bias.
- How to interrogate AI-generated code and interpret the answers without outsourcing scientific judgment.

**Common pitfalls:** Calling NASA POWER 'measured station temperatures'; interpreting a small p-value as the probability the null is true; treating nearby grid cells as independent; taking a complete reanalysis series as proof of homogeneous climate measurements; claiming warming can be causally attributed to a specific source from one regression; extrapolating single-grid-cell results to all East Africa.

**MAT102 background:** [data exploration](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke3/K1_dataanalyse.ipynb), [least squares](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke13/Regresjon_temperaturer.ipynb), [seasonality](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke13/Variasjoner_temperatur.ipynb) and [testing trends](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke15/testhelding.ipynb). Revised material uses stronger time-series and provenance cautions.

**Workshop report:** insist on a clear scientific question, data source and retrieval date, units, analysis window, choice of reference period, mathematical method, robustness checks, and conclusions justified by the data.
