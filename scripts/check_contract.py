"""Check CSVs against CONTRACT.md. Usage: python scripts/check_contract.py [data/sample | data/clean] [exports]
Exits non-zero on any failure, so it can run in CI or before a push."""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SPEC = {
    "fact_payments_monthly.csv": ["date", "payment_method", "volume_mn", "value_cr"],
    "upi_monthly_detail.csv": ["date", "banks_live", "volume_mn", "value_cr", "avg_ticket_inr"],
    "dim_date.csv": ["date", "year", "fy", "quarter", "month_num", "month_name"],
    "eda_metrics.csv": ["date", "payment_method", "mom_vol_pct", "yoy_vol_pct", "yoy_val_pct",
                        "share_vol_pct", "share_val_pct", "avg_ticket_inr", "is_anomaly",
                        "anomaly_reason", "trend_label"],
    "key_insights.csv": ["order", "stage", "headline", "detail", "metric_value", "metric_label"],
}
METHODS = {"UPI", "IMPS", "NEFT", "RTGS", "Debit Card", "Credit Card", "NACH", "Other"}
STAGES = {"hook", "buildup", "insight", "conclusion"}
errors = []

def err(f, msg): errors.append(f"{f}: {msg}")

def check(path):
    name = path.name
    df = pd.read_csv(path)
    if list(df.columns) != SPEC[name]:
        err(name, f"columns {list(df.columns)} != {SPEC[name]}"); return
    if "date" in df:
        d = pd.to_datetime(df["date"], errors="coerce")
        if d.isna().any(): err(name, "unparseable date")
        elif not (d.dt.day == 1).all(): err(name, "dates must be first of month")
    if name == "fact_payments_monthly.csv":
        if df.duplicated(["date", "payment_method"]).any(): err(name, "duplicate date/method rows")
        if not set(df.payment_method) <= METHODS: err(name, f"unknown methods {set(df.payment_method)-METHODS}")
        if "UPI" not in set(df.payment_method): err(name, "no UPI rows")
        if (df[["volume_mn", "value_cr"]] < 0).any().any(): err(name, "negative values")
    if name == "upi_monthly_detail.csv":
        calc = df.value_cr * 1e7 / (df.volume_mn * 1e6)
        if ((calc - df.avg_ticket_inr).abs() > 0.5).any(): err(name, "avg_ticket_inr does not match value/volume")
        if df.date.duplicated().any(): err(name, "duplicate months")
    if name == "dim_date.csv":
        if not df.quarter.isin(["Q1", "Q2", "Q3", "Q4"]).all(): err(name, "bad quarter")
    if name == "eda_metrics.csv":
        if not df.is_anomaly.isin([0, 1]).all(): err(name, "is_anomaly must be 0/1")
    if name == "key_insights.csv":
        if not set(df.stage) <= STAGES: err(name, f"stage must be one of {STAGES}")
        if not STAGES <= set(df.stage): err(name, f"missing stages {STAGES - set(df.stage)}")

def main():
    dirs = [ROOT / a for a in sys.argv[1:]] or [ROOT / "data/clean", ROOT / "exports"]
    found = 0
    for d in dirs:
        for f in SPEC:
            if (d / f).exists():
                found += 1; check(d / f); print("checked", (d / f).relative_to(ROOT))
    if not found: errors.append("no contract files found in " + ", ".join(map(str, dirs)))
    for e in errors: print("FAIL", e)
    print("OK" if not errors else f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)

main()
