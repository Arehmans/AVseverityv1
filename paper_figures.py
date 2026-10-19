#!/usr/bin/env python3
"""Draw the article's result figures from the CSV tables written by RA_MDST_revision.ipynb.

    python paper_figures.py --out revision_results        # writes revision_results/paper_figures/Fig*.pdf|png

Every figure is a pure function of the tables, so identical tables give identical figures.
The notebook calls make_all() at the end (Section 15)."""
import argparse, os, re
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SAMPLERS = ["None", "ROS", "SMOTE", "Borderline-SMOTE", "ADASYN", "SMOTE-NC", "MDST", "RA-MDST", "RA-MDST-TP"]
LABEL = {"None": "No oversampling", "ROS": "Random oversampling", "Borderline-SMOTE": "Borderline-SMOTE"}
COL = {"None": "#8c8c8c", "ROS": "#e87ba4", "SMOTE": "#eb6834", "Borderline-SMOTE": "#eda100", "ADASYN": "#e34948",
       "SMOTE-NC": "#008300", "MDST": "#1baf7a", "RA-MDST": "#2a78d6", "RA-MDST-TP": "#6250d6"}
CLF = ["LogisticRegression", "LinearSVM", "RBFSVM", "KNN", "DecisionTree", "RandomForest", "ExtraTrees",
       "GradientBoosting", "AdaBoost", "MLP"]
CLF_LABEL = {"LogisticRegression": "Logistic regression", "LinearSVM": "Linear SVM", "RBFSVM": "RBF SVM", "KNN": "k-NN",
             "DecisionTree": "Decision tree", "RandomForest": "Random forest", "ExtraTrees": "Extra trees",
             "GradientBoosting": "Gradient boosting", "AdaBoost": "AdaBoost", "MLP": "MLP"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True, "legend.frameon": False,
                     "savefig.dpi": 300, "pdf.fonttype": 42})

TABLE9_COMPS = ["RA-MDST − MDST", "RA-MDST-TP − MDST", "RA-MDST-TP − SMOTE", "RA-MDST − None", "RA-MDST-TP − None", "MDST − None"]

def holm_adjust(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); out = np.empty(n); run = 0.0
    for r, i in enumerate(o):
        run = max(run, min(1.0, (n - r) * p[i])); out[i] = run
    return out

def _num(x):
    return float(str(x).split("±")[0])

def _save(fig, out, name):
    d = os.path.join(out, "paper_figures"); os.makedirs(d, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(d, f"{name}.{ext}"), bbox_inches="tight", metadata={"CreationDate": None} if ext == "pdf" else None)
    plt.close(fig)

