
# EIA Crude Oil Inventory Pipeline

A reproducible data pipeline for analyzing U.S. commercial crude oil inventories relative to their historical seasonal average.

## Data Source

- **Provider:** U.S. Energy Information Administration (EIA)
- **Dataset:** Weekly U.S. Ending Stocks of Crude Oil, Excluding SPR
- **Series:** WCESTUS1
- **Source:** https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?f=W&n=PET&s=WCESTUS1
- **API:** https://api.eia.gov/v2/petroleum/stoc/wstk/data/
- **Observation cutoff:** November 13, 2026

## Methodology

The pipeline retrieves weekly U.S. commercial crude oil inventories from January 2020 through November 13, 2026.

It calculates a five-year seasonal benchmark using observations from 2021–2025, grouped by ISO calendar week.

The output includes the latest 12 months of observations and four indicators:

- `inventories_mmbbl`: Actual inventories in millions of barrels.
- `five_year_avg_mmbbl`: Historical seasonal average in millions of barrels.
- `gap_mmbbl`: Actual inventories minus the seasonal average.
- `gap_pct`: Percentage difference from the seasonal average.

## Reproducing the Pipeline

Install dependencies:

```bash
uv sync
```

Run the pipeline:

```bash
uv run doit
```

Or run through ChartBook:

```bash
uv run chartbook trust
uv run chartbook run
```

## Output

The derived dataset is saved to:

`_data/eia_crude_oil_inventories.csv`

The dataframe is declared in `chartbook.toml` as `eia_crude_oil_inventories`.

## Research Application

This pipeline supports an exhibit examining whether U.S. commercial crude oil inventories have tightened relative to historical seasonal levels over the past year.

Prepared for FINM 32800: Data Pipelines for Quantitative Research, Autumn 2026.