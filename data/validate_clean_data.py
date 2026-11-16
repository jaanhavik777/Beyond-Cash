from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent
CLEAN_DIR = DATA_DIR / "clean"

EXPECTED_METHODS = {
    "UPI",
    "IMPS",
    "NEFT",
    "RTGS",
    "Debit Card",
    "Credit Card",
    "NACH",
}

EXPECTED_MONTHS = pd.date_range(
    "2023-04-01",
    "2025-03-01",
    freq="MS",
)

FACT_COLUMNS = {
    "date", "payment_method", "volume_mn", "value_cr"
}

UPI_COLUMNS = {
    "date", "banks_live", "volume_mn",
    "value_cr", "avg_ticket_inr"
}

DATE_COLUMNS = {
    "date", "year", "fy", "quarter",
    "month_num", "month_name"
}


def check(condition, message):
    if not condition:
        raise ValueError(f"FAILED: {message}")
    print(f"PASS: {message}")


def main():
    fact_path = CLEAN_DIR / "fact_payments_monthly.csv"
    upi_path = CLEAN_DIR / "upi_monthly_detail.csv"
    date_path = CLEAN_DIR / "dim_date.csv"

    for path in [fact_path, upi_path, date_path]:
        check(path.exists(), f"{path.name} exists")

    fact = pd.read_csv(fact_path, parse_dates=["date"])
    upi = pd.read_csv(upi_path, parse_dates=["date"])
    dates = pd.read_csv(date_path, parse_dates=["date"])

    check(
        FACT_COLUMNS.issubset(fact.columns),
        "Fact table has required columns"
    )

    check(
        UPI_COLUMNS.issubset(upi.columns),
        "UPI detail table has required columns"
    )

    check(
        DATE_COLUMNS.issubset(dates.columns),
        "Date dimension has required columns"
    )

    check(
        len(fact) == 168,
        "Fact table contains 168 records"
    )

    check(
        len(upi) == 24,
        "UPI detail contains 24 records"
    )

    check(
        len(dates) == 24,
        "Date dimension contains 24 records"
    )

    check(
        set(fact["payment_method"].unique()) == EXPECTED_METHODS,
        "Fact table contains exactly seven expected payment methods"
    )

    check(
        fact.groupby("date")["payment_method"].nunique().eq(7).all(),
        "Every month contains all seven payment methods"
    )

    check(
        fact["date"].nunique() == 24,
        "Fact table covers 24 distinct months"
    )

    check(
        set(fact["date"]) == set(EXPECTED_MONTHS),
        "Fact table covers April 2023 to March 2025"
    )

    check(
        not fact.duplicated(["date", "payment_method"]).any(),
        "No duplicate date-payment method combinations"
    )

    for name, frame, columns in [
        ("Fact table", fact, ["volume_mn", "value_cr"]),
        ("UPI detail", upi, [
            "banks_live", "volume_mn",
            "value_cr", "avg_ticket_inr"
        ]),
    ]:
        check(
            frame[columns].notna().all().all(),
            f"{name} has no missing numeric values"
        )

        check(
            (frame[columns] >= 0).all().all(),
            f"{name} has no negative numeric values"
        )

    check(
        upi["date"].is_unique,
        "UPI detail has unique monthly dates"
    )

    check(
        dates["date"].is_unique,
        "Date dimension has unique monthly dates"
    )

    check(
        set(upi["date"]) == set(EXPECTED_MONTHS),
        "UPI detail covers the expected 24 months"
    )

    check(
        set(dates["date"]) == set(EXPECTED_MONTHS),
        "Date dimension covers the expected 24 months"
    )

    check(
        (fact["date"].dt.day == 1).all(),
        "Fact dates use the first day of each month"
    )

    check(
        (upi["date"].dt.day == 1).all(),
        "UPI dates use the first day of each month"
    )

    print("\nAll data validation checks passed!")
    print(f"Fact records: {len(fact)}")
    print(f"UPI detail records: {len(upi)}")
    print(f"Date dimension records: {len(dates)}")


if __name__ == "__main__":
    main()
