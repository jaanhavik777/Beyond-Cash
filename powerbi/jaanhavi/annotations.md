# Annotation text (fill from real data; delete a line if the data does not support it)

Source of numbers: `exports/key_insights.csv` and the measures. Never type a number you cannot trace.

| Stage | Where | Text |
|---|---|---|
| Hook | beside visual 1 | UPI grew from **[X] million** to **[Y] million** transactions a month between **[start month]** and **[end month]**. |
| Build-up | beside visual 2 | UPI's share of digital payment volume rose from **[A]%** to **[B]%**, while **[method]** fell from **[C]%** to **[D]%**. |
| Insight | on visual 3, with arrow | **[Month year]:** UPI overtook every other method in volume. |
| Insight (optional) | below visual 3 | Value share lags volume share: UPI carries **[B]%** of volume but **[E]%** of value. |
| Conclusion | bottom box | Volume grew **[P]%** a year but value **[Q]%**, so UPI is becoming the default for small, frequent payments. |

Check before using the conclusion line: it only holds if volume CAGR > value CAGR in Krishna's results. If the opposite is true, rewrite it as: "Value grew faster than volume, so average payments are getting larger."

## Anomaly note (small text under visual 1, only if Krishna flags one)
"**[Month year]** dip: **[reason from eda_metrics.anomaly_reason]**." Leave out any anomaly labelled "unexplained".
