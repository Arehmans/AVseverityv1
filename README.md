# RA-MDST: reproducing the article

Everything in the article's results section is produced by one notebook, `RA_MDST_revision.ipynb`.
This repository version is release **v1.0**, the version cited in the article's Data Availability Statement.

## Two datasets, two sets of expected results

| | Main analysis (all tables and figures of the article) | Public-file analysis (Supplementary Table S6) |
|---|---|---|
| Data file | full processed file, 189 predictors (not public; available from the authors on request for research use) | `data/AV_crash_severity_deidentified.csv`, 184 predictors (in this repository) |
| Command | `python run_all.py --data <full file>.csv` | `python run_all.py --data data/AV_crash_severity_deidentified.csv --sections 3,4 --out results_public` |
| Expected values | `expected_values.json` | `expected_values_public.json` |
| Verification | `python verify_outputs.py --out revision_results` | `python verify_outputs.py --out results_public --expected expected_values_public.json` |
| Output files | listed in `EXPECTED_OUTPUTS.md` | `tables/T03b_protocolB_macroF1_matrix.csv`, `T03c_protocolB_LinearSVM_table.csv`, `T04_pairwise_statistics.csv`, `T04b_friedman_average_ranks.csv` (and `T03`, `T04c`) |
| Article item | Tables 2–17, Figures 3–16, Supplementary Tables S1–S5 | Supplementary Table S6 (build it with `python make_table_s6.py --public results_public`) |

`run_all.py` verifies automatically after a run, choosing `expected_values_public.json` when the data file is the public
file. The two sets of numbers differ because the public file lacks five predictors (see `DATA.md`); the public run does
**not** reproduce the article's main tables, and the main run does not reproduce Table S6's "De-id." columns.
The "Full" columns of Table S6 are read from `reference/main_analysis_189/`, which holds summary result tables of the
main run (aggregated results only; no records).

## Data

`data/AV_crash_severity_deidentified.csv` is the public, de-identified version of the processed dataset of
Shafique et al. (IEEE Access, 2024): 324 crash reports, 184 predictors and the target column `target`
(0 = Minor, 1 = Moderate, 2 = None). `DATA.md` describes its source, the preprocessing, the removed fields, the
remaining linkage risk and the conditions of use. No lookup tables or mappings from codes to original values are published.

## Quick start (public file, about 60–90 min on 2–4 CPU cores)

```bash
pip install -r requirements.txt
python run_all.py --data data/AV_crash_severity_deidentified.csv --sections 3,4 --out results_public
python make_table_s6.py --public results_public          # writes results_public/tables/S6_main_vs_public.csv
```

* `--quick` runs a 5-minute smoke test (numbers differ from the article).
* `--sections 3,4` regenerates selected sections only (see `EXPECTED_OUTPUTS.md` for which section makes which table).
* `--fresh` ignores checkpoints and recomputes everything.
* To confirm that two runs are identical: `python verify_outputs.py --compare runA/revision_results runB/revision_results`.

On Kaggle, upload `RA_MDST_revision.ipynb`, add the data file as an Input and use *Save & Run All (Commit)*.

## Files

| File | Purpose |
|---|---|
| `RA_MDST_revision.ipynb` | the single notebook (Sections 1–17) |
| `run_all.py` | runs the notebook headless with the chosen options |
| `verify_outputs.py` | checks expected files and key values; compares two runs |
| `expected_values.json` | key values of the main analysis (full 189-predictor file), with tolerances |
| `expected_values_public.json` | key values of Supplementary Table S6 (public 184-predictor file) |
| `make_table_s6.py` | builds Supplementary Table S6 from a public run and `reference/main_analysis_189/` |
| `reference/main_analysis_189/` | summary result tables of the main run (used for Table S6 and Supplementary Tables S2–S4) |
| `DATA.md` | data source, preprocessing, de-identification and conditions of use |
| `EXPECTED_OUTPUTS.md` | every output file and the table or figure of the article it belongs to |
| `paper_figures.py` | draws the article's result figures from the output tables (also run as Section 15) |
| `figures_src/fig1_workflow.py` | draws the workflow diagram (Fig. 1) |
| `requirements.txt` | pinned package versions |

## Determinism

All random states derive from the base seed 42 (Table 3 of the article explains the seed formulas). With the pinned
versions in `requirements.txt`, two runs produce identical tables; only the run-time columns (`*_sec`) and Fig. 14,
which report measured computation time, differ between machines.
