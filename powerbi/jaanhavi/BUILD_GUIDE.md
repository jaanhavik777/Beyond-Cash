# Jaanhavi's Power BI build guide (Unit 2: the narrative)

Goal: one page that reads Hook → Build-up → Insight → Conclusion. Build it now on `data/sample/`, then change the source path when real data lands.

## 1. Load and model (20 min)
1. Home > Get data > Text/CSV. Load `data/sample/fact_payments_monthly.csv`, `upi_monthly_detail.csv`, `dim_date.csv`. Later also `exports/eda_metrics.csv` and `exports/key_insights.csv`.
2. In Power Query, check `date` is type **Date** in every table.
3. Model view: relate `dim_date[date]` (one) to `date` in `fact_payments_monthly`, `upi_monthly_detail`, `eda_metrics` (many). Leave `key_insights` unrelated.
4. Right-click `dim_date` > **Mark as date table** > `date`.
5. View > Themes > Browse for themes > `theme.json`. Push this file to the repo so Kushi can use the same one.
6. New measure for each block in `measures.dax`. Format: volume/value as whole number, share and YoY as Percentage, Avg Ticket as Decimal 0.

## 2. Page layout (16:9, 1280 x 720)
```
+--------------------------------------------------------------+
| Title: Beyond Cash: UPI's rise in India's digital payments    |
+------------------------+-----------------------------------+
| HOOK (visual 1)        | BUILD-UP (visual 2)               |
| line: UPI volume+value | 100% stacked col: share by method |
| text: hook annotation  | text: build-up annotation         |
+------------------------+-----------------------------------+
| INSIGHT (visual 3)  highlighted turning point + annotation   |
+--------------------------------------------------------------+
| CONCLUSION: one takeaway, 2-3 lines                          |
+--------------------------------------------------------------+
```
Kushi's visuals 4 and 5 and the slicers go on the right or a second page at merge time. Leave room.

## 3. Visuals
| # | Stage | Type | Fields | Format |
|---|-------|------|--------|--------|
| 1 | Hook | Line and clustered column chart | X: `dim_date[date]` (month); column: `[Total Volume (Mn)]`; line: `[Total Value (Cr)]`; filter payment_method = UPI (visual-level filter) | Title "UPI monthly volume and value"; axis titles with units |
| 2 | Build-up | 100% stacked column | X: `dim_date[date]`; values `[Total Volume (Mn)]`; legend `payment_method` | Make UPI the first colour (blue), others in greys |
| 3 | Insight | Line chart | X: `dim_date[date]`; Y: `[UPI Share % (Volume)]`; second line `[UPI Share % (Value)]` | Colour the crossover month's marker with conditional formatting from `[x_Is Crossover]`; add a 50% constant line (Analytics pane) |

Rules to hit the brief: at most 5 visuals in the final file (text boxes and slicers: ask the faculty if they count), the insight chart must show a highlight or annotation, and the conclusion is a text box, not a chart.

## 4. Annotations
Put the sentence next to each chart in a text box. Use the templates in `annotations.md`. Do not type numbers in by hand when a card can show them: add a Card visual for `[x_UPI Crossover Month]` only if you still have room under the 5-visual cap; otherwise type the number once real data is final.

## 5. Merge test (do this early, 15 min)
1. Ask Kushi for her current `.pbix`, or send her yours.
2. In yours: open her file, select one of her visuals, Ctrl+C. In your file, Ctrl+V on a blank page.
3. If the visual shows data, the measure names match. If it asks to fix fields, a name differs: compare the names to `CONTRACT.md` and rename.
4. Check cross-filtering: click a bar on her visual 5 and watch your visuals 1–3 respond. If they don't: Format > Edit interactions.
5. Delete the test visual afterwards.

## 6. Switching to real data (when Amrit and Krishna push)
1. `git pull`. Run `python scripts/check_contract.py data/clean exports` and expect 5 files and OK.
2. Home > Transform data > Data source settings > Change source to `data/clean/...` and `exports/...`.
3. Refresh. Re-check every annotation against the new numbers. Delete anything that no longer holds.

## 7. Done when
- Story reads top to bottom with no explaining.
- Hook, build-up, insight (highlighted), conclusion all present.
- Every number on the page can be traced to `exports/` or a measure.
- File saved as `powerbi/jaanhavi/Story_v1.pbix`, then merged into `powerbi/final/UPI_Story.pbix`.
