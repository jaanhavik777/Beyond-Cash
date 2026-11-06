# Jaanhavi's Power BI build guide (Unit 2: the narrative), v2 for the real data

Goal: one page that reads Hook → Build-up → Insight → Conclusion, built on the real files in `data/clean/` and `exports/`.

## 1. Load and model (20 min)
1. Home > Get data > Text/CSV. Load `data/clean/fact_payments_monthly.csv`, `upi_monthly_detail.csv`, `dim_date.csv`, and `exports/eda_metrics.csv`. Skip `key_insights.csv` unless you want it for reference. Keep the default table names.
2. In Power Query, check `date` is type **Date** in every table.
3. **Model view. Power BI will auto-create relationships. Delete every one that does not involve `dim_date`** (right-click the line > Delete). Fact tables must never connect to each other, or you get "ambiguous paths".
4. Keep exactly three relationships, each **One to many**, **Single** direction, active:
   - `dim_date[date]` → `fact_payments_monthly[date]`
   - `dim_date[date]` → `upi_monthly_detail[date]`
   - `dim_date[date]` → `eda_metrics[date]`
5. Right-click `dim_date` > **Mark as date table** > `date`.
6. View > Themes > Browse for themes > `powerbi/jaanhavi/theme.json`.
7. Create each measure in `measures.dax`. Formats: volume and value as whole number, shares, YoY and `x_UPI Share Gap` as Percentage, Avg Ticket as Decimal 0.

## 2. Page layout (16:9, 1280 x 720)
```
+--------------------------------------------------------------+
| Title: Beyond Cash: UPI's rise in India's digital payments    |
+------------------------+-----------------------------------+
| HOOK (visual 1)        | BUILD-UP (visual 2)               |
| text: hook annotation  | text: build-up annotation         |
+------------------------+-----------------------------------+
| INSIGHT (visual 3): volume share vs value share, gap marked  |
+--------------------------------------------------------------+
| CONCLUSION: one takeaway, 2-3 lines                          |
+--------------------------------------------------------------+
```
Leave room on the right for Kushi's visuals 4–5 and the slicers.

## 3. Visuals
| # | Stage | Type | Fields | Format |
|---|---|---|---|---|
| 1 | Hook | Line chart | X: `dim_date[date]`; Y: `[UPI Share % (Volume)]` | Title "UPI's share of transactions". Y axis from 80% to 90% so the rise is visible; label the first and last points (83.8%, 88.7%). |
| 2 | Build-up | 100% stacked column | X: `dim_date[date]`; values `[Total Volume (Mn)]`; legend `payment_method` | UPI in blue, others in greys. UPI will dominate; that is the point. Optionally filter out UPI in a second small multiple to show debit card and IMPS shrinking. |
| 3 | Insight | Line chart | X: `dim_date[date]`; Y: `[UPI Share % (Volume)]` and `[UPI Share % (Value)]` | Two lines, about 80 points apart. Blue for volume, grey for value. Label the last point of each (88.7% and 8.2%). Add a text box on the gap: "UPI: 88.7% of transactions, 8.2% of value." |

Rules to hit the brief: at most 5 visuals in the final file (ask the faculty whether text boxes and slicers count), the insight chart has a highlight or annotation, and the conclusion is a text box, not a chart.

Note on visual 1: your Hook should answer "why does this question matter". The rising line plus the 88.7% label does it. If you prefer to show size, use `upi_monthly_detail` volume instead.

## 4. Annotations
Use the filled-in sentences in `annotations.md`. Every number there is traced to a column and row in `eda_metrics.csv`.

## 5. Merge test (15 min, do early)
1. Ask Kushi for her current `.pbix`.
2. Open her file, select one of her visuals, Ctrl+C. In your file, Ctrl+V on a blank page.
3. If it shows data, measure names match. If it asks to fix fields, a name differs: compare to `CONTRACT.md`.
4. Click a bar on her visual 5 and watch your visuals respond. If not: Format > Edit interactions.
5. Delete the test visual afterwards.

## 6. If the data is re-exported
`git pull`, `python scripts/check_contract.py data/clean exports` (expect 4 or 5 files, then OK), then Home > Refresh in Power BI. Re-check every number in `annotations.md`.

## 7. Done when
- The story reads top to bottom with no explaining.
- Hook, build-up, insight (gap highlighted) and conclusion are all present.
- Every number on the page matches `eda_metrics.csv`.
- Saved as `powerbi/jaanhavi/Story_v1.pbix`, then merged into `powerbi/final/UPI_Story.pbix`.
