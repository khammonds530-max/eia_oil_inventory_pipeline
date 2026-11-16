
"""Build tasks for the EIA crude oil inventory pipeline."""

import subprocess
import sys
from pathlib import Path


def task_pull_eia():
    """Download EIA data and generate the derived inventory dataframe."""
    output = Path("_data/eia_crude_oil_inventories.csv")

    return {
        "actions": [
            [sys.executable, "src/pull_eia.py"],
        ],
        "file_dep": [
            "src/pull_eia.py",
            "src/settings.py",
        ],
        "targets": [str(output)],
        "clean": True,
    }
