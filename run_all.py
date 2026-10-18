#!/usr/bin/env python3
"""Regenerate every table and figure of the RA-MDST article with one command.

    python run_all.py --data data/NN_MissingHandlingdataset.csv            # full run (paper numbers, ~60-90 min on 4 cores)
    python run_all.py --data data/NN_MissingHandlingdataset.csv --quick    # smoke test (~5 min)
    python run_all.py --data ... --sections 3,4                            # regenerate selected sections only
    python run_all.py --data ... --fresh                                   # ignore checkpoints, recompute everything

The notebook RA_MDST_revision.ipynb is executed headless; outputs go to --out (default: revision_results/).
After a full run, verify_outputs.py checks every expected file and the key values reported in the article.
"""
import argparse, os, subprocess, sys, time, pathlib

HERE = pathlib.Path(__file__).resolve().parent
NB = HERE / "RA_MDST_revision.ipynb"

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="path to NN_MissingHandlingdataset.csv")
    ap.add_argument("--out", default=str(HERE / "revision_results"), help="output folder")
    ap.add_argument("--quick", action="store_true", help="fast smoke test (QUICK mode; numbers differ from the paper)")
    ap.add_argument("--sections", default="", help="comma-separated section numbers, e.g. 3,4 (default: all 1-14)")
    ap.add_argument("--fresh", action="store_true", help="do not reuse checkpoints from a previous run")
    ap.add_argument("--no-verify", action="store_true", help="skip verify_outputs.py after a full run")
    a = ap.parse_args()

    env = dict(os.environ)
    env["RA_MDST_DATA"] = str(pathlib.Path(a.data).resolve())
    env["RA_MDST_OUT"] = str(pathlib.Path(a.out).resolve())
    env["RA_MDST_MODE"] = "QUICK" if a.quick else "FULL"
    env["RA_MDST_RESUME"] = "0" if a.fresh else "1"
    if a.sections:
        secs = sorted({int(s) for s in a.sections.split(",")} | {14})   # 14 = summary, manifest, zip
        env["RA_MDST_SECTIONS"] = ",".join(map(str, secs))
    os.makedirs(env["RA_MDST_OUT"], exist_ok=True)
    executed = pathlib.Path(env["RA_MDST_OUT"]) / "RA_MDST_revision_executed.ipynb"
    cmd = [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", str(NB),
           "--output", str(executed), "--ExecutePreprocessor.timeout=-1", "--ExecutePreprocessor.kernel_name=python3"]
    print("Running:", " ".join(cmd)); print("Mode:", env["RA_MDST_MODE"], "| output:", env["RA_MDST_OUT"])
    t0 = time.time()
    rc = subprocess.call(cmd, env=env, cwd=HERE)
    print(f"Notebook finished with exit code {rc} in {(time.time() - t0) / 60:.1f} min")
    if rc != 0:
        sys.exit(rc)
    err = pathlib.Path(env["RA_MDST_OUT"]) / "ERRORS.txt"
    if err.exists():
        print("Some sections failed; see", err)
    if not a.quick and not a.no_verify and not a.sections:
        sys.exit(subprocess.call([sys.executable, str(HERE / "verify_outputs.py"), "--out", env["RA_MDST_OUT"]]))

if __name__ == "__main__":
    main()