def fig03_overlap(T, out):
    t = T("T01_overlap_distribution_all_observations.csv")
    n = t.n_observations.sum(); mean = (t.shared * t.n_observations).sum() / (3 * n)
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    b = ax.bar(t.shared, t.n_observations, color="#2a78d6", width=0.65)
    for x, v, p in zip(t.shared, t.n_observations, t.percent):
        ax.text(x, v + n * 0.01, f"{v}\n({p:.1f}%)", ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(t.shared, [f"{s}\n(score {['0', '1/3', '2/3', '1'][s]})" for s in t.shared])
    ax.set_xlabel("Shared neighbors between Euclidean and Manhattan top-3 sets"); ax.set_ylabel("Number of observations")
    ax.set_ylim(0, t.n_observations.max() * 1.28)
    ax.text(0.02, 0.97, f"Mean overlap = {mean:.4f} (n = {n})", transform=ax.transAxes, va="top", fontsize=9,
            bbox=dict(boxstyle="round", fc="white", ec="#888"))
    _save(fig, out, "Fig03_overlap_distribution")

def fig06_protocols(T, out):
    a = T("T02a_protocolA_seed42_reproduction.csv").set_index("sampler")
    b = T("T03c_protocolB_LinearSVM_table.csv").set_index("sampler")
    s = [x for x in SAMPLERS if x in a.index and x in b.index]
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    for ax, (ma, mr, mb, title) in zip(axes, [("accuracy", "acc_real_test_rows", "accuracy", "(a) Accuracy"),
                                             ("f1_macro", "f1_real_test_rows", "f1_macro", "(b) Macro-F1")]):
        x = np.arange(len(s)); w = 0.27
        ax.bar(x - w, a.loc[s, ma], w, color="#c9c9c9", label="Protocol A, all test rows")
        ax.bar(x, a.loc[s, mr], w, color="#8c8c8c", label="Protocol A, real test rows only")
        ax.bar(x + w, [_num(v) for v in b.loc[s, mb]], w, color="#2a78d6", label="Protocol B (leakage-controlled)")
        ax.set_xticks(x, [LABEL.get(v, v) for v in s], rotation=35, ha="right"); ax.set_title(title, loc="left")
        ax.set_ylim(0, 100)
    axes[0].set_ylabel("Linear SVM (%)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, fontsize=9, bbox_to_anchor=(0.5, 1.04))
    _save(fig, out, "Fig06_protocolA_vs_B")

def fig07_heatmap(T, out):
    m = T("T03b_protocolB_macroF1_matrix.csv").set_index("classifier")
    s = [x for x in SAMPLERS if x in m.columns]; c = [x for x in CLF if x in m.index]
    M = m.loc[c, s]
    rk = T("T04b_friedman_average_ranks.csv"); rk = rk[rk.metric == "f1_macro"].set_index("sampler").avg_rank
    fig, ax = plt.subplots(figsize=(10, 4.6))
    im = ax.imshow(M.values, cmap="Blues", aspect="auto", vmin=np.nanmin(M.values) - 5, vmax=np.nanmax(M.values) + 2)
    best = M.values.argmax(axis=1)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M.values[i, j]
            ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=8.3, fontweight="bold" if j == best[i] else "normal",
                    color="white" if v > np.nanmean(M.values) + 5 else "#1f2328")
    SHORT = {"None": "None", "ROS": "ROS", "Borderline-SMOTE": "B-SMOTE"}
    ax.set_xticks(range(len(s)), [f"{SHORT.get(x, x)}\n(rank {rk.get(x, np.nan):.2f})" for x in s], fontsize=8)
    ax.set_xlabel("Oversampling method (average rank across classifiers; lower is better)")
    ax.set_yticks(range(len(c)), [CLF_LABEL[x] for x in c]); ax.grid(False)
    plt.colorbar(im, ax=ax, fraction=0.025, pad=0.01, label="Macro-F1 (%)")
    _save(fig, out, "Fig07_protocolB_macroF1_heatmap")

def fig08_forest(T, out):
    st = T("T04_pairwise_statistics.csv"); st = st[st.metric == "f1_macro"].copy()
    fam = st.comparison.isin(TABLE9_COMPS)            # Holm across all 60 tests of Table 9 (6 comparisons x 10 classifiers)
    st.loc[fam, "p_holm60"] = holm_adjust(st.loc[fam, "p_nadeau_bengio"].astype(float).values)
    comps = [x for x in ["RA-MDST − MDST", "RA-MDST-TP − MDST", "RA-MDST-TP − SMOTE", "RA-MDST − None", "RA-MDST-TP − None"]
             if x in set(st.comparison)]
    lo = st[st.comparison.isin(comps)].nb_ci_low_pp.min(); hi = st[st.comparison.isin(comps)].nb_ci_high_pp.max()
    rc = {"font.size": 12, "axes.titlesize": 12, "xtick.labelsize": 11, "ytick.labelsize": 12}
    with plt.rc_context(rc):
        fig, axes = plt.subplots(1, len(comps), figsize=(2.55 * len(comps), 4.6), sharey=True, sharex=True)
        _forest_panels(fig, axes, st, comps, lo, hi)
    _save(fig, out, "Fig08_forest_macroF1")

def _forest_panels(fig, axes, st, comps, lo, hi):
    for k, (ax, comp) in enumerate(zip(np.atleast_1d(axes), comps)):
        d = st[st.comparison == comp].set_index("classifier").reindex([x for x in CLF if x in set(st.classifier)])
        yy = np.arange(len(d))[::-1]; col = COL[comp.split(" − ")[0]]
        sig = d.p_holm60 < 0.05
        lib = (d.p_nb_holm < 0.05) & ~sig
        ax.hlines(yy, d.nb_ci_low_pp, d.nb_ci_high_pp, color=col, lw=1.8)
        ax.scatter(d.delta_pp[sig], yy[sig.values], color=col, s=34, zorder=3)
        ax.scatter(d.delta_pp[~sig], yy[~sig.values], facecolor="white", edgecolor=col, s=34, zorder=3)
        for yv, (_, rr), lb in zip(yy, d.iterrows(), lib.values):
            if lb:
                ax.text(rr.nb_ci_high_pp + 0.8, yv, "†", va="center", fontsize=11, color=col)
        ax.axvline(0, color="#52514e", lw=0.9)
        a_, b_ = comp.split(" − ")
        ax.set_title(f"({'abcde'[k]}) {a_}\n− {'no oversampling' if b_ == 'None' else b_}", loc="left")
        ax.set_xlim(lo - 2, hi + 2); ax.set_xlabel("Δ macro-F1 (pp)")
        ax.set_yticks(yy, [CLF_LABEL[x] for x in d.index])


def fig09_diversity(T, out):
    t = T("T07a_diversity_summary.csv").set_index("sampler")
    s = [x for x in ["ROS", "SMOTE", "MDST", "RA-MDST", "RA-MDST-TP"] if x in t.index]
    panels = [("unique_ratio", "(a) Unique rows ↑"), ("near_dup_within_syn", "(b) Near-duplicates ↓"),
              ("rel_pairwise_spread", "(c) Spread ↑"), ("rel_nn_dist_to_real", "(d) Distance to real"),
              ("intrusion_rate", "(e) Intrusion ↓"), ("knn5_purity", "(f) 5-NN purity")]
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.0), sharey=True, gridspec_kw={"wspace": 0.3, "hspace": 0.45})
    axes = axes.ravel()
    for ax, (cname, title) in zip(axes, panels):
        v = t.loc[s, cname]
        ax.barh(range(len(s))[::-1], v, color=[COL[x] for x in s], height=0.65)
        for y, val in zip(range(len(s))[::-1], v):
            ax.text(val, y, f" {val:.3f}", va="center", fontsize=8.5)
        ax.set_title(title, fontsize=10, loc="left"); ax.set_xlim(0, max(1.0, v.max() * 1.35))
    for ax in (axes[0], axes[3]):
        ax.set_yticks(range(len(s))[::-1], [LABEL.get(x, x) for x in s])
    _save(fig, out, "Fig09_synthetic_diversity")

