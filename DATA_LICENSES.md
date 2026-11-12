# Dataset licensing and provenance

| Material | License / publication rule |
| --- | --- |
| Synthetic workplace-insurance claims created by `tools/synthetic_insurance.py` | **CC0 1.0**: entirely invented establishment-year examples, claim counts and arbitrary cost units; no relation to WCF, TIRA, insurers, actual rates or Tanzanian shillings |
| Synthetic values produced by `tools/generate_synthetic_temperature.py` | **CC0 1.0**: free reuse; these are invented training values, not climate evidence |
| NASA POWER daily T2M gridded reanalysis | **Not included**. Download privately and credit the NASA LaRC POWER project; follow the [POWER referencing guide](https://power.larc.nasa.gov/docs/referencing/), documenting service/version/access date and source methodology |
| Meteostat historical station observations | **Not included**. Check current terms, original provider attributions and redistribution permission before sharing |
| Data from NBS, TMA, insurers, WCF or other industry partners | **Not included**. Keep private unless the partner explicitly authorizes particular uses and publication |
| Student projects, figures and models that may disclose third-party data | Obtain all relevant data-owner and student permissions before publication |

Meteostat's [developer license page](https://dev.meteostat.net/license)
describes its redistributed datasets as CC BY 4.0, requiring credit to Meteostat
**and its original providers**. Its [support page](https://meteostat.net/en/support)
has displayed older CC BY-NC terms. The source and provider terms should
therefore be checked **at time of redistribution**. The download script
writes to ignored local storage by default, not the public repository.

Licensing MIT code or CC BY teaching text **does not grant rights to any
third-party dataset**. No credentials, personal records, confidential model
outputs or private industry correspondence may be published here.

NASA POWER data are **model-derived grid-cell estimates**, not station measurements.
See [source methodology](https://power.larc.nasa.gov/docs/methodology/data/sources_meteorology/).
The official referencing guide requests a NASA POWER acknowledgment, service
name, version, and access date, as well as notification when sharing data
products. Data download scripts save metadata and CSV files outside Git.
