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

files = sorted(
    file for file in RAW_DIR.glob("*.XLSX")
    if file.name.startswith(("PAYMENTSYSTEM", "PSI"))
)

fact = pd.read_csv(
    RAW_DIR.parent / "clean" / "fact_payments_monthly.csv",
    parse_dates=["date"],
)

results = []

patterns = {
    "NACH_CREDIT": r"^\d+\.\d+\s+nach cr",
    "NACH_DEBIT": r"^\d+\.\d+\s+nach dr",
    "Credit Card": r"^\d+\.\d+\s+credit cards?$",
    "Debit Card": r"^\d+\.\d+\s+debit cards?$",
}

for file in files:

    workbook = load_workbook(file, data_only=True)
    sheet = workbook.active

    try:
        date = get_month_date(sheet.title)

        if not START_DATE <= date <= END_DATE:
            continue

        volume_col, value_col = find_header_columns(sheet)

        source = {}

        for method, pattern in patterns.items():

            row = find_row(sheet, pattern)

            source[method] = {
                "volume_mn": (
                    get_numeric_value(sheet, row, volume_col) / 10
                ),
                "value_cr": get_numeric_value(
                    sheet, row, value_col
                ),
            }

        expected = {
            "NACH": {
                "volume_mn": (
                    source["NACH_CREDIT"]["volume_mn"]
                    + source["NACH_DEBIT"]["volume_mn"]
                ),
                "value_cr": (
                    source["NACH_CREDIT"]["value_cr"]
                    + source["NACH_DEBIT"]["value_cr"]
                ),
            },
            "Credit Card": source["Credit Card"],
            "Debit Card": source["Debit Card"],
        }

        for method, values in expected.items():

            actual = fact[
                (fact["date"] == date)
                & (fact["payment_method"] == method)
            ]

            if len(actual) != 1:
                raise ValueError(
                    f"Missing or duplicate {method} for {date}"
                )

            actual = actual.iloc[0]

            results.append({
                "date": date,
                "method": method,
                "volume_difference": (
                    actual["volume_mn"] - values["volume_mn"]
                ),
                "value_difference": (
                    actual["value_cr"] - values["value_cr"]
                ),
            })

    finally:
        workbook.close()


comparison = pd.DataFrame(results)

print("\n========== RBI EXTRACTION VALIDATION ==========")

print("Comparisons:", len(comparison))

print(
    comparison.groupby("method")[["volume_difference", "value_difference"]]
    .agg(["min", "max"])
    .to_string()
)

print("\nMaximum absolute differences:")

for method, group in comparison.groupby("method"):

    print(
        method,
        "| Volume:",
        group["volume_difference"].abs().max(),
        "| Value:",
        group["value_difference"].abs().max(),
    )

comparison.to_csv(
    RAW_DIR.parent / "clean" / "rbi_extraction_comparison.csv",
    index=False,
)

print("\nSaved: data/clean/rbi_extraction_comparison.csv")