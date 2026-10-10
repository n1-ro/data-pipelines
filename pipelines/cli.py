"""Command-line entry points for the pipeline stages."""

from __future__ import annotations

import argparse
import sys

from .clean import clean_phone, split_full_name, iter_rows, detect_columns, clean_row
from .dedupe import dedupe, load_known_keys
from .split import split_rows, write_csv


def cmd_clean(args: argparse.Namespace) -> int:
    headers: list[str] = []
    cleaned: list[dict[str, str]] = []
    cols: dict[str, int | None] | None = None

    for row in iter_rows(args.input):
        if cols is None:
            headers = list(row.keys())
            cols = detect_columns(headers)
        out = clean_row(row, cols, headers)
        if out is not None:
            cleaned.append(out)

    write_csv(args.out, cleaned, ["first", "last", "phone", "file"])
    print(f"cleaned {len(cleaned)} rows -> {args.out}")
    return 0


def cmd_split(args: argparse.Namespace) -> int:
    rows = list(iter_rows(args.input))
    buckets = split_rows(rows, args.parts, seed=args.seed, shuffle=not args.no_shuffle)
    for i, bucket in enumerate(buckets):
        write_csv(f"{args.out}/part{i + 1}.csv", bucket, ["first", "last", "phone", "file"])
    print(f"split {len(rows)} rows into {args.parts} parts")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pipelines", description="Clean, dedupe, split tabular data")
    sub = parser.add_subparsers(dest="command", required=True)

    p_clean = sub.add_parser("clean")
    p_clean.add_argument("input")
    p_clean.add_argument("--out", default="cleaned.csv")
    p_clean.set_defaults(func=cmd_clean)

    p_split = sub.add_parser("split")
    p_split.add_argument("input")
    p_split.add_argument("--parts", type=int, required=True)
    p_split.add_argument("--out", default="out")
    p_split.add_argument("--seed", type=int, default=None)
    p_split.add_argument("--no-shuffle", action="store_true")
    p_split.set_defaults(func=cmd_split)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
