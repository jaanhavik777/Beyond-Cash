from pathlib import Path
import pandas as pd

from clean_data import (
    RAW_DIR,
    START_DATE,
    END_DATE,
    get_month_date,
    find_header_columns,
    find_row,
    get_numeric_value,
)

from openpyxl import load_workbook


# Load NPCI UPI data
npci = pd.read_csv(
    RAW_DIR.parent / "clean" / "upi_monthly_detail.csv",
    parse_dates=["date"],
)

results = []

files = sorted(
    file
    for file in RAW_DIR.glob("*.XLSX")
    if file.name.startswith(("PAYMENTSYSTEM", "PSI"))
)

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

comparison.to_csv(
    RAW_DIR.parent / "clean" / "upi_source_comparison.csv",
    index=False,
)

print("\nComparison saved to data/clean/upi_source_comparison.csv")