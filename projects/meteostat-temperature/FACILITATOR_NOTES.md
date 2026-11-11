# Facilitator notes — Meteostat backup

**Format:** Industry partners present their problems on 18 November; groups mainly work from 19 November, with facilitators circulating. Do **not** schedule a five-day Meteostat lecture course. Use a 10–20 minute morning demonstration when useful, and 2–3 minutes per group for end-of-day progress reports.

**Suggested prompts:** What does a “40-year difference” measure? How much weather is missing, and does it vary by month? Why is carrying forward a missing season misleading? What is the design matrix? Can the group reproduce the slope using two independent implementations? Does accounting for correlated annual errors alter the interval? How would a station relocation distort the inference? What evidence would increase scientific confidence?

**Mathematical caution:** The notebook uses all-twelve-months annual means, with at least 20 daily temperatures per month. Both the completeness rule and the regression period are choices to interrogate. Standard errors and Newey–West/HAC estimates address only some statistical assumptions; they cannot resolve unrecorded station history, bias from non-random missingness, regional representativeness, or causal attribution. A precise estimated slope is not necessarily a defensible climate claim.

**Synthetic mode:** Deliberately includes 0.020 °C/year artificial trend, a +0.55 °C artificial jump in 2008, serial dependence, seasonality, and missing blocks. Students should question whether the fitted linear slope recovers the underlying trend. These results must never be communicated as observations from Tanzania.

**MAT102 lineage:**
- [Week 3, data analysis](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke3/K1_dataanalyse.ipynb): Meteostat and pandas.
- [Week 13, regression](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke13/Regresjon_temperaturer.ipynb): NumPy least squares and model comparison.
- [Week 13, seasonal variation](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke13/Variasjoner_temperatur.ipynb): annual sine/cosine terms.
- [Week 15, hypothesis testing](https://github.com/mbr085/V26MAT102/blob/main/notebooks/uke15/testhelding.ipynb): why model assumptions matter.

Unlike the older notebooks, this project explicitly flags serial dependence, handles missingness without forward filling, and avoids interpreting p-values as hypothesis probabilities.

**AI policy:** AI can explain, generate and test code, but participants must verify assumptions and results. Never submit confidential partner data, records or personal information to external AI tools without permission. End each day by inviting groups to state one result, one uncertainty and one next action.
