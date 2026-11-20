"""Tests for EIA crude oil inventory calculations."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pull_eia import calculate_indicators


def test_inventory_shortfall():
    """400 vs. 500 million barrels should produce -100 and -20%."""
    # Five historical observations in the same ISO week.
    historical_dates = pd.to_datetime(
        [
            "2021-11-12",
            "2022-11-11",
            "2023-11-10",
            "2024-11-08",
            "2025-11-07",
        ]
    )

    historical = pd.DataFrame(
        {
            "date": historical_dates,
            "inventories_mmbbl": [500.0] * 5,
        }
    )

    recent = pd.DataFrame(
        {
            "date": pd.to_datetime(["2026-11-06"]),
            "inventories_mmbbl": [400.0],
        }
    )

    df = pd.concat([historical, recent], ignore_index=True)

    result = calculate_indicators(df)
    observation = result.loc[result["date"] == pd.Timestamp("2026-11-06")].iloc[0]

    assert observation["five_year_avg_mmbbl"] == pytest.approx(500.0)
    assert observation["gap_mmbbl"] == pytest.approx(-100.0)
    assert observation["gap_pct"] == pytest.approx(-20.0)