def fig10_sensitivity(T, out):
    t = T("T08a_sensitivity_summary.csv"); n_f = T("T08_sensitivity_fold_level.csv").groupby(["factor", "sampler"]).size().max()
    specs = [("k", "k", "(a) Neighborhood size k"), ("lambda", "lam", "(b) λ interval"),
             ("n_features", "n", "(c) RFE features"), ("C", "C", "(d) SVM C (log scale)")]
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.4), sharey=True)
    for ax, (fac, col, title) in zip(axes, specs):
        d = t[t.factor == fac]
        for s in [x for x in SAMPLERS if x in set(d.sampler)]:
            e = d[d.sampler == s].copy()
            if fac == "lambda":
                e["x"] = e[col].map(lambda z: float(re.findall(r"[\d.]+", str(z))[1]) - float(re.findall(r"[\d.]+", str(z))[0]))
            else:
                e["x"] = e[col].astype(float)
            e = e.sort_values("x"); reps = max(1, len(T("T08_sensitivity_fold_level.csv")[lambda q: (q.factor == fac) & (q.sampler == s)]) // max(len(e), 1))
            ax.errorbar(e.x, e.f1_macro_mean, yerr=e.f1_macro_std / np.sqrt(reps), color=COL[s], marker="o", ms=3.5, lw=1.4,
                        capsize=2, label=LABEL.get(s, s))
        ax.set_title(title, loc="left", fontsize=9)
        if fac == "C": ax.set_xscale("log")
        if fac == "lambda": ax.set_xlabel("interval width (centered at 0.5)")
    axes[0].set_ylabel("Macro-F1 (%)"); axes[-1].legend(fontsize=7.5, loc="lower right")
    _save(fig, out, "Fig10_sensitivity")

def fig11_partial(T, out):
    t = T("T10a_partial_balancing_summary.csv")
    clfs = [x for x in ["LinearSVM", "LogisticRegression", "RandomForest"] if x in set(t.classifier)]
    fig, axes = plt.subplots(1, len(clfs), figsize=(4.2 * len(clfs), 3.4))
    for k, (ax, c) in enumerate(zip(np.atleast_1d(axes), clfs)):
        d = t[t.classifier == c]; base = d[d.sampler == "None"].f1_macro
        for s in [x for x in SAMPLERS if x in set(d.sampler) and x != "None"]:
            e = pd.concat([d[d.sampler == "None"].assign(sampler=s), d[d.sampler == s]]).sort_values("alpha")
            ax.plot(e.alpha, e.f1_macro, marker="o", ms=3.5, color=COL[s], label=LABEL.get(s, s))
        if len(base): ax.axhline(base.iloc[0], color=COL["None"], ls="--", lw=1, label="No oversampling")
        ax.set_title(f"({'abc'[k]}) {CLF_LABEL[c]}", loc="left"); ax.set_xlabel("Balancing level α")
    np.atleast_1d(axes)[0].set_ylabel("Macro-F1 (%)"); np.atleast_1d(axes)[-1].legend(fontsize=7.5)
    _save(fig, out, "Fig11_partial_balancing")

def fig12_shap(T, out):
    t = T("T12a_shap_global_importance.csv")
    try:
        ident = {f for f in T("T00_feature_types.csv").feature if re.search(r"DATE|TIME|ADDRESS|DETAILS", str(f), re.I)}
    except Exception:
        ident = set()
    models = list(dict.fromkeys(t.model))[:2]
    fig, axes = plt.subplots(1, len(models), figsize=(6.4 * len(models), 4.6), gridspec_kw={"wspace": 0.55})
    for k, (ax, m) in enumerate(zip(np.atleast_1d(axes), models)):
        d = t[t.model == m].sort_values("mean_abs_shap", ascending=False).head(15)[::-1]
        ax.barh(d.feature, d.mean_abs_shap, color=["#b0b0b0" if f in ident else "#2a78d6" for f in d.feature])
        for y, (v, n) in enumerate(zip(d.mean_abs_shap, d.top20_stability_folds)):
            ax.text(v, y, f" {n}/5", va="center", fontsize=7.5)
        nm = "Linear SVM" if "Linear" in m else ("Random forest" if "Forest" in m else m)
        ax.set_title(f"({'ab'[k]}) {nm}", loc="left"); ax.set_xlabel("Mean |SHAP| on held-out real records")
        ax.set_xlim(0, d.mean_abs_shap.max() * 1.15)
    _save(fig, out, "Fig12_shap_importance")

def fig13_confusion(T, out):
    p = T("T03_protocolB_oof_predictions.csv")
    p = p[(p.repeat == 0) & (p.classifier == "LinearSVM")]
    names = {0: "Minor", 1: "Moderate", 2: "None"}
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8), gridspec_kw={"wspace": 0.45})
    for k, (ax, s) in enumerate(zip(axes, ["MDST", "RA-MDST"])):
        d = p[p.sampler == s]; labs = sorted(set(d.y_true))
        cm = pd.crosstab(d.y_true, d.y_pred).reindex(index=labs, columns=labs, fill_value=0).values
        r = cm / cm.sum(1, keepdims=True)
        ax.imshow(r, cmap="Blues", vmin=0, vmax=1); ax.grid(False)
        for i in range(len(labs)):
            for j in range(len(labs)):
                ax.text(j, i, f"{100 * r[i, j]:.1f}%\n({cm[i, j]})", ha="center", va="center", fontsize=8.5,
                        color="white" if r[i, j] > 0.55 else "#1f2328")
        ax.set_xticks(range(len(labs)), [names.get(l, l) for l in labs]); ax.set_yticks(range(len(labs)), [names.get(l, l) for l in labs])
        ax.set_xlabel("Predicted"); ax.set_ylabel("True"); ax.set_title(f"({'ab'[k]}) {s}", loc="left")
    _save(fig, out, "Fig13_confusion_linearSVM")

