# SPDX-License-Identifier: MIT
"""Invented workplace-insurance claim counts for a public teaching exercise.

Every record and number is ARTIFICIAL. This is not data supplied by WCF,
TIRA, another Tanzanian institution, or any real insurer. No individuals.
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261112
YEARS = (2021, 2022, 2023, 2024, 2025)
SECTORS = ("Construction", "Manufacturing", "Transport", "Retail", "Services")
ZONES = ("Zone A", "Zone B", "Zone C")
SYNTHETIC_MARKER = "SYNTHETIC_NOT_REAL"


def generate(n_establishments: int = 600, seed: int = SEED) -> pd.DataFrame:
    """One invented establishment-year per row, with worker-year exposure.

    The data-generating mechanism deliberately includes:
      * varying exposure, sector and zone incidence differences;
      * unobserved establishment risk shared across years (dependence);
      * nonrandom uptake of a training programme (confounding);
      * a change in baseline incidence in 2025 (distribution shift);
      * incomplete sector labels on some rows;
      * synthetic, skewed total claim costs in arbitrary accounting units.

    The modelling notebook must never treat these invented effects as facts
    about any real place, employer, intervention or industry.
    """
    if n_establishments < 20:
        raise ValueError("n_establishments must be at least 20")
    rng = np.random.default_rng(seed)
    sectors = rng.choice(SECTORS, size=n_establishments, p=[0.18, 0.23, 0.18, 0.21, 0.20])
    zones = rng.choice(ZONES, size=n_establishments, p=[0.40, 0.35, 0.25])
    workers = rng.integers(20, 350, size=n_establishments)
    latent = rng.lognormal(mean=-0.5 * 0.45**2, sigma=0.45, size=n_establishments)
    sector_rate = {"Construction": 1.8, "Manufacturing": 1.3, "Transport": 1.5,
                   "Retail": 0.65, "Services": 0.52}
    zone_rate = {"Zone A": 1.0, "Zone B": 1.12, "Zone C": 0.91}
    records: list[dict] = []
    for year in YEARS:
        for i in range(n_establishments):
            sector, zone = str(sectors[i]), str(zones[i])
            exposed_workers = int(max(10, round(workers[i] * rng.uniform(0.80, 1.22))))
            share_of_year = float(rng.uniform(0.65, 1.0))
            exposure = round(exposed_workers * share_of_year, 3)
            # Training is offered preferentially to higher-risk establishments.
            # The (hidden) establishment risk also affects programme uptake.
            log_odds = (-1.15 + 0.42 * (sector in {"Construction", "Transport"})
                        + 0.19 * (year - YEARS[0]) + 0.35 * np.log(latent[i]))
            training_probability = 1 / (1 + np.exp(-log_odds))
            programme = "Yes" if rng.random() < training_probability else "No"
            mean_count = (exposure * 0.017 * sector_rate[sector] * zone_rate[zone]
                          * latent[i] * (0.82 if programme == "Yes" else 1.0)
                          * (1.22 if year == 2025 else 1.0))
            claims_count = int(rng.poisson(mean_count))
            # Sum of i.i.d. gamma claim sizes is gamma(shape*k, scale).
            # These 'costs' are dimensionless classroom accounting units.
            severity_scale = 1100.0 * (1.45 if sector == "Construction" else 1.0)
            total_cost = (float(rng.gamma(shape=1.7 * claims_count, scale=severity_scale))
                          if claims_count else 0.0)
            records.append({
                "establishment_id": f"E{i:04d}", "year": year,
                "sector": sector if rng.random() >= 0.04 else None,
                "zone": zone, "programme": programme,
                "workers": exposed_workers, "worker_years": exposure,
                "claims_count": claims_count, "total_claim_cost_units": round(total_cost, 2),
                "dataset_status": SYNTHETIC_MARKER,
            })
    return pd.DataFrame.from_records(records)


def main() -> None:
    output = (Path(__file__).resolve().parents[1]
              / "data" / "synthetic_insurance_claims.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    generate().to_csv(output, index=False)
    print(f"Wrote {output}: ENTIRELY SYNTHETIC — NO REAL INSURANCE DATA")


if __name__ == "__main__":
    main()
