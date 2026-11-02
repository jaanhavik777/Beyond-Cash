"""Rebuild data/clean/*.csv from data/raw/*. Owner: Amrit.

Output columns are fixed by CONTRACT.md. TODO: fill in the loaders once the
RBI and NPCI files are in data/raw/.
"""
from pathlib import Path
import re
import calendar

import pandas as pd
from openpyxl import load_workbook


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw"
CLEAN_DIR = BASE_DIR / "clean"

START_DATE = pd.Timestamp("2023-04-01")
END_DATE = pd.Timestamp("2025-03-01")

MONTHS = {
    name.lower(): number
    for number, name in enumerate(calendar.month_name)
    if name
}

PAYMENT_METHODS = [
    "UPI",
    "IMPS",
    "NEFT",
    "RTGS",
    "Debit Card",
    "Credit Card",
    "NACH",
]


# ============================================================
# GENERAL HELPERS
# ============================================================

def normalize_text(value):
    """Normalize text from Excel cells."""

    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value)).strip().lower()


def parse_number(value):
    """Convert numeric values, including Indian comma formatting."""

    if value is None:
        raise ValueError("Encountered an empty numeric value.")

    if isinstance(value, (int, float)):
        return float(value)

    cleaned = str(value).replace(",", "").strip()

    return float(cleaned)


def get_month_date(sheet_title):
    """Extract month and year from an RBI worksheet title."""

    text = normalize_text(sheet_title)

    match = re.search(
        r"(january|february|march|april|may|june|july|"
        r"august|september|october|november|december)"
        r"[\s-]+(\d{4})",
        text,
    )

    if not match:
        raise ValueError(
            f"Could not identify month/year from sheet: {sheet_title}"
        )

    month = MONTHS[match.group(1)]
    year = int(match.group(2))

    return pd.Timestamp(
        year=year,
        month=month,
        day=1,
    )


def find_header_columns(sheet):
    """Identify the monthly volume and value columns."""

    volume_col = None
    value_col = None

    for row in sheet.iter_rows():
        for cell in row:
            text = normalize_text(cell.value)

            if text == "volume (lakh)":
                volume_col = cell.column

            elif text.startswith("value"):
                value_col = cell.column

        if volume_col and value_col:
            break

    if volume_col is None or value_col is None:
        raise ValueError(
            f"Could not find Volume/Value headers in {sheet.title}"
        )

    # The monthly observation is the fourth column
    # in each section: FY total, previous year,
    # current year, latest month.

    return volume_col + 3, value_col + 3


def find_row(sheet, pattern):
    """Find the first matching transaction row."""

    regex = re.compile(pattern, re.IGNORECASE)

    matches = []

    for row in sheet.iter_rows():
        for cell in row:
            text = normalize_text(cell.value)

            if regex.search(text):
                matches.append(cell.row)
                break

    if not matches:
        raise ValueError(
            f"No matching row for {pattern!r} "
            f"in {sheet.title}"
        )

    if len(matches) > 1:
        print(
            f"  NOTE: Multiple matches for {pattern!r} "
            f"in {sheet.title}: {matches}. "
            f"Using first occurrence: row {matches[0]}"
        )

    return matches[0]


def get_numeric_value(sheet, row, col):
    """Read and validate a numeric RBI cell."""

    value = sheet.cell(
        row=row,
        column=col,
    ).value

    if value is None:
        raise ValueError(
            f"Missing value in {sheet.title}, "
            f"cell {sheet.cell(row=row, column=col).coordinate}"
        )

    return parse_number(value)


# ============================================================
# RBI DATA EXTRACTION
# ============================================================

