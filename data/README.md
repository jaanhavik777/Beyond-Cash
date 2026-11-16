Data Collection and Cleaning Documentation

1. Overview

This directory contains the source datasets, cleaned datasets, synthetic sample datasets, and validation utilities used in the Beyond Cash: A Data Story of UPI’s Rise in India’s Digital Payments project.

The data pipeline prepares monthly Indian digital payment statistics for analysis and visualization.

Coverage: April 2023 – March 2025
Frequency: Monthly
Primary sources: Reserve Bank of India (RBI) and National Payments Corporation of India (NPCI).

2. Data Sources

2.1 Reserve Bank of India (RBI)

Source: RBI Database on Indian Economy – Payment System Indicators

RBI monthly Payment System Indicator workbooks provide transaction volume and value for:

* RTGS
* IMPS
* NEFT
* NACH
* Credit Cards
* Debit Cards

The original Excel workbooks are retained in data/raw/.

2.2 National Payments Corporation of India (NPCI)

Source: NPCI – UPI Product Statistics

NPCI monthly UPI statistics provide:

* Number of banks live on UPI
* Transaction volume
* Transaction value

The 2023–24 and 2024–25 monthly workbooks are retained in data/raw/.

NPCI figures are used as the primary UPI source in the final cleaned datasets. RBI UPI figures are used for cross-source validation.

3. Directory Structure

data/
├── raw/
│   ├── RBI monthly Excel workbooks
│   └── NPCI UPI monthly workbooks
│
├── clean/
│   ├── fact_payments_monthly.csv
│   ├── upi_monthly_detail.csv
│   └── dim_date.csv
│
├── sample/
│   ├── fact_payments_monthly.csv
│   ├── upi_monthly_detail.csv
│   ├── dim_date.csv
│   └── README.md
│
├── validation/
│   ├── rbi_extraction_comparison.csv
│   └── upi_source_comparison.csv
│
├── clean_data.py
├── make_sample.py
├── verify_rbi_extraction.py
└── verify_upi_sources.py

4. Cleaned Datasets

4.1 fact_payments_monthly.csv

Contains monthly transaction volume and value for seven payment methods:

* UPI
* IMPS
* NEFT
* RTGS
* Debit Card
* Credit Card
* NACH

Column	Description	Unit
date	First day of the corresponding month	YYYY-MM-DD
payment_method	Payment system or method	Category
volume_mn	Number of transactions	Millions
value_cr	Total transaction value	₹ Crore

The dataset contains 24 months × 7 payment methods = 168 records.

4.2 upi_monthly_detail.csv

Contains additional monthly UPI statistics.

Column	Description
date	First day of the corresponding month
banks_live	Number of banks live on UPI
volume_mn	UPI transaction volume in millions
value_cr	UPI transaction value in ₹ crore
avg_ticket_inr	Average transaction value in ₹

Average ticket size is calculated as:

avg_ticket_inr = (value_cr × 10,000,000) / (volume_mn × 1,000,000)

4.3 dim_date.csv

Provides calendar and Indian financial-year attributes for time-based analysis.

Column	Description
date	First day of the month
year	Calendar year
fy	Indian financial year
quarter	Financial quarter (Q1–Q4)
month_num	Numeric month
month_name	Abbreviated month name

The Indian financial year runs from April to March.

5. Data Cleaning and Transformation

The cleaning pipeline is implemented in clean_data.py.

The major transformations include:

1. Reading monthly RBI Excel workbooks and NPCI UPI workbooks.
2. Identifying the relevant transaction rows and monthly columns in RBI workbooks.
3. Extracting transaction volume and value for each payment method.
4. Converting RBI transaction volume from lakh to million by dividing by 10.
5. Combining NACH Credit and NACH Debit into one NACH category.
6. Extracting UPI volume, value, and banks-live figures from NPCI workbooks.
7. Calculating UPI average ticket size.
8. Generating the date dimension using the Indian financial-year calendar.
9. Combining the payment-method records into the final fact table.
10. Validating the resulting datasets before writing the CSV files.

The original files in data/raw/ are retained unchanged.

6. Validation

Two verification scripts are maintained.

6.1 RBI Extraction Validation

Script: verify_rbi_extraction.py

This compares extracted RBI values against the corresponding source workbook rows for:

* NACH
* Credit Card
* Debit Card

The validation covers 24 months, producing 72 comparisons.

The recorded comparison results show zero differences for the checked volume and value fields.

Output: validation/rbi_extraction_comparison.csv

6.2 UPI Cross-Source Validation

Script: verify_upi_sources.py

This compares monthly UPI volume and value extracted from RBI and NPCI sources.

The validation covers 24 months.

The two sources show very close values overall, with small differences in some months. The largest observed absolute differences are approximately:

* Volume: 0.354319 million transactions
* Value: ₹0.03 crore

The July 2023 volume difference is larger than the typical monthly differences and is retained as a source discrepancy rather than assumed to be only a rounding difference.

NPCI values are used for UPI in the final fact table.

Output: validation/upi_source_comparison.csv

7. Sample Data

The sample/ directory contains synthetic datasets generated using make_sample.py.

These datasets preserve the structure and column names of the cleaned datasets and can be used for development and visualization before real data is available.

Important: Sample values are synthetic and must not be presented as actual RBI or NPCI statistics.

8. Limitations and Notes

* RBI source data may be provisional and subject to revision.
* RBI and NPCI UPI statistics can differ slightly.
* RBI transaction-volume figures are converted from lakh to million.
* NACH Credit and NACH Debit are combined into one category.
* The cleaned dataset covers April 2023 to March 2025.
* Payment-method definitions and reporting practices may change over time.
* The dataset represents the categories selected for this project and should not be interpreted as an exhaustive representation of every digital payment instrument in India.

9. Reproducing the Pipeline

From the repository root:

pip install -r requirements.txt
python data/clean_data.py

To regenerate synthetic sample datasets:

python data/make_sample.py

To run the verification scripts:

python data/verify_rbi_extraction.py
python data/verify_upi_sources.py

The cleaning script writes the three contract datasets to data/clean/. The verification scripts generate their comparison reports in data/validation/.