#!/usr/bin/env python3
"""Check a results folder against the article.

    python verify_outputs.py --out revision_results                 # main analysis (full 189-predictor file):
                                                                    # files present + key values of the article
    python verify_outputs.py --out results_public --expected expected_values_public.json
                                                                    # public 184-predictor file: values of Table S6
    python verify_outputs.py --compare run1/revision_results run2/revision_results
                                                                    # two runs give identical tables (timing columns ignored)
"""
import argparse, json, pathlib, sys
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent

def check_values(out, expected="expected_values.json"):
    spec = json.load(open(HERE / expected))
    print("Expected values:", expected, "-", spec.get("dataset", "main_189"))
    if "files" in spec:                      # public-file check: only the files of Sections 3 and 4
        expected_files = spec["files"]
    else:                                    # main analysis: every file listed in EXPECTED_OUTPUTS.md
        expected_files = [l.split("|")[1].strip().strip("`") for l in open(HERE / "EXPECTED_OUTPUTS.md")
                          if l.startswith("|") and "`" in l.split("|")[1]]
    ok = True
    missing = [f for f in expected_files if not (out / f).exists()]
    print(f"Expected files: {len(expected_files)}, missing: {len(missing)}")
    for f in missing:
        print("  MISSING", f); ok = False
    for c in spec["checks"]:
        p = out / c["file"]
        if not p.exists():
            print(f"  SKIP  {c['paper']}: {c['file']} not found"); ok = False; continue
        t = pd.read_csv(p, keep_default_na=False, na_values=["", "nan", "NaN"])
        for k, v in c["where"].items():
            t = t[t[k].astype(str) == str(v)]
        if len(t) != 1:
            print(f"  FAIL  {c['paper']}: {c['where']} matched {len(t)} rows in {c['file']}"); ok = False; continue
        if c["col"] not in t.columns:
            print(f"  FAIL  {c['paper']}: column {c['col']} not in {c['file']}"); ok = False; continue
        raw = t.iloc[0][c["col"]]
        val = float(str(raw).split("±")[0])
        good = abs(val - c["expected"]) <= c["tol"] + 1e-9
        ok &= good
        print(f"  {'OK  ' if good else 'FAIL'}  {c['paper']:<16} {c['file'].split('/')[-1]:<45} {c['col']:<18} "
              f"got {val:<10g} expected {c['expected']}")
    return ok

def compare(a, b):
    ma, mb = pd.read_csv(a / "MANIFEST.csv"), pd.read_csv(b / "MANIFEST.csv")
    ma, mb = [m[m.file.str.startswith("tables/")].set_index("file") for m in (ma, mb)]
    ok = True
    for f in sorted(set(ma.index) | set(mb.index)):
        if f not in ma.index or f not in mb.index:
            print("  ONLY IN ONE RUN", f); ok = False
        elif ma.loc[f, "sha256_without_timing"] != mb.loc[f, "sha256_without_timing"]:
            print("  DIFFERENT", f); ok = False
    print(f"{len(ma)} tables compared:", "identical" if ok else "differences found")
    return ok

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out"); ap.add_argument("--compare", nargs=2)
    ap.add_argument("--expected", default="expected_values.json",
                    help="expected_values.json (full 189-predictor file) or expected_values_public.json (public file)")
    a = ap.parse_args()
    if a.compare:
        sys.exit(0 if compare(*map(pathlib.Path, a.compare)) else 1)
    if not a.out:
        ap.error("give --out or --compare")
    res = check_values(pathlib.Path(a.out), a.expected)
    print("\nALL CHECKS PASSED" if res else "\nSOME CHECKS FAILED"); sys.exit(0 if res else 1)