def extract_rbi_workbook(file):
    """Extract six non-UPI payment methods from one RBI workbook."""

    workbook = load_workbook(
        file,
        data_only=True,
    )

    sheet = workbook.active

    try:
        date = get_month_date(sheet.title)

        if not START_DATE <= date <= END_DATE:
            return []

        volume_col, value_col = find_header_columns(sheet)

        row_patterns = {
            "RTGS": r"^\d+\s+credit transfers\s*-\s*rtgs$",
            "IMPS": r"^\d+\.\d+\s+imps$",
            "NACH_CREDIT": r"^\d+\.\d+\s+nach cr",
            "NEFT": r"^\d+\.\d+\s+neft$",
            "NACH_DEBIT": r"^\d+\.\d+\s+nach dr",
            "Credit Card": r"^\d+\.\d+\s+credit cards?$",
            "Debit Card": r"^\d+\.\d+\s+debit cards?$",
        }

        extracted = {}

        for method, pattern in row_patterns.items():

            row = find_row(
                sheet,
                pattern,
            )

            volume_lakh = get_numeric_value(
                sheet,
                row,
                volume_col,
            )

            value_cr = get_numeric_value(
                sheet,
                row,
                value_col,
            )

            # RBI volume is in lakh.
            # Convert lakh to million by dividing by 10.

            extracted[method] = {
                "volume_mn": volume_lakh / 10,
                "value_cr": value_cr,
            }

        # Combine NACH Credit and NACH Debit.

        extracted["NACH"] = {
            "volume_mn": (
                extracted["NACH_CREDIT"]["volume_mn"]
                + extracted["NACH_DEBIT"]["volume_mn"]
            ),
            "value_cr": (
                extracted["NACH_CREDIT"]["value_cr"]
                + extracted["NACH_DEBIT"]["value_cr"]
            ),
        }

        records = []

        methods = [
            "RTGS",
            "IMPS",
            "NEFT",
            "Credit Card",
            "Debit Card",
            "NACH",
        ]

        for method in methods:

            records.append({
                "date": date,
                "payment_method": method,
                "volume_mn": extracted[method]["volume_mn"],
                "value_cr": extracted[method]["value_cr"],
            })

        return records

    finally:
        workbook.close()


def extract_all_rbi():
    """Extract monthly data from all RBI workbooks."""

    files = sorted(
        file
        for file in RAW_DIR.glob("*.XLSX")
        if file.name.startswith(("PAYMENTSYSTEM", "PSI"))
    )

    if len(files) != 24:
        raise ValueError(
            f"Expected 24 RBI workbooks, found {len(files)}"
        )

    records = []

    for file in files:

        print(f"Reading RBI: {file.name}")

        records.extend(
            extract_rbi_workbook(file)
        )

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("No RBI records were extracted.")

    return df


# ============================================================
# NPCI UPI DATA EXTRACTION
# ============================================================

def extract_all_npci():
    """Extract monthly UPI statistics from NPCI workbooks."""

    files = sorted(
        RAW_DIR.glob("Product-Statistics-UPI-*.xlsx")
    )

    if len(files) != 2:
        raise ValueError(
            f"Expected 2 NPCI UPI workbooks, found {len(files)}"
        )

    records = []

    for file in files:

        print(f"Reading NPCI: {file.name}")

        workbook = load_workbook(
            file,
            data_only=True,
        )

        try:
            if "Product Statistics" not in workbook.sheetnames:
                raise ValueError(
                    f"Product Statistics sheet missing in {file.name}"
                )

            sheet = workbook["Product Statistics"]

            headers = {
                normalize_text(sheet.cell(1, col).value): col
                for col in range(1, sheet.max_column + 1)
            }

            required_columns = {
                "month",
                "no. of banks live on upi",
                "volume (in mn.)",
                "value (in cr.)",
            }

            missing = required_columns - set(headers)

            if missing:
                raise ValueError(
                    f"Missing NPCI columns in {file.name}: {missing}"
                )

            for row in range(2, sheet.max_row + 1):

                month_text = sheet.cell(
                    row,
                    headers["month"],
                ).value

                if not month_text:
                    continue

                date = pd.to_datetime(
                    month_text,
                    errors="coerce",
                )

                if pd.isna(date):
                    continue

                date = pd.Timestamp(
                    year=date.year,
                    month=date.month,
                    day=1,
                )

                if not START_DATE <= date <= END_DATE:
                    continue

                banks_live = parse_number(
                    sheet.cell(
                        row,
                        headers["no. of banks live on upi"],
                    ).value
                )

                volume_mn = parse_number(
                    sheet.cell(
                        row,
                        headers["volume (in mn.)"],
                    ).value
                )

                value_cr = parse_number(
                    sheet.cell(
                        row,
                        headers["value (in cr.)"],
                    ).value
                )

                if volume_mn <= 0:
                    raise ValueError(
                        f"Invalid UPI volume for {date.date()}"
                    )

                avg_ticket = (
                    value_cr * 1e7
                    / (volume_mn * 1e6)
                )

                records.append({
                    "date": date,
                    "banks_live": banks_live,
                    "volume_mn": volume_mn,
                    "value_cr": value_cr,
                    "avg_ticket_inr": avg_ticket,
                })

        finally:
            workbook.close()

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError("No NPCI UPI records were extracted.")

    return df


# ============================================================
# DATE DIMENSION
# ============================================================

