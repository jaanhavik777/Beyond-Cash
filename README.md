# Beyond Cash: A Data Story of UPI's Rise in India's Digital Payments

**Repo:** `upi-data-story` · **Course:** Visualization of Data, Understanding and Interpretation (PES University)

## Question
How has UPI's share of India's digital payments changed over time, and how has it reshaped transaction volume, value and ticket size compared with other payment methods?

## Units covered
| Unit | What we do | Tool |
|------|-----------|------|
| Unit 1 | EDA: cleaning, growth rates, share, trend tests, anomaly flags | Python |
| Unit 2 | Narrative: Hook → Build-up → Insight → Conclusion | Power BI |
| Unit 3 | Interactive: slicers, Year→Quarter→Month drill-down, cross-filtering | Power BI |

## Team
| Person | SRN | Owns |
|--------|-----|------|
| Jaanhavi Ashwin Kher | PES2UG24CS199 | Narrative visuals 1–3, final .pbix merge, deck, demo |
| Krishna Manoj | PES2UG24CS236 | Python EDA, metrics, insights |
| Kushi Niranjana | PES2UG24CS245 | Interactive visuals 4–5, slicers, DAX, IEEE paper |
| Amrit Raj Anmol | PES2UG24CS056 | Data collection, cleaning, repo |

## Data sources
- RBI, Payment System Indicators
- NPCI, UPI Product Statistics
- NPCI, IMPS Product Statistics (optional)

## Repo layout
```
data/raw/        original downloads, never edited        (Amrit)
data/clean/      the three contract CSVs                 (Amrit)
data/sample/     synthetic stand-ins, same columns       (Amrit)
notebooks/       EDA notebook                            (Krishna)
exports/         eda_metrics.csv, key_insights.csv       (Krishna)
powerbi/jaanhavi story file and theme.json               (Jaanhavi)
powerbi/kushi    interactive file and measures.dax       (Kushi)
powerbi/final    merged UPI_Story.pbix                   (Jaanhavi)
paper/           IEEE draft                              (Kushi, all write sections)
slides/          project deck                            (Jaanhavi)
```

## Start here
1. Read `CONTRACT.md` for the exact file and column names.
2. Read `CONTRIBUTING.md` for folder ownership and git workflow.
3. Build against `data/sample/` until `data/clean/` has real data.

```bash
git clone <repo-url> && cd upi-data-story
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python data/clean_data.py        # once Amrit has filled it in
```
