# SPDX-License-Identifier: MIT
"""Connect notebooks in this folder to the repository's helper modules.

For students: just write `import bootstrap` at the beginning of a notebook
stored directly in `notebooks/`. The path setup belongs here, not in exercises.
"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
