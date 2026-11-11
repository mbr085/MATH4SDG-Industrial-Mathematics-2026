# Data for the Meteostat backup

There are **no real station observations** committed to this public repository.

- The student notebook creates a deterministic **synthetic** series in memory if no real download is present. Run `uv run python tools/generate_synthetic_temperature.py` only if you want a CSV copy for offline demonstrations. This generated dataset is **artificial** and not evidence of any change in East African climate; the synthetic values are offered under CC0 1.0.
- The optional `tools/download_meteostat.py` script downloads station records to `data/private/`. These files and adjacent metadata are Git-ignored. Data quality, provider attribution, and rights must be assessed before distributing any real CSV. No missing values are filled by the script.
- Do not put NBS, TMA, insurer, WCF or other non-public partner data in the repository. Private workshop analysis does not imply permission to redistribute the inputs or derived results.

See [DATA_LICENSES.md](../DATA_LICENSES.md) and [Meteostat’s developer documentation](https://dev.meteostat.net/license).
