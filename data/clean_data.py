"""Rebuild data/clean/*.csv from data/raw/*. Owner: Amrit.

Output columns are fixed by CONTRACT.md. TODO: fill in the loaders once the
RBI and NPCI files are in data/raw/.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW, CLEAN = ROOT / "raw", ROOT / "clean"


def build_dim_date(start, end):
    d = pd.DataFrame({"date": pd.date_range(start, end, freq="MS")})
    d["year"] = d.date.dt.year
    fy_start = d.date.dt.year.where(d.date.dt.month >= 4, d.date.dt.year - 1)
    d["fy"] = "FY" + fy_start.astype(str) + "-" + ((fy_start + 1) % 100).astype(str).str.zfill(2)
    d["quarter"] = "Q" + (((d.date.dt.month - 4) % 12) // 3 + 1).astype(str)  # Indian FY quarters
    d["month_num"] = d.date.dt.month
    d["month_name"] = d.date.dt.strftime("%b")
    return d


def check(fact):
    assert not fact.duplicated(["date", "payment_method"]).any(), "duplicate date/method rows"
    assert (fact[["volume_mn", "value_cr"]] >= 0).all().all(), "negative values"


if __name__ == "__main__":
    raise SystemExit("TODO: load RBI/NPCI files from data/raw and write the three contract CSVs to data/clean")
