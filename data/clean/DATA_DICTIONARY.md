# Data Dictionary

## Dataset overview

These cleaned monthly datasets support **Beyond Cash: A Data Story of UPI's Rise in India's Digital Payments**.

- **Coverage:** April 2023 to March 2025 (24 months).
- **Geography:** India.
- **Frequency:** Monthly.
- **Payment methods:** UPI, IMPS, NEFT, RTGS, Debit Card, Credit Card and NACH.
- **Sources:** RBI Payment System Indicators and NPCI UPI Product Statistics.

## 1. `fact_payments_monthly.csv`

**Grain:** One row per month and payment method.  
**Expected size:** 168 rows (24 months × 7 payment methods).

| Column | Data type | Unit / format | Meaning | Source |
|---|---|---|---|---|
| `date` | Date | `YYYY-MM-DD`, first day of month | Month represented by the record | RBI reporting month for six non-UPI methods; NPCI reporting month for UPI |
| `payment_method` | String / category | One of seven agreed categories | Payment instrument or system | Standardized from RBI/NPCI source labels |
| `volume_mn` | Numeric (decimal) | Million transactions | Number of transactions during the month | RBI for IMPS, NEFT, RTGS, Debit Card, Credit Card and NACH; NPCI for UPI |
| `value_cr` | Numeric (decimal) | ₹ crore | Total transaction value during the month | RBI for the six non-UPI methods; NPCI for UPI |

### Payment-method mapping

| Standardized category | Source row(s) / treatment |
|---|---|
| `UPI` | NPCI UPI Product Statistics |
| `IMPS` | RBI Payment System Indicators — IMPS |
| `NEFT` | RBI Payment System Indicators — NEFT |
| `RTGS` | RBI Payment System Indicators — Credit Transfers - RTGS |
| `Debit Card` | RBI domestic debit-card transaction row |
| `Credit Card` | RBI domestic credit-card transaction row |
| `NACH` | Sum of RBI NACH Credit (`NACH Cr`) and NACH Debit (`NACH Dr`) |

RBI reports transaction volume in lakh. The cleaning process converts lakh to million by dividing by 10. Transaction value is retained in ₹ crore.

NPCI is used as the UPI source in the consolidated fact table. RBI UPI figures are used for source comparison, rather than as the consolidated UPI values.

## 2. `upi_monthly_detail.csv`

**Grain:** One row per month.  
**Expected size:** 24 rows.

| Column | Data type | Unit / format | Meaning | Source |
|---|---|---|---|---|
| `date` | Date | `YYYY-MM-DD`, first day of month | Month represented by the record | NPCI UPI Product Statistics |
| `banks_live` | Integer (may display as decimal in CSV readers) | Number of banks | Number of banks live on UPI in that month | NPCI UPI Product Statistics |
| `volume_mn` | Numeric (decimal) | Million transactions | Monthly UPI transaction volume | NPCI UPI Product Statistics |
| `value_cr` | Numeric (decimal) | ₹ crore | Monthly UPI transaction value | NPCI UPI Product Statistics |
| `avg_ticket_inr` | Numeric (decimal) | ₹ per transaction | Average value per UPI transaction | Derived from NPCI volume and value |

Average ticket size is calculated as:

`avg_ticket_inr = (value_cr × 10,000,000) / (volume_mn × 1,000,000)`

Equivalently:

`avg_ticket_inr = value_cr × 10 / volume_mn`

This converts crore rupees to rupees and million transactions to individual transactions.

## 3. `dim_date.csv`

**Grain:** One row per month.  
**Expected size:** 24 rows.

| Column | Data type | Unit / format | Meaning | Source / derivation |
|---|---|---|---|---|
| `date` | Date | `YYYY-MM-DD`, first day of month | Month key used to relate the date dimension to the fact tables | Generated for the project coverage period |
| `year` | Integer | Calendar year | Calendar year of the month | Derived from `date` |
| `fy` | String | `FY2023-24` format | Indian financial year, April to March | Derived from `date` |
| `quarter` | String / category | `Q1` to `Q4` | Quarter within the Indian financial year | Derived from `date`; Q1 is April–June |
| `month_num` | Integer | 1–12 | Calendar month number | Derived from `date` |
| `month_name` | String | Full month name | Calendar month name | Derived from `date` |

### Indian financial-year convention

The financial year begins in April and ends in March. For example:
- April 2023 to March 2024 is `FY2023-24`.
- April 2024 to March 2025 is `FY2024-25`.

Financial-year quarters are:
- Q1: April–June
- Q2: July–September
- Q3: October–December
- Q4: January–March

## Units and interpretation

- `volume_mn` is a transaction count expressed in millions; it is not a monetary value.
- `value_cr` is transaction value expressed in crore rupees.
- `avg_ticket_inr` is average rupees per transaction.
- The records are aggregate system-level monthly data. They do not identify individual users or transactions.

## Scope notes

- The consolidated dataset contains seven payment methods. `Other` is not included in the final schema, following the team's agreed seven-method scope.
- NACH combines credit and debit transactions into one category.
- Card values refer to the selected domestic transaction rows, not card issuance counts, international transactions or broader card-use summary rows.
- Raw source files are retained separately under `data/raw/`; the cleaned CSVs are generated by the project's cleaning pipeline.
