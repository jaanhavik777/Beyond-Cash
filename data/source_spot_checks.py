"""Traceable source-level spot checks for selected RBI and NPCI months."""

from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

from clean_data import (
    RAW_DIR,
    CLEAN_DIR,
    extract_rbi_workbook,
    extract_all_npci,
    get_month_date,
)

VALIDATION_DIR = Path(__file__).resolve().parent / "validation"

CHECK_MONTHS = [
    "2023-04-01",
    "2023-07-01",
    "2024-03-01",
    "2025-03-01",
]

RBI_METHODS = [
    "RTGS",
    "IMPS",
    "NEFT",
    "Credit Card",
    "Debit Card",
    "NACH",
]


def find_rbi_sources():
    """Map each RBI workbook to its reporting month."""

    sources = {}

    files = sorted(
        file
        for file in RAW_DIR.glob("*.XLSX")
        if file.name.startswith(("PAYMENTSYSTEM", "PSI"))
    )

    for file in files:
        workbook = load_workbook(file, read_only=True, data_only=True)

        try:
            date = get_month_date(workbook.active.title)
            sources[date.strftime("%Y-%m-%d")] = file
        finally:
            workbook.close()

    return sources


def compare_values(
    date,
    method,
    source_type,
    source_file,
    source_volume,
    source_value,
    clean_row,
):
    """Create one source-versus-clean comparison."""

    clean_volume = float(clean_row["volume_mn"])
    clean_value = float(clean_row["value_cr"])

    volume_diff = source_volume - clean_volume
    value_diff = source_value - clean_value

    tolerance = 1e-8

    volume_match = abs(volume_diff) <= tolerance
    value_match = abs(value_diff) <= tolerance

    return {
        "date": date,
        "payment_method": method,
        "source_type": source_type,
        "source_file": source_file,
        "source_volume_mn": source_volume,
        "clean_volume_mn": clean_volume,
        "volume_difference": volume_diff,
        "source_value_cr": source_value,
        "clean_value_cr": clean_value,
        "value_difference": value_diff,
        "volume_match": volume_match,
        "value_match": value_match,
        "status": "PASS" if volume_match and value_match else "REVIEW",
    }


def main():
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    clean = pd.read_csv(CLEAN_DIR / "fact_payments_monthly.csv")
    clean["date"] = pd.to_datetime(clean["date"])

    rbi_sources = find_rbi_sources()
    npci = extract_all_npci()
    npci["date"] = pd.to_datetime(npci["date"])

    records = []

    for month in CHECK_MONTHS:
        date = pd.Timestamp(month)

        print(f"\nChecking {month}")

        clean_month = clean[clean["date"] == date]

        if len(clean_month) != 7:
            raise ValueError(
                f"Expected 7 cleaned payment methods for {month}"
            )

        # -------------------------------
        # RBI source checks
        # -------------------------------

        if month not in rbi_sources:
            raise FileNotFoundError(
                f"No RBI workbook found for {month}"
            )

        rbi_file = rbi_sources[month]

        rbi_records = extract_rbi_workbook(rbi_file)

        rbi_month = {
            row["payment_method"]: row
            for row in rbi_records
        }

        for method in RBI_METHODS:
            source_row = rbi_month[method]

            clean_row = clean_month[
                clean_month["payment_method"] == method
            ].iloc[0]

            records.append(
                compare_values(
                    month,
                    method,
                    "RBI",
                    rbi_file.name,
                    float(source_row["volume_mn"]),
                    float(source_row["value_cr"]),
                    clean_row,
                )
            )

        # -------------------------------
        # NPCI UPI source check
        # -------------------------------

        npci_month = npci[npci["date"] == date]

        if len(npci_month) != 1:
            raise ValueError(
                f"Expected one NPCI UPI record for {month}"
            )

        npci_row = npci_month.iloc[0]
        clean_upi = clean_month[
            clean_month["payment_method"] == "UPI"
        ].iloc[0]

        # Identify the NPCI workbook by financial year.
        npci_filename = (
            "Product-Statistics-UPI-Product-statistics-upi-2023-24-Monthly.xlsx"
            if date < pd.Timestamp("2024-04-01")
            else "Product-Statistics-UPI-Product-statistics-upi-2024-25-Monthly.xlsx"
        )

        records.append(
            compare_values(
                month,
                "UPI",
                "NPCI",
                npci_filename,
                float(npci_row["volume_mn"]),
                float(npci_row["value_cr"]),
                clean_upi,
            )
        )

    report = pd.DataFrame(records)

    output_file = (
        VALIDATION_DIR / "source_level_spot_checks.csv"
    )

    report.to_csv(output_file, index=False)

    print("\n" + "=" * 65)
    print("SOURCE-LEVEL SPOT CHECK SUMMARY")
    print("=" * 65)

    print(f"Months checked: {len(CHECK_MONTHS)}")
    print(f"Total comparisons: {len(report)}")
    print(f"Passed: {(report['status'] == 'PASS').sum()}")
    print(f"Require review: {(report['status'] == 'REVIEW').sum()}")

    print("\nResults by month:")
    print(
        report.groupby(["date", "status"])
        .size()
        .unstack(fill_value=0)
        .to_string()
    )

    print("\nResults by source:")
    print(
        report.groupby(["source_type", "status"])
        .size()
        .unstack(fill_value=0)
        .to_string()
    )

    print(f"\nReport saved to: {output_file}")

    if (report["status"] == "REVIEW").any():
        print("\nWARNING: Some comparisons need review.")
    else:
        print("\nAll source-level spot checks passed.")


if __name__ == "__main__":
    main()
