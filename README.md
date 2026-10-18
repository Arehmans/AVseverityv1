# RA-MDST: reproducing the article

Everything in the article's results section is produced by one notebook, `RA_MDST_revision.ipynb`.

## Quick start

```bash
pip install -r requirements.txt
python run_all.py --data data/NN_MissingHandlingdataset.csv          # full run, about 60–90 min on 4 CPU cores
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
| `RA_MDST_revision.ipynb` | the single notebook (Sections 1–15) |
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
