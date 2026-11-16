
"""Build derived weekly U.S. crude oil inventory indicators."""

from pathlib import Path

import pandas as pd

from settings import END_DATE, START_DATE, EIA_SERIES

OUTPUT_DIR = Path("_data")
OUTPUT_FILE = OUTPUT_DIR / "eia_crude_oil_inventories.csv"

# FRED distributes the EIA's WCESTUS1 weekly series.
# Official EIA API endpoint
DATA_URL = "https://api.eia.gov/v2/petroleum/stoc/wstk/data/"


def load_eia_data():
    """Download weekly commercial crude oil inventories directly from EIA."""
    import json
    from urllib.parse import urlencode
    from urllib.request import urlopen

    params = {
        "api_key": "DEMO_KEY",
        "data[0]": "value",
        "facets[series][]": EIA_SERIES,
        "start": START_DATE.isoformat(),
        "end": END_DATE.isoformat(),
        "offset": 0,
        "length": 5000,
    }

    url = f"{DATA_URL}?{urlencode(params)}"

    with urlopen(url, timeout=60) as response:
        payload = json.load(response)

    if "response" not in payload:
        raise ValueError(f"Unexpected EIA API response: {payload}")

    records = payload["response"]["data"]
    total = int(payload["response"]["total"])

    if len(records) != total:
        raise ValueError(
            f"Incomplete EIA download: received {len(records)} of {total} rows."
        )

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("No EIA observations found in the selected period.")

    df = df.rename(
        columns={
            "period": "date",
            "value": "inventories_thousand_bbl",
        }
    )

    df["date"] = pd.to_datetime(df["date"])
    df["inventories_thousand_bbl"] = pd.to_numeric(
        df["inventories_thousand_bbl"], errors="coerce"
    )

    df = df.dropna(subset=["date", "inventories_thousand_bbl"])
    df = df.sort_values("date")

    # EIA reports this series in thousands of barrels.
    df["inventories_mmbbl"] = df["inventories_thousand_bbl"] / 1000

    return df


def calculate_indicators(df):
    """Compare recent inventories with a historical seasonal benchmark."""
    df = df.copy()
    df["week"] = df["date"].dt.isocalendar().week.astype(int)

    # Use the five complete calendar years before 2026.
    historical = df[df["date"].dt.year.between(2021, 2025)]

    seasonal = (
        historical.groupby("week")["inventories_mmbbl"]
        .mean()
        .rename("five_year_avg_mmbbl")
    )

    # Keep the latest 12 months of observations.
    cutoff = pd.Timestamp(END_DATE) - pd.DateOffset(months=12)
    recent = df[df["date"] >= cutoff].copy()

    recent = recent.join(seasonal, on="week")

    if recent["five_year_avg_mmbbl"].isna().any():
        raise ValueError("Missing historical seasonal benchmark.")

    recent["gap_mmbbl"] = (
        recent["inventories_mmbbl"] - recent["five_year_avg_mmbbl"]
    )

    recent["gap_pct"] = (
        100 * recent["gap_mmbbl"] / recent["five_year_avg_mmbbl"]
    )

    return recent[
        [
            "date",
            "inventories_mmbbl",
            "five_year_avg_mmbbl",
            "gap_mmbbl",
            "gap_pct",
        ]
    ]


def main():
    df = load_eia_data()
    result = calculate_indicators(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False, float_format="%.6f")

    print(f"Saved {len(result)} observations to {OUTPUT_FILE}")
    print(result.tail().to_string(index=False))


if __name__ == "__main__":
    main()