def create_date_dimension():
    """Create monthly date dimension using Indian financial years."""

    dates = pd.date_range(
        START_DATE,
        END_DATE,
        freq="MS",
    )

    records = []

    for date in dates:

        if date.month >= 4:
            fy_start = date.year
            quarter = ((date.month - 4) // 3) + 1

        else:
            fy_start = date.year - 1
            quarter = ((date.month + 8) // 3) + 1

        records.append({
            "date": date,
            "year": date.year,
            "fy": (
                f"FY{fy_start}-{str(fy_start + 1)[-2:]}"
            ),
            "quarter": f"Q{quarter}",
            "month_num": date.month,
            "month_name": date.strftime("%B"),
        })

    return pd.DataFrame(records)


# ============================================================
# VALIDATION
# ============================================================

def validate_data(fact, upi, dates):
    """Validate completeness, uniqueness and numeric values."""

    expected_dates = set(dates["date"])
    expected_methods = set(PAYMENT_METHODS)

    # Check duplicate fact records.

    if fact.duplicated(
        subset=["date", "payment_method"]
    ).any():

        raise ValueError(
            "Duplicate date/payment-method records found."
        )

    # Check date coverage.

    actual_dates = set(fact["date"])

    if actual_dates != expected_dates:

        raise ValueError(
            "Fact table does not cover the expected 24 months."
        )

    # Check payment methods for every month.

    for date in expected_dates:

        methods = set(
            fact.loc[
                fact["date"] == date,
                "payment_method",
            ]
        )

        if methods != expected_methods:

            raise ValueError(
                f"Incorrect payment methods for "
                f"{date.date()}: {methods}"
            )

    # Check expected record counts.

    if len(fact) != 168:

        raise ValueError(
            f"Expected 168 fact records, found {len(fact)}"
        )

    if len(upi) != 24:

        raise ValueError(
            f"Expected 24 UPI records, found {len(upi)}"
        )

    if len(dates) != 24:

        raise ValueError(
            f"Expected 24 date records, found {len(dates)}"
        )

    # Check missing and negative values.

    numeric_columns = [
        "volume_mn",
        "value_cr",
    ]

    if fact[numeric_columns].isna().any().any():
        raise ValueError("Missing values found in fact table.")

    if (fact[numeric_columns] < 0).any().any():
        raise ValueError("Negative values found in fact table.")

    upi_numeric_columns = [
        "banks_live",
        "volume_mn",
        "value_cr",
        "avg_ticket_inr",
    ]

    if upi[upi_numeric_columns].isna().any().any():
        raise ValueError("Missing values found in UPI detail.")

    if (upi[upi_numeric_columns] < 0).any().any():
        raise ValueError("Negative values found in UPI detail.")

    print("\n========== VALIDATION PASSED ==========")

    print("Months covered: 24")
    print("Payment methods: 7")
    print("Fact records: 168")
    print("UPI detail records: 24")
    print("Date dimension records: 24")
    print("Duplicate records: 0")
    print("Missing numeric values: 0")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():

    CLEAN_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("\n========== RBI EXTRACTION ==========")

    rbi = extract_all_rbi()

    print("\n========== NPCI EXTRACTION ==========")

    upi = extract_all_npci()

    # Use NPCI as the UPI source in the fact table.

    upi_fact = upi[[
        "date",
        "volume_mn",
        "value_cr",
    ]].copy()

    upi_fact["payment_method"] = "UPI"

    # Combine RBI payment methods and NPCI UPI.

    fact = pd.concat(
        [
            rbi,
            upi_fact,
        ],
        ignore_index=True,
    )

    fact = fact[[
        "date",
        "payment_method",
        "volume_mn",
        "value_cr",
    ]]

    fact["date"] = pd.to_datetime(
        fact["date"]
    )

    fact = fact.sort_values(
        ["date", "payment_method"]
    ).reset_index(drop=True)

    # Generate date dimension.

    dates = create_date_dimension()

    upi = upi.sort_values(
        "date"
    ).reset_index(drop=True)

    # Validate before writing output files.

    validate_data(
        fact,
        upi,
        dates,
    )

    # Write final CSVs.

    fact.to_csv(
        CLEAN_DIR / "fact_payments_monthly.csv",
        index=False,
        date_format="%Y-%m-%d",
    )

    upi.to_csv(
        CLEAN_DIR / "upi_monthly_detail.csv",
        index=False,
        date_format="%Y-%m-%d",
    )

    dates.to_csv(
        CLEAN_DIR / "dim_date.csv",
        index=False,
        date_format="%Y-%m-%d",
    )

    print("\n========== OUTPUTS CREATED ==========")

    print("data/clean/fact_payments_monthly.csv")
    print("data/clean/upi_monthly_detail.csv")
    print("data/clean/dim_date.csv")

    print("\n========== FACT TABLE PREVIEW ==========")

    print(
        fact.head(10).to_string(index=False)
    )

    print("\n========== UPI DETAIL PREVIEW ==========")

    print(
        upi.head(5).to_string(index=False)
    )


if __name__ == "__main__":
    main()