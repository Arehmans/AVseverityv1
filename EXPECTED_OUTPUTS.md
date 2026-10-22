# Expected outputs

`python run_all.py --data <path>/AV_crash_severity_deidentified.csv` (FULL mode, base seed 42) writes everything below to
`revision_results/`. Each row gives the article item it supports and the notebook section that produces it.
A section can be regenerated on its own with `--sections N`; sections 4, 5 and 15 read the Protocol B results of
Section 3 from its checkpoint, so run Section 3 first (or keep its checkpoint).
`verify_outputs.py --out revision_results` checks that every file exists and that the key values in
`expected_values.json` match the article; `verify_outputs.py --compare runA runB` checks that two runs produced
identical tables (run-time columns ending in `_sec` are ignored).

## Tables

| File | Article item | Section | Content |
|---|---|---|---|
| `tables/T00_feature_types.csv` | Section 3.5.2 | setup | variable type assigned to each predictor |
| `tables/T01_overlap_distribution_all_observations.csv` | Table 4, Fig. 3 | 1 | shared Euclidean/Manhattan neighbors (0–3) for the 324 observations; mean 0.7623 |
| `tables/T01b_overlap_by_class.csv` | Section 3.3 | 1 | overlap by class |
| `tables/T02_protocolA_fold_results_all_seeds.csv` | Tables 6–7 | 2 | Protocol A fold-level results, 11 seeds |
| `tables/T02a_protocolA_seed42_reproduction.csv` | Table 6, Fig. 6 | 2 | Protocol A, seed 42 (MDST 90.58, RA-MDST 92.41) |
| `tables/T02b_protocolA_seed_sweep.csv` | Table 7 | 2 | Protocol A across 11 seeds |
| `tables/T02c_protocolB_fold_class_counts.csv` | Table 2 | 2 | class counts per Protocol B fold |
| `tables/T03_protocolB_fold_results.csv` | Tables 8–10, Fig. 7 | 3 | all metrics, 50 folds × 10 classifiers × 11 samplers |
| `tables/T03_protocolB_oof_predictions.csv` | Fig. 13 | 3 | out-of-fold predictions |
| `tables/T03a_protocolB_summary_all.csv` | Section 4.2 | 3 | mean ± SD per classifier and sampler |
| `tables/T03b_protocolB_macroF1_matrix.csv` | Fig. 7 | 3 | macro-F1 matrix, classifier × sampler |
| `tables/T03c_protocolB_LinearSVM_table.csv` | Table 8 | 3 | linear SVM, all samplers (incl. QWK) |
| `tables/T04_pairwise_statistics.csv` | Table 9, Fig. 8, Table S4 | 4 | paired tests: Δ, corrected 95% CI, raw p, Holm over the 60 tests of Table 9 (`p_nb_holm_table9_60tests`, primary), Holm within each comparison (`p_nb_holm`), Holm over all 100 tests, BH, rank-biserial r, Cohen's d_z |
| `tables/T04b_friedman_average_ranks.csv` | Section 4.2, Fig. 7 | 4 | average ranks, Friedman test |
| `tables/T04c_holm_survival_summary.csv` | Table 9 | 4 | which comparisons survive Holm correction (60-test family; per-comparison family for reference) |
| `tables/T05_ablation_protocolB.csv` | Table 10 | 5 | component ablation |
| `tables/T06_validity_fold_level.csv` | Table 5 | 3 | invalid synthetic values per fold |
| `tables/T06a_validity_summary.csv` | Table 5 | 6 | invalid synthetic values, summary |
| `tables/T07_diversity_fold_level.csv` | Table 12 | 3 | diversity metrics per fold |
| `tables/T07a_diversity_summary.csv` | Table 12, Fig. 9, Table S1 | 7 | diversity metrics incl. coverage and density, summary |
| `tables/T07b_diversity_by_class.csv` | Section 4.6 | 7 | diversity metrics by class |
| `tables/T08_sensitivity_fold_level.csv` | Table 13 | 8 | sensitivity, fold level |
| `tables/T08a_sensitivity_summary.csv` | Fig. 10 | 8 | sensitivity, per setting |
| `tables/T08b_sensitivity_ranges.csv` | Table 13 | 8 | macro-F1 range per factor |
| `tables/T09_nested_cv_fold_level.csv` | Table 14 | 9 | nested CV, outer folds |
| `tables/T09a_nested_cv_summary.csv` | Table 14 | 9 | nested CV summary |
| `tables/T09b_nested_cv_selected_hyperparameters.csv` | Section 4.7 | 9 | selected hyper-parameters |
| `tables/T10_partial_balancing_fold_level.csv` | Fig. 11 | 10 | partial balancing, fold level |
| `tables/T10a_partial_balancing_summary.csv` | Fig. 11, Section 4.8 | 10 | partial balancing summary and real-to-synthetic ratios |
| `tables/T11_ordinal_fold_level.csv` | Table 15 | 11 | ordinal models, fold level |
| `tables/T11a_ordinal_summary.csv` | Table 15 | 11 | nominal vs ordinal models |
| `tables/T12_shap_fold_level.csv` | Fig. 12 | 12 | SHAP per fold |
| `tables/T12a_shap_global_importance.csv` | Fig. 12 | 12 | global SHAP importance and top-20 stability |
| `tables/T12b_shap_by_class.csv` | Section 4.10 | 12 | SHAP by class |
| `tables/T13_external_fold_level.csv` | Table 16 | 13 | external benchmarks, fold level |
| `tables/T13a_external_summary.csv` | Table 16 | 13 | external benchmarks summary |
| `tables/T13b_external_macroF1_matrix.csv` | Table 16 | 13 | macro-F1 matrix |
| `tables/T16_tp_baselines_fold_results.csv` | Table 11, Table S2 | 16 | type-preserving SMOTE / Borderline-SMOTE / ADASYN, fold level |
| `tables/T16_tp_baselines_validity_fold_level.csv` | Table 11 | 16 | invalid values of the type-preserving variants |
| `tables/T16_tp_baselines_diversity_fold_level.csv` | Table 11 | 16 | diversity of the type-preserving variants |
| `tables/T16a_macroF1_matrix_with_TP.csv` | Table 11, Table S2 | 16 | macro-F1, twelve samplers × ten classifiers |
| `tables/T16a_average_ranks_with_TP.csv` | Table 11 | 16 | average ranks among twelve samplers |
| `tables/T16a_linearSVM_with_TP.csv` | Section 4.6 | 16 | linear SVM, twelve samplers |
| `tables/T16b_tp_statistics.csv` | Section 4.6, Table S3 | 16 | paired tests (Holm within each family of 30) |
| `tables/T16c_tp_validity_diversity.csv` | Table 11 | 16 | validity and diversity summary of the variants |
| `tables/T17_near_duplicate_threshold_fold_level.csv` | Table S5 | 17 | near-duplicate rate at f = 0.05, 0.1, 0.2, 0.3, fold level |
| `tables/T17a_near_duplicate_threshold_summary.csv` | Table S5, Section 4.7 | 17 | near-duplicate rate and rank per threshold |

