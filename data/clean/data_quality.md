# Data Quality Report

## 1. Purpose

This report records the completeness, structural checks, extraction checks and known source differences for the cleaned datasets used in **Beyond Cash: A Data Story of UPI's Rise in India's Digital Payments**.

It describes the checks actually performed on the April 2023–March 2025 dataset. Passing these checks confirms that the pipeline produced data meeting the tested structural and reconciliation conditions; it does not independently establish that every statistic published by the source organizations is error-free.

## 2. Dataset scope

| Item | Result |
|---|---|
| Coverage | April 2023 – March 2025 |
| Frequency | Monthly |
| Months | 24 |
| Payment methods | 7 |
| Methods | UPI, IMPS, NEFT, RTGS, Debit Card, Credit Card, NACH |
| Fact table | 168 rows |
| UPI detail table | 24 rows |
| Date dimension | 24 rows |

The consolidated fact table uses NPCI values for UPI and RBI values for the other six payment methods. NACH Credit and NACH Debit are combined into one NACH category.

## 3. Structural and completeness checks

The cleaning pipeline and the standalone `validate_clean_data.py` script checked the following:

| Check | Observed result | Status |
|---|---:|---|
| Required cleaned CSV files exist | 3 of 3 | PASS |
| Required columns exist in each dataset | All checked | PASS |
| Fact table row count | 168 | PASS |
| UPI detail row count | 24 | PASS |
| Date dimension row count | 24 | PASS |
| Expected payment methods | Exactly 7 | PASS |
| Methods represented in every month | 7 per month | PASS |
| Distinct months in fact table | 24 | PASS |
| Coverage matches April 2023–March 2025 | Yes | PASS |
| Duplicate date/payment-method combinations | 0 | PASS |
| Missing numeric values in fact table | 0 | PASS |
| Negative numeric values in fact table | 0 | PASS |
| Missing numeric values in UPI detail | 0 | PASS |
| Negative numeric values in UPI detail | 0 | PASS |
| Unique monthly dates in UPI detail | Yes | PASS |
| Unique monthly dates in date dimension | Yes | PASS |
| UPI and date dimension month coverage | 24 expected months each | PASS |
| Fact and UPI dates use first day of month | Yes | PASS |

All checks implemented in `validate_clean_data.py` passed when run against the regenerated cleaned datasets.

## 4. RBI extraction verification

The RBI extraction verification script compares the cleaned values with the selected source workbook rows for three payment-method categories over 24 months:

- NACH (combined NACH Credit and NACH Debit)
- Credit Card
- Debit Card

This produced **72 comparisons** (3 categories × 24 months).

| Payment method | Number of monthly comparisons | Maximum absolute volume difference | Maximum absolute value difference |
|---|---:|---:|---:|
| NACH | 24 | 0 | 0 |
| Credit Card | 24 | 0 | 0 |
| Debit Card | 24 | 0 | 0 |

The comparison report recorded zero differences for both volume and value in all 72 checked records.

**Interpretation:** This verifies that the extraction and transformations for these selected rows reproduce the corresponding values read by the verification script from the RBI workbooks. It is not an independent audit of the RBI source data or a separate verification of every extracted method.

Output: `data/validation/rbi_extraction_comparison.csv`

## 5. RBI–NPCI UPI source comparison

UPI volume and value were compared between RBI and NPCI for all 24 months. NPCI values are used in the consolidated fact table and UPI detail table; RBI values are retained as the comparison reference.

Observed maximum absolute differences:

| Measure | Maximum absolute difference |
|---|---:|
| Transaction volume | 0.354319 million transactions |
| Transaction value | ₹0.03 crore |

Most monthly differences are small. July 2023 has the largest observed volume difference:

- RBI volume: 9,964.255681 million
- NPCI volume: 9,964.61 million
- Difference (RBI minus NPCI): approximately −0.354319 million

The comparison also records a maximum absolute value difference of ₹0.03 crore across the period.

The available comparison establishes that the two published sources differ for some months. It does **not** establish the reason for each difference. Differences may relate to source revisions, reporting or precision conventions, but these explanations have not been independently confirmed. The July 2023 difference should therefore be described as an observed source discrepancy, not automatically attributed to rounding.

Output: `data/validation/upi_source_comparison.csv`

## 6. Known data treatments and scope decisions

### 6.1 Exclusion of `Other`

The final project schema contains seven agreed payment methods and does not contain an `Other` category. The category was excluded following the team's agreed scope. It should not be interpreted as a measured zero or as evidence that no other payment activity exists.

### 6.2 NACH aggregation

RBI NACH Credit and NACH Debit rows are added together to create one monthly NACH category. The validation script checks the resulting combined volume and value against the sum of those two source rows.

### 6.3 Card transaction rows

RBI workbooks contain multiple rows with card-related labels, including rows that do not represent the intended domestic transaction measures. The extraction selects the first matching domestic transaction row for Credit Cards and Debit Cards. The repeated multiple-match notes in the extraction output are expected from the presence of other card-related rows; the selected rows were checked by the RBI extraction comparison.

### 6.4 RBI volume unit conversion

RBI transaction volume is supplied in lakh and converted to millions by dividing by 10. Transaction value is retained in ₹ crore.

### 6.5 UPI source selection

NPCI is the selected source for UPI in the consolidated datasets. RBI UPI values are used for cross-source comparison. The two sources should not be silently mixed within the same UPI series.

## 7. Limitations and interpretation cautions

1. **Source revisions:** RBI statistics may be provisional and can be revised. The retained raw workbooks represent the source files collected for this project; later source updates may differ.
2. **Cross-source differences:** RBI and NPCI UPI values are not identical in every month. The comparison report preserves the observed differences.
3. **Scope:** The dataset covers seven selected payment methods, not every possible digital or electronic payment channel.
4. **Aggregation:** The data is monthly and system-level. It does not support conclusions about individual users, merchants or transactions.
5. **Definitions over time:** Source definitions and reporting practices may change. Comparisons across months should be interpreted with the source notes in mind.
6. **No causal inference:** Descriptive changes in payment volume, value or average ticket size do not by themselves establish why those changes occurred.
7. **Validation scope:** Automated checks detect the tested structural and reconciliation issues. They cannot detect every possible source error, classification issue or methodological limitation.

## 8. Reproduction

From the repository root, with the project dependencies installed:

```bash
python data/run_pipeline.py
```

The runner executes, in order:

1. `data/clean_data.py` — regenerates the three cleaned datasets.
2. `data/validate_clean_data.py` — checks the cleaned dataset structure and expected coverage.
3. `data/verify_rbi_extraction.py` — regenerates the RBI extraction comparison.
4. `data/verify_upi_sources.py` — regenerates the RBI–NPCI UPI comparison.

The validation outputs are written under `data/validation/`.

## 9. Related files

- `data/README.md` — data sources, pipeline and methodology overview.
- `data/clean/DATA_DICTIONARY.md` — field-level definitions, units and source mapping.
- `data/clean_data.py` — extraction, transformation and output generation.
- `data/validate_clean_data.py` — structural and completeness checks.
- `data/verify_rbi_extraction.py` — selected RBI extraction reconciliation.
- `data/verify_upi_sources.py` — RBI–NPCI UPI source comparison.
- `data/validation/rbi_extraction_comparison.csv` — 72 RBI comparisons.
- `data/validation/upi_source_comparison.csv` — 24 UPI monthly comparisons.
