# RA-MDST: reproducing the article

Everything in the article's results section is produced by one notebook, `RA_MDST_revision.ipynb`.

## Data

`data/AV_crash_severity_deidentified.csv` is the public, de-identified version of the processed dataset of
Shafique et al. (IEEE Access, 2024): 324 crash reports, 184 predictors and the target column `target`
(0 = Minor, 1 = Moderate, 2 = None). See `DATA.md` for its source, the preprocessing and the fields that were removed.
The article's main results were computed on the full processed file (189 predictors), which contains fields that could
help locate the source reports and is therefore available from the authors on reasonable request for research use.
Running the notebook on the public file reproduces Supplementary Table S6 of the article (results without the removed fields).

## Quick start

```bash
pip install -r requirements.txt
python run_all.py --data data/AV_crash_severity_deidentified.csv          # full run, about 60–90 min on 4 CPU cores
python verify_outputs.py --out revision_results                      # runs automatically after a full run
```

* `--quick` runs a 5-minute smoke test (numbers differ from the article).
* `--sections 3,4` regenerates selected sections only (see `EXPECTED_OUTPUTS.md` for which section makes which table).
* `--fresh` ignores checkpoints and recomputes everything.
* To confirm that two runs are identical: `python verify_outputs.py --compare runA/revision_results runB/revision_results`.

On Kaggle, upload `RA_MDST_revision.ipynb`, add the dataset as an Input and use *Save & Run All (Commit)*.

## Files

| File | Purpose |
|---|---|
| `RA_MDST_revision.ipynb` | the single notebook (Sections 1–17) |
| `run_all.py` | runs the notebook headless with the chosen options |
| `verify_outputs.py` | checks expected files and key values; compares two runs |
| `expected_values.json` | key values reported in the article, with tolerances |
| `EXPECTED_OUTPUTS.md` | every output file and the table or figure of the article it belongs to |
| `paper_figures.py` | draws the article's result figures from the output tables (also run as Section 15) |
| `figures_src/fig1_workflow.py` | draws the workflow diagram (Fig. 1) |
| `requirements.txt` | pinned package versions |

## Determinism

All random states derive from the base seed 42 (Table 3 of the article explains the seed formulas). With the pinned
versions in `requirements.txt`, two runs produce identical tables; only the run-time columns (`*_sec`) and Fig. 14,
which report measured computation time, differ between machines.
