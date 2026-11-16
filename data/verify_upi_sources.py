from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

from clean_data import (
    RAW_DIR,
    START_DATE,
    END_DATE,
    get_month_date,
    find_header_columns,
    find_row,
    get_numeric_value,
)


# Load cleaned NPCI UPI dataset
npci = pd.read_csv(
    RAW_DIR.parent / "clean" / "upi_monthly_detail.csv",
    parse_dates=["date"],
)

results = []

# Identify RBI monthly workbooks
files = sorted(
    file
    for file in RAW_DIR.glob("*.XLSX")
    if file.name.startswith(("PAYMENTSYSTEM", "PSI"))
)

# Compare RBI UPI figures against NPCI figures
for file in files:
    workbook = load_workbook(file, data_only=True)
    sheet = workbook.active

    try:
        date = get_month_date(sheet.title)

        if not START_DATE <= date <= END_DATE:
            continue

        volume_col, value_col = find_header_columns(sheet)

        upi_row = find_row(
            sheet,
            r"^\d+\.\d+\s+upi\b",
        )

        # RBI volume is reported in lakh; convert to million
        rbi_volume = (
            get_numeric_value(sheet, upi_row, volume_col) / 10
        )

        rbi_value = get_numeric_value(
            sheet, upi_row, value_col
        )

        npci_row = npci[npci["date"] == date]

        if len(npci_row) != 1:
            raise ValueError(
                f"NPCI record missing or duplicated for {date}"
            )

        npci_volume = npci_row.iloc[0]["volume_mn"]
        npci_value = npci_row.iloc[0]["value_cr"]

        results.append({
            "date": date,
            "rbi_volume_mn": rbi_volume,
            "npci_volume_mn": npci_volume,
            "volume_difference": rbi_volume - npci_volume,
            "rbi_value_cr": rbi_value,
            "npci_value_cr": npci_value,
            "value_difference": rbi_value - npci_value,
        })

    finally:
        workbook.close()


# Create and display comparison report
comparison = pd.DataFrame(results).sort_values("date")

print("\n========== RBI vs NPCI UPI COMPARISON ==========")
print(comparison.to_string(index=False))

print("\n========== MAXIMUM DIFFERENCES ==========")

print(
    "Volume difference:",
    comparison["volume_difference"].abs().max()
)

print(
    "Value difference:",
    comparison["value_difference"].abs().max()
)


# Save validation report
validation_dir = RAW_DIR.parent / "validation"
validation_dir.mkdir(parents=True, exist_ok=True)

comparison.to_csv(
    validation_dir / "upi_source_comparison.csv",
    index=False,
)

print(
    "\nComparison saved to "
    "data/validation/upi_source_comparison.csv"
)