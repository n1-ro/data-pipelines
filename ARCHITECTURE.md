# Architecture

`data-pipelines` is a pure-Python, stdlib-only ETL toolkit. No external runtime
dependencies — it composes into cron jobs or CI without a package install step.

## Pipeline stages

```
raw CSV ──► clean ──► dedupe ──► split ──► outputs
              │          │          │
              │          └─ phone/name-keyed, quality-aware
              └─ column detection + normalization + blocking
```

## Modules

| Module | Responsibility |
|---|---|
| `clean.py` | Column detection, phone/name normalization, blocked-record filtering |
| `normalize.py` | Field-level normalizers (phone, name, email, zip) |
| `validate.py` | Record validation (phone/email formats, required fields) |
| `dedupe.py` | Exact + phone-keyed dedupe, quality-aware row selection |
| `merge.py` | Multi-file merge with schema projection |
| `split.py` | Balanced / capped partitioning, deterministic shuffle |
| `report.py` | Run summaries (rows read/kept/dropped) |
| `cli.py` | `clean` and `split` command entry points |

## Design notes

- **Quality-aware dedupe** keeps the highest-quality row when keys collide
  (prefers rows with a file number and complete names).
- **Deterministic split** accepts a seed so a run is reproducible.
- **Excel-ready output** writes quote-free CSVs.

## Testing

`tests/` covers each module with pytest. Run `pytest` from the repo root.