def fig14_cost(T, out):
    f = T("T03_protocolB_fold_results.csv")
    f = f[(f.classifier == "LinearSVM") & f.sampler.isin(["MDST", "RA-MDST", "RA-MDST-TP", "SMOTE"])]
    g = f.groupby("sampler")[["sampling_sec", "fit_sec"]].mean().reindex(["SMOTE", "MDST", "RA-MDST", "RA-MDST-TP"]).dropna()
    fig, ax = plt.subplots(figsize=(5.4, 3.2)); x = np.arange(len(g)); w = 0.38
    ax.bar(x - w / 2, 1000 * g.sampling_sec, w, color="#2a78d6", label="Oversampling")
    ax.bar(x + w / 2, 1000 * g.fit_sec, w, color="#8c8c8c", label="Linear SVM training")
    ax.set_xticks(x, g.index); ax.set_ylabel("Mean time per fold (ms)"); ax.legend()
    _save(fig, out, "Fig14_computational_cost")

ALL = [fig03_overlap, fig06_protocols, fig07_heatmap, fig08_forest, fig09_diversity, fig10_sensitivity,
       fig11_partial, fig12_shap, fig13_confusion, fig14_cost]

def make_all(out):
    tabs = os.path.join(out, "tables")
    T = lambda name: pd.read_csv(os.path.join(tabs, name), keep_default_na=False, na_values=["", "nan", "NaN"])
    done, failed = [], []
    for fn in ALL:
        try:
            fn(T, out); done.append(fn.__name__)
        except FileNotFoundError as e:
            failed.append(f"{fn.__name__}: missing {os.path.basename(e.filename)}")
        except Exception as e:
            failed.append(f"{fn.__name__}: {type(e).__name__}: {e}")
    print("paper figures written:", ", ".join(done))
    for f in failed:
        print("  not drawn ->", f)
    return done, failed

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="revision_results"); a = ap.parse_args()
    make_all(a.out)
