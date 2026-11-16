from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
CLEAN_DIR = DATA_DIR / "clean"
OUTPUT_DIR = DATA_DIR / "validation"

INPUT_FILE = CLEAN_DIR / "fact_payments_monthly.csv"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(INPUT_FILE, parse_dates=["date"])

    required = {
        "date", "payment_method", "volume_mn", "value_cr"
    }

    if not required.issubset(df.columns):
        raise ValueError("Fact table is missing required columns.")

    if df.empty or df["value_cr"].isna().any():
        raise ValueError("Fact table is empty or contains missing values.")

    # Scenario A: all payment methods, including RTGS
    monthly_total = (
        df.groupby("date")["value_cr"]
        .sum()
        .rename("total_value_including_rtgs_cr")
    )

    # Scenario B: exclude RTGS from the denominator
    without_rtgs = df[df["payment_method"] != "RTGS"].copy()

    monthly_excluding = (
        without_rtgs.groupby("date")["value_cr"]
        .sum()
        .rename("total_value_excluding_rtgs_cr")
    )

    # Monthly payment-method shares under both scenarios
    monthly = df.merge(monthly_total, on="date")
    monthly = monthly.merge(monthly_excluding, on="date")

    monthly["share_including_rtgs_pct"] = (
        monthly["value_cr"]
        / monthly["total_value_including_rtgs_cr"] * 100
    )

    monthly["share_excluding_rtgs_pct"] = (
        monthly["value_cr"]
        / monthly["total_value_excluding_rtgs_cr"] * 100
    )

    # RTGS is absent from the second scenario, so its share is undefined.
    monthly.loc[
        monthly["payment_method"] == "RTGS",
        "share_excluding_rtgs_pct"
    ] = pd.NA

    monthly["share_change_pp"] = (
        monthly["share_excluding_rtgs_pct"]
        - monthly["share_including_rtgs_pct"]
    )

    monthly_output = monthly[
        [
            "date",
            "payment_method",
            "value_cr",
            "total_value_including_rtgs_cr",
            "total_value_excluding_rtgs_cr",
            "share_including_rtgs_pct",
            "share_excluding_rtgs_pct",
            "share_change_pp",
        ]
    ].sort_values(["date", "payment_method"])

    # Aggregate all 24 months before calculating weighted shares.
    # This avoids treating a small month and a large month equally.
    totals = (
        df.groupby("payment_method")["value_cr"]
        .sum()
        .rename("total_value_cr")
        .reset_index()
    )

    grand_total = totals["total_value_cr"].sum()
    total_without_rtgs = totals.loc[
        totals["payment_method"] != "RTGS",
        "total_value_cr"
    ].sum()

    totals["share_including_rtgs_pct"] = (
        totals["total_value_cr"] / grand_total * 100
    )

    totals["share_excluding_rtgs_pct"] = pd.NA

    non_rtgs = totals["payment_method"] != "RTGS"

    totals.loc[non_rtgs, "share_excluding_rtgs_pct"] = (
        totals.loc[non_rtgs, "total_value_cr"]
        / total_without_rtgs * 100
    )

    totals["share_change_pp"] = (
        totals["share_excluding_rtgs_pct"]
        - totals["share_including_rtgs_pct"]
    )

    totals = totals.sort_values(
        "share_including_rtgs_pct",
        ascending=False
    )

    # Key summary metrics
    rtgs_value = totals.loc[
        totals["payment_method"] == "RTGS",
        "total_value_cr"
    ].iloc[0]

    upi = totals.loc[totals["payment_method"] == "UPI"].iloc[0]

    summary = pd.DataFrame([
        {
            "metric": "Total value including RTGS",
            "value": grand_total,
            "unit": "₹ crore",
        },
        {
            "metric": "Total value excluding RTGS",
            "value": total_without_rtgs,
            "unit": "₹ crore",
        },
        {
            "metric": "RTGS share of total value",
            "value": rtgs_value / grand_total * 100,
            "unit": "%",
        },
        {
            "metric": "UPI share including RTGS",
            "value": upi["share_including_rtgs_pct"],
            "unit": "%",
        },
        {
            "metric": "UPI share excluding RTGS",
            "value": upi["share_excluding_rtgs_pct"],
            "unit": "%",
        },
        {
            "metric": "Change in UPI value share",
            "value": upi["share_change_pp"],
            "unit": "percentage points",
        },
    ])

    monthly_output.to_csv(
        OUTPUT_DIR / "rtgs_monthly_sensitivity.csv",
        index=False
    )

    totals.to_csv(
        OUTPUT_DIR / "rtgs_aggregate_sensitivity.csv",
        index=False
    )

    summary.to_csv(
        OUTPUT_DIR / "rtgs_sensitivity_summary.csv",
        index=False
    )

    print("\n========== RTGS SENSITIVITY ANALYSIS ==========")

    print("\nAGGREGATE PAYMENT VALUE SHARES")
    print(
        totals.round(4).to_string(index=False)
    )

    print("\nKEY FINDINGS")
    print(
        summary.round(4).to_string(index=False)
    )

    print("\n========== OUTPUTS CREATED ==========")
    print("data/validation/rtgs_monthly_sensitivity.csv")
    print("data/validation/rtgs_aggregate_sensitivity.csv")
    print("data/validation/rtgs_sensitivity_summary.csv")


if __name__ == "__main__":
    main()
