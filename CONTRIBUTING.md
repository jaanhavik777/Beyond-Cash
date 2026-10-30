# Working rules

## Folder ownership
Only the owner edits a folder (see README table). Need a change elsewhere? Message the owner.

## Git workflow
- `main` is always working. Nobody pushes directly to it.
- One branch per person per task: `amrit/clean-data`, `krishna/eda-metrics`, `jaanhavi/story-visuals`, `kushi/interactive-layer`.
- Small commits, message format: `area: what changed` (e.g. `data: add dim_date with Indian FY`).
- Open a pull request into `main`; one teammate approves; squash and merge.
- Pull `main` before you start each work block: `git pull origin main`.

## Power BI files (.pbix)
They are binary and cannot be merged. Jaanhavi and Kushi work in separate files under their own folders. Only Jaanhavi writes `powerbi/final/UPI_Story.pbix`.

## Notebooks
Clear outputs before committing large ones, and make sure it runs top to bottom (`Kernel → Restart & Run All`).

## Data
Never edit `data/raw/`. All cleaning lives in `data/clean_data.py` so anyone can rebuild `data/clean/`.
