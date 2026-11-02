# Project rules (from the Mini Project Brief)

Course: Visualization of Data, Understanding and Interpretation · Team of 4 · 20 marks, scaled to 6

## Rules
1. **One dataset, one clear question.** Ours: *How has UPI's share of India's digital payments changed over time?* RBI and NPCI monthly statistics are treated as one combined payments dataset.
2. **At least 2 units, and Unit 1 or Unit 2 must be one.** We cover Unit 1 (Python EDA), Unit 2 (narrative) and Unit 3 (interactive).
3. **The story has a shape:** Hook → Build-up (2–3 charts) → Insight (annotation or highlight) → Conclusion (takeaway).
4. **Deliverables:** Power BI file (.pbix) with **3–5 visuals max**, a PPT, and an IEEE draft paper (publication not required).
5. **Literature survey:** each student summarises **2 papers** (8 in total).

## Story map (5 charts, matches the rules above)
| Stage | Visual | Owner |
|---|---|---|
| Hook | 1. UPI monthly volume and value, line | Jaanhavi |
| Build-up | 2. Volume share by payment method, 100% stacked column | Jaanhavi |
| Build-up | 4. UPI volume with Year→Quarter→Month drill-down (or ticket size) | Kushi |
| Insight | 3. Annotated highlight of the turning point | Jaanhavi |
| Conclusion | Text block with the takeaway (not a chart) | Jaanhavi |
| Explore | 5. Payment-method comparison bar, cross-filters the rest | Kushi |

Slicers (date range, payment method) are controls. Ask the faculty whether they count toward the 5.

## Marks and reviews
| Item | Marks | When |
|---|---|---|
| Title, units, dataset | 1 | Review 1, week 6 |
| Literature survey (2 papers each) | 1 | Review 2, week 10 |
| Implementation and demo | 3 | Review 3, week 12 |
| IEEE draft | 1 | Review 3, week 12 |

## Final-review checklist
- [ ] One question stated on the first slide, in the paper and on the dashboard
- [ ] Units 1, 2 (and 3) each shown: notebook, narrative page, slicers and drill-down
- [ ] Hook, build-up, insight and conclusion visible in that order
- [ ] 5 charts or fewer in `powerbi/final/UPI_Story.pbix`
- [ ] Insight chart has an annotation or highlight
- [ ] Every dashboard number matches `exports/` (spot-check 5)
- [ ] Deck updated: data, method, dashboard screenshots, insights, conclusion
- [ ] IEEE draft complete with references
- [ ] 8 literature papers summarised (2 per student)
- [ ] `python scripts/check_contract.py` passes on `data/clean/` and `exports/`
