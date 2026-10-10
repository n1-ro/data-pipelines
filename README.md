# Data Pipelines

A small, dependency-light toolkit for cleaning and splitting tabular data at scale — the kind of repetitive ETL work that usually eats hours of manual spreadsheet effort.

Pure-Python, no external runtime beyond the standard library, with clear CLI entry points so it composes into cron jobs or CI. Includes a fast, memory-conscious deduplicator that can handle multi-hundred-thousand-row CSV files without loading everything twice.

## What it does

- **clean** — dynamic column detection, quote/whitespace trimming, name normalization, and blocked-record filtering
- **dedupe** — exact and phone-keyed deduplication across one or many source files, keeping the highest-quality row
- **split** — deterministic partitioning of a master file into N balanced outputs (or capped families) with Excel-ready (quote-free) output
- **report** — per-run summary (rows read, deduped, kept, output sizes)

## Usage

```bash
python -m pipelines.clean input.csv --out cleaned.csv
python -m pipelines.dedupe cleaned.csv --against processed/*.csv --out deduped.csv
python -m pipelines.split deduped.csv --parts 4 --cap 15000 --out out/
```

## Structure

```
pipelines/
  __init__.py
  clean.py       # column detection + normalization
  dedupe.py      # exact + phone-keyed dedupe
  split.py       # balanced / capped partitioning
  report.py      # run summaries
tests/
  test_clean.py
  test_dedupe.py
  test_split.py
```

> All sample data under `samples/` is randomly generated. No real records.