## Article figures (drawn from the tables by Section 15 / `paper_figures.py`)

| File | Article item | Source tables |
|---|---|---|
| `paper_figures/Fig03_overlap_distribution.pdf` | Fig. 3 | T01 |
| `paper_figures/Fig06_protocolA_vs_B.pdf` | Fig. 6 | T02a, T03c |
| `paper_figures/Fig07_protocolB_macroF1_heatmap.pdf` | Fig. 7 | T03b, T04b |
| `paper_figures/Fig08_forest_macroF1.pdf` | Fig. 8 | T04 |
| `paper_figures/Fig09_synthetic_diversity.pdf` | Fig. 9 | T07a |
| `paper_figures/Fig10_sensitivity.pdf` | Fig. 10 | T08, T08a |
| `paper_figures/Fig11_partial_balancing.pdf` | Fig. 11 | T10a |
| `paper_figures/Fig12_shap_importance.pdf` | Fig. 12 | T12a, T00 |
| `paper_figures/Fig13_confusion_linearSVM.pdf` | Fig. 13 | T03 predictions |
| `paper_figures/Fig14_computational_cost.pdf` | Fig. 14 | T03 (timings vary between machines) |

Figures 1, 4 and 5 are schematic diagrams (Fig. 1 is drawn by `figures_src/fig1_workflow.py`). Fig. 2 shows the class
counts (237 / 52 / 35), and Figs 15–16 (ROC curves and PCA projection of the first repeat) are descriptive illustrations
that are not used for any quantitative claim.

## Other files

| File | Content |
|---|---|
| `RESULTS_SUMMARY.md` | key numbers of every section |
| `PROTOCOL.md` | protocol description, seeds and software versions |
| `MANIFEST.csv` | every output file with a content hash for run-to-run comparison |
| `RA_MDST_revision_executed.ipynb` | the executed notebook with all printed output |
| `../RA_MDST_revision_results.zip` | everything above in one archive |
