# Facilitator notes — primary NASA POWER temperature exercise

**Context:** A flexible fallback for groups, not a six-day teaching schedule. Morning discussions should respond to problems encountered the preceding day. Invite groups to finish the day with one finding, one uncertainty, and one next step.

**Data source:** NASA POWER T2M is the daily average two-metre air temperature estimated for a coarse **reanalysis grid cell**, drawing principally on MERRA-2; it is **not a point observation from Dar es Salaam Airport**. NASA's method documentation records transitions between MERRA-2 and GEOS-IT near real time; this investigation ends in 2025, but users should still check source history and metadata. Do not imply independent observational confirmation from reanalysis.

**Plenary possibilities (10–20 minutes):**
- Data provenance, one daily-completeness check, and direct calendar-year means (no filling of missing values).
- Least squares from a NumPy design matrix, then cross-check with SciPy.
- Why the conventional confidence interval differs from a HAC/Newey–West interval; both are conditional on model assumptions.
- Gridded estimates versus station observations: using their common observation dates, gaps and sampling bias.
- How to interrogate AI-generated code and interpret the answers without outsourcing scientific judgment.

**Pedagogical revision:** The main investigation now assumes **complete daily input** and checks this exactly once against the 1986–2025 calendar, including leap days. It rejects incomplete or non-finite series. Annual temperature means are computed directly from daily estimates by year; students do not need monthly coverage criteria, an equal-weight-month convention, or a separate reference-implementation check. The offline synthetic fallback is complete by design and remains prominently labelled. Notebook cells still show least-squares regression, conventional and HAC intervals, and overlapping-window sensitivity. The older `annual_means` helper and its missingness criteria remain relevant to the **separate optional Meteostat station exercise**, where daily observations are incomplete.

**Focused discussion: sensitivity to the starting year (section 9).**
In an executed NASA POWER notebook reviewed for this project, the annual
least-squares trend ending in 2025 was approximately **+0.152 °C/decade**
when starting in 1986, but **+0.036 °C/decade** when starting in 2001.
These are example *estimates from a particular retrieved reanalysis series*,
not measurements at a weather station or evidence that warming has stopped.
Students should compute their own results, including the HAC intervals for
all four nested windows, without treating these numbers as target answers.

Ask: Do the nested-period fits estimate the same quantity? Are their slopes
independent? **No**: the windows share observations, so comparing the
confidence intervals is not a statistical test of a change in trend.
An optional mathematical challenge is a **single segmented regression**,
with a candidate change point specified in advance, testing the change-in-slope
coefficient with an autocorrelation-aware interval. This is a *different*
estimand from subtracting two overlapping OLS slopes. If a breakpoint is
chosen because the graph looks interesting, subsequent naive significance
calculations risk overstating the evidence. Contrast statistical precision
with uncertainty from reanalysis inputs, model changes, and spatial scale.

**Common pitfalls:** Calling NASA POWER 'measured station temperatures'; interpreting a small p-value as the probability the null is true; treating nearby grid cells as independent; taking a complete reanalysis series as proof of homogeneous climate measurements; claiming warming can be causally attributed to a specific source from one regression; extrapolating single-grid-cell results to all East Africa.

**MAT102 background:** [data exploration](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke3/K1_dataanalyse.ipynb), [least squares](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke13/Regresjon_temperaturer.ipynb), [seasonality](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke13/Variasjoner_temperatur.ipynb) and [testing trends](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke15/testhelding.ipynb). Revised material uses stronger time-series and provenance cautions.

**Workshop report:** insist on a clear scientific question, data source and retrieval date, units, analysis window, choice of reference period, mathematical method, robustness checks, and conclusions justified by the data.
