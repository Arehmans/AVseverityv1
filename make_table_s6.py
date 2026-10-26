#!/usr/bin/env python3
"""Build Supplementary Table S6: main results on the full 189-predictor file vs the public 184-predictor file.

    python run_all.py --data data/AV_crash_severity_deidentified.csv --sections 3,4 --out results_public
    python make_table_s6.py --public results_public

The "Full" columns are read from reference/main_analysis_189/ (summary tables of the article's main run on the full
file, which is available on request); the "De-id." columns from the public run. Output: results_public/tables/S6_main_vs_public.csv
"""
import argparse, pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ORDER = ["None", "ROS", "SMOTE", "Borderline-SMOTE", "ADASYN", "SMOTE-NC", "MDST", "RA-MDST", "RA-MDST-TP"]

def load(folder):
    rd = lambda f: pd.read_csv(folder / f, keep_default_na=False, na_values=["", "nan", "NaN"])
    lin = rd("T03c_protocolB_LinearSVM_table.csv").set_index("sampler")
    mf = rd("T03b_protocolB_macroF1_matrix.csv").set_index("classifier")
    rk = rd("T04b_friedman_average_ranks.csv")
    rk = rk[rk.metric == "f1_macro"].set_index("sampler")["avg_rank"]
    num = lambda v: round(float(str(v).split("±")[0]), 2)
    return {s: (num(lin.loc[s, "f1_macro"]), num(lin.loc[s, "balanced_accuracy"]),
                num(mf.loc["RandomForest", s]), round(float(rk[s]), 2)) for s in ORDER}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--public", required=True, help="output folder of the public run")
    ap.add_argument("--main", default=str(HERE / "reference" / "main_analysis_189"))
    a = ap.parse_args()
    full, pub = load(pathlib.Path(a.main)), load(pathlib.Path(a.public) / "tables")
    rows = []
    for s in ORDER:
        f, p = full[s], pub[s]
        rows.append({"sampler": s,
                     "linearSVM_macroF1_full": f[0], "linearSVM_macroF1_public": p[0],
                     "linearSVM_balacc_full": f[1], "linearSVM_balacc_public": p[1],
                     "RF_macroF1_full": f[2], "RF_macroF1_public": p[2],
                     "avg_rank_full": f[3], "avg_rank_public": p[3]})
    out = pathlib.Path(a.public) / "tables" / "S6_main_vs_public.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(pd.DataFrame(rows).to_string(index=False)); print("written:", out)
