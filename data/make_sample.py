"""Writes SYNTHETIC sample files to data/sample/. Numbers are made up; columns match CONTRACT.md."""
from pathlib import Path
import numpy as np, pandas as pd
import importlib.util

out = Path(__file__).resolve().parent / "sample"
out.mkdir(exist_ok=True)
rng = np.random.default_rng(7)
dates = pd.date_range("2023-04-01", periods=24, freq="MS")
t = np.arange(24)

base = {"UPI": (8000, 0.035, 1500), "IMPS": (500, 0.01, 1800),
        "NEFT": (400, 0.005, 33000), "Debit Card": (350, -0.005, 1800)}
rows = []
for m, (v0, g, tick) in base.items():
    vol = v0 * (1 + g) ** t * rng.normal(1, 0.015, 24)
    val = vol * tick * rng.normal(1, 0.01, 24) / 10  # ₹ crore (illustrative)
    rows += [dict(date=d.date(), payment_method=m, volume_mn=round(a, 2), value_cr=round(b, 2))
             for d, a, b in zip(dates, vol, val)]
fact = pd.DataFrame(rows).sort_values(["date", "payment_method"])
fact.to_csv(out / "fact_payments_monthly.csv", index=False)

u = fact[fact.payment_method == "UPI"].copy()
det = pd.DataFrame({"date": u.date, "banks_live": (330 + t * 6).astype(int),
                    "volume_mn": u.volume_mn.values, "value_cr": u.value_cr.values})
det["avg_ticket_inr"] = (det.value_cr * 1e7 / (det.volume_mn * 1e6)).round(2)
det.to_csv(out / "upi_monthly_detail.csv", index=False)

spec = importlib.util.spec_from_file_location("cd", Path(__file__).with_name("clean_data.py"))
cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
cd.build_dim_date("2023-04-01", "2025-03-01").to_csv(out / "dim_date.csv", index=False)
print("wrote sample files to", out)
