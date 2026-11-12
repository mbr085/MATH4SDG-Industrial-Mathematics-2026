# Facilitator notes — optional Meteostat missingness exercise

The **primary** temperature-trend project now uses
[NASA POWER gridded reanalysis](../nasa-power-temperature/README.md).
The Meteostat station series is retained only to illustrate the consequences
of inadequate observational coverage.

**Why:** In the instructor-inspected Dar es Salaam Meteostat record for
1986–2025, about a third of daily temperatures were missing, leaving no
eligible years in the early 1986–1995 decade under the preselected rule of
at least 20 observed days in each calendar month.

**Questions worth discussing:**
- When do missing days undermine inference, rather than simply reduce precision?
- Why does forward-filling missing months not solve the problem?
- What would we need from TMA about station history or data provenance?
- Does NASA POWER give an independent observational reference? Why not?
- If we restrict a POWER-to-station comparison to dates that have observations,
  could the resulting agreement be selection-biased?

Invite students to report an inconclusive result when warranted. This is a
flexible group exercise, not a prescribed lecture. Other MAT102 topics on
regression and confidence intervals remain relevant, but should not be
applied uncritically to an unrepresentative set of years.

**AI:** Encourage participants to use AI to inspect code and assumptions, not
to fill in absent scientific evidence or expose non-public data.
