# Demo script (about 5 minutes, one presenter, others take Q&A on their part)

| Time | Who | Say and show |
|---|---|---|
| 0:00 | Jaanhavi | The question: how has UPI's share of India's digital payments changed? Show the dashboard title. |
| 0:30 | Amrit | Data: RBI + NPCI monthly statistics, [N] months, cleaned with `clean_data.py`; show `data/clean/` and the quality note. |
| 1:15 | Krishna | EDA (Unit 1): growth rates, share, trend test, anomaly flags. Show 1 notebook output. |
| 2:00 | Jaanhavi | Narrative (Unit 2): walk Hook → Build-up → Insight → Conclusion, reading each annotation. |
| 3:30 | Kushi | Interactive (Unit 3): use the date slicer, drill Year→Quarter→Month, click a payment method to cross-filter. |
| 4:30 | Jaanhavi | Conclusion and limits. |
| 5:00 | All | Questions. |

## Likely questions
- Why UPI vs other methods? Because share change is the story; compare with IMPS, NEFT, RTGS, cards.
- How was anomaly detection done? Krishna: [rule], from `flag_anomalies()`.
- What are the limits? Aggregate monthly data; cannot split person-to-person from person-to-merchant; correlation is not causation.
- Where do the numbers come from? RBI Payment System Indicators; NPCI UPI Product Statistics.
