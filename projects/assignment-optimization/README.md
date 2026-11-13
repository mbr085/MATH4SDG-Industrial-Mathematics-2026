# Optional backup challenge — Who should do which job?

**MATH4SDG / UDSM, November 2026 · Fictional optimization problem**

**Situation.** A fictional company needs to complete four different jobs today: **Inspection**, **Inventory**, **Transport** and **Reporting**. Four workers, A, B, C and D, are available. Each worker can do at most one job; each job needs exactly one worker.

The table gives **invented hours** needed for each worker–job pair. A dash means the worker is **not qualified** for that job. None of these figures describes a real Tanzanian company or worker.

| Worker | Inspection | Inventory | Transport | Reporting |
| :--- | ---: | ---: | ---: | ---: |
| A | 6 | 4 | — | 7 |
| B | 5 | 8 | 6 | 5 |
| C | — | 3 | 7 | 6 |
| D | 7 | — | 4 | 3 |

## The question

**Assign one job to each worker, respecting qualifications, so that the total number of worker-hours is as small as possible.**

Start by proposing an assignment yourself. Then ask:

- Is your assignment *feasible*? Is every job assigned exactly once, and can each worker do the selected job?
- Can you demonstrate that your assignment is *optimal*, rather than merely reasonable?
- Are there multiple optimal assignments?
- What assumptions does the total-worker-hours objective make? If the four workers act **simultaneously**, would minimizing the time at which *all four jobs finish* instead give the same answer?

## A mathematical formulation

Let `x[i,j]` be 1 if worker `i` receives job `j`, and 0 otherwise. With invented completion times `c[i,j]`, the objective is

\[
\min \sum_{i=1}^{4} \sum_{j=1}^{4} c_{ij} x_{ij}.
\]

Constraints: for every worker, \(\sum_j x_{ij}=1\); for every job, \(\sum_i x_{ij}=1\); forbidden pairs have \(x_{ij}=0\); and all variables are binary. This is a small **linear assignment problem**.

## Check with Python (optional)

SciPy is already installed by the workshop's usual `uv sync --locked`. No new dependency is required. Experiment first with your own solution, then compare with:

```python
import numpy as np
from scipy.optimize import linear_sum_assignment

hours = np.array([
    [6, 4, np.inf, 7],
    [5, 8, 6, 5],
    [np.inf, 3, 7, 6],
    [7, np.inf, 4, 3],
])

workers = ["A", "B", "C", "D"]
jobs = ["Inspection", "Inventory", "Transport", "Reporting"]

rows, columns = linear_sum_assignment(hours)

for i, j in zip(rows, columns):
    print(workers[i], "→", jobs[j], ":", hours[i, j], "hours")

print("Total worker-hours:", hours[rows, columns].sum())
```

`np.inf` represents a forbidden worker–job pair. This example uses the existing one-to-one assignment solver: it **does not** model multiple jobs per worker, job order, deadlines, travel, or fairness. A solver result should still be checked for feasibility and meaningful units.

## Optional extensions

**Choose one**:

- Formulate a different objective: minimize the **longest** job duration instead of total worker-hours. Does your assignment change? How would you test it?
- Change one capability or completion time. How stable is the optimum?
- Suppose one worker is unavailable, or two jobs require the same specialist. What must change in the mathematical model?
- Ask an AI assistant to formulate the optimization problem, then independently check every variable and constraint.

**Five-minute group report:** State the optimization goal, at least one mathematical constraint, a feasible solution, an argument or computational check of optimality, and a realistic limitation of this toy model. You may use the [pandas](../../reference/pandas_cheatsheet.ipynb) and [Matplotlib](../../reference/matplotlib_cheatsheet.ipynb) references if they help, but **no Jupyter notebook is required**.

This is a **short, optional backup challenge**, not a third major teaching project or a substitute for industry-supplied problems.

*Teaching text CC BY 4.0 · Code example MIT · All numbers and roles invented.*
