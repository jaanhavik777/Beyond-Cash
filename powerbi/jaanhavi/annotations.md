# Annotation text, filled from the real `exports/eda_metrics.csv`

Data window: **Apr 2023 to Mar 2025 (24 months)**, 7 payment methods. Numbers below come from the file as of your last pull. If Krishna re-exports, re-check each one against the dashboard.

| Stage | Where | Text |
|---|---|---|
| Hook | beside visual 1 | UPI's share of digital payment transactions rose from **83.8%** (Apr 2023) to **88.7%** (Mar 2025). |
| Build-up | beside visual 2 | As UPI gained, **debit cards** fell from 2.2% to 0.6% of transactions and **IMPS** from 4.7% to 2.2%. |
| Insight | on visual 3, with the gap highlighted | UPI carries **88.7%** of transactions but only **8.2%** of value. **RTGS** carries about **71%** of value from **0.15%** of transactions. |
| Conclusion | bottom box | In Mar 2025 UPI volume was up **36%** on the year but value only **25%**, and the average UPI payment fell **15%**, from **₹1,597 to ₹1,354**. UPI is becoming the default for small, frequent payments. |

## Where each number comes from (for the demo and Q&A)
| Number | Column in `eda_metrics.csv` | Row |
|---|---|---|
| 83.8% and 88.7% | `share_vol_pct` | UPI, Apr 2023 and Mar 2025 |
| 8.3% and 8.2% | `share_val_pct` | UPI, Apr 2023 and Mar 2025 (range 7.5% to 10.0% in between) |
| 36% and 25% | `yoy_vol_pct`, `yoy_val_pct` | UPI, Mar 2025 |
| ₹1,597 and ₹1,354 | `avg_ticket_inr` | UPI, Apr 2023 and Mar 2025 |
| Debit 2.2% to 0.6%, IMPS 4.7% to 2.2% | `share_vol_pct` | Apr 2023 and Mar 2025 |
| RTGS about 71% value, 0.15% volume | `share_val_pct`, `share_vol_pct` | RTGS, Mar 2025 |

## Say this on the slide and in the paper
- Shares are of the **7 methods in the dataset** (UPI, IMPS, NEFT, RTGS, debit card, credit card, NACH), not of all payments. Write "share of the payment methods covered".
- The data window is **24 months**; year-on-year figures only exist from Apr 2024.
- No anomalies were flagged (`is_anomaly` is False), so there is no anomaly note on the dashboard. Do not mention COVID-19.
- "Becoming the default for small, frequent payments" is an interpretation of volume growing faster than value and the falling average ticket. It shows association, not cause.
