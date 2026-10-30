# Data contract (frozen after kickoff)

Changing a column name or file name needs a message in the group chat first, then an edit here.

## From Amrit (`data/clean/`, sample copies in `data/sample/`)
**fact_payments_monthly.csv**
| column | meaning |
|---|---|
| date | first day of month, YYYY-MM-DD |
| payment_method | UPI, IMPS, NEFT, RTGS, Debit Card, Credit Card, NACH, Other |
| volume_mn | transactions, millions |
| value_cr | value, ₹ crore |

**upi_monthly_detail.csv**: `date, banks_live, volume_mn, value_cr, avg_ticket_inr` where `avg_ticket_inr = value_cr*1e7 / (volume_mn*1e6)`

**dim_date.csv**: `date, year, fy (e.g. FY2023-24), quarter (Q1..Q4), month_num, month_name`. Financial year runs April to March.

## From Krishna (`exports/`)
**eda_metrics.csv**: `date, payment_method, mom_vol_pct, yoy_vol_pct, yoy_val_pct, share_vol_pct, share_val_pct, avg_ticket_inr, is_anomaly, anomaly_reason, trend_label`

**key_insights.csv**: `order, stage (hook|buildup|insight|conclusion), headline, detail, metric_value, metric_label`

## Shared Power BI measure names (identical in every .pbix)
`[Total Volume (Mn)]`, `[Total Value (Cr)]`, `[Avg Ticket (₹)]`, `[UPI Share % (Volume)]`, `[UPI Share % (Value)]`, `[YoY Volume %]`. Extra measures are prefixed `x_`.

## Versions
`v0` = sample data, `v1` = real data, `v2` = final. Announce each new version in the group chat.
