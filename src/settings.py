
"""Configuration for the EIA crude oil inventory pipeline."""

from datetime import date

# Fixed cutoff date for reproducible ChartBook snapshots.
END_DATE = date(2026, 11, 13)

# Retrieve historical observations for the seasonal benchmark.
START_DATE = date(2020, 1, 1)

# EIA weekly U.S. commercial crude oil inventories,
# excluding the Strategic Petroleum Reserve.
EIA_SERIES = "WCESTUS1"

# Output dataframe name.
DATAFRAME_NAME = "eia_crude_oil_inventories"
