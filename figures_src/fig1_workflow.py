import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib import font_manager as fm

plt.rcParams.update({"font.family": "Liberation Serif",      # Times-metric TrueType font (matches the article text)
                     "mathtext.fontset": "stix", "pdf.fonttype": 42})

W, H = 6.37, 4.75                       # inches = printed size (text width of the article)
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
K = "#000000"; G = "#e6e6e6"; LW = 0.8
FS, FT = 9, 9.5                          # body / box-title font size in points

def box(x, y, w, h, title=None, lines=(), fill="white", fs=FS, bold_title=True, dy=0.155):
    ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=K, lw=LW))
    n = (1 if title else 0) + len(lines)
    y0 = y + h / 2 + (n - 1) * dy / 2
    if title:
        ax.text(x + w / 2, y0, title, ha="center", va="center", fontsize=FT, fontweight="bold" if bold_title else "normal")
        y0 -= dy
    for l in lines:
        ax.text(x + w / 2, y0, l, ha="center", va="center", fontsize=fs); y0 -= dy

def arrow(x1, y1, x2, y2, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7, lw=LW, color=K,
                                 linestyle=ls, shrinkA=0, shrinkB=0))

# ---- row 1: data and descriptive diagnosis
y1, h1 = 3.92, 0.72
box(0.05, y1, 1.85, h1, "AV crash reports", ["California DMV, $n$ = 324", "189 predictors, 3 classes"])
box(2.15, y1, 1.45, h1, "Preprocessing", ["encoding;", "variable types"])
box(3.85, y1, 2.47, h1, "Redundancy diagnosis", ["Euclidean vs Manhattan top-3", r"neighbors; overlap $O_i$ (mean 0.76)"])
arrow(1.90, y1 + h1 / 2, 2.15, y1 + h1 / 2); arrow(3.60, y1 + h1 / 2, 3.85, y1 + h1 / 2)

# ---- Protocol B frame
fx, fy, fw, fh = 0.05, 1.18, 6.27, 2.48
ax.add_patch(Rectangle((fx, fy), fw, fh, fc="none", ec=K, lw=LW, ls=(0, (4, 2))))
ax.text(fx + fw - 0.08, fy + 0.13, "Protocol B: repeated for 50 outer folds (10 × 5-fold CV); every step is fitted on the training fold only",
        ha="right", va="center", fontsize=FS - 0.5, style="italic")
arrow(0.975, y1, 0.975, 3.24)

yt, ht = 2.62, 0.62                       # training path
box(0.30, yt, 1.35, ht, "Training fold", ["real records only"])
box(1.83, yt, 0.92, ht, "Standardize", [])
box(2.93, yt, 0.92, ht, "RFE", ["100 features"])
box(5.27, yt, 0.95, ht, "Classifier", ["10 models"])
arrow(1.65, yt + ht / 2, 1.83, yt + ht / 2); arrow(2.75, yt + ht / 2, 2.93, yt + ht / 2)

# oversampling step (the proposed method, light grey)
ox, ow, oh = 4.03, 1.06, 0.98
oy = yt + ht / 2 - oh / 2
ax.add_patch(Rectangle((ox, oy), ow, oh, fc=G, ec=K, lw=LW))
for i, (l, bold) in enumerate([("Oversample", True), ("RA-MDST or", False), ("RA-MDST-TP", False), ("(or a comparator)", False)]):
    ax.text(ox + ow / 2, oy + oh - 0.17 - i * 0.215, l, ha="center", va="center",
            fontsize=FT if bold else (FS - 0.5 if i == 3 else FS), fontweight="bold" if bold else "normal")
arrow(3.85, yt + ht / 2, ox, yt + ht / 2); arrow(ox + ow, yt + ht / 2, 5.27, yt + ht / 2)

yv = 1.42                                  # test path
box(0.30, yv, 1.35, ht, "Test fold", ["real records only"])
box(5.27, yv, 0.95, ht, "Predict", [])
arrow(5.745, yt, 5.745, yv + ht)
ax.annotate("", xy=(5.27, yv + ht / 2), xytext=(1.65, yv + ht / 2),
            arrowprops=dict(arrowstyle="-|>", mutation_scale=7, lw=LW, color=K, linestyle=(0, (3, 2)), shrinkA=0, shrinkB=0))
ax.text(3.46, yv + ht / 2 + 0.12, "scaled and reduced with the training-fold parameters;", ha="center", va="center", fontsize=FS - 0.5)
ax.text(3.46, yv + ht / 2 - 0.12, "never used for fitting or oversampling", ha="center", va="center", fontsize=FS - 0.5)

# ---- evaluation row
ye, he = 0.05, 0.86
box(0.05, ye, 2.00, he, "Prediction", ["macro-F1, balanced accuracy,", "corrected tests (Holm)"])
box(2.185, ye, 2.00, he, "Synthetic data", ["validity, duplicates,", "diversity, intrusion"])
box(4.32, ye, 2.00, he, "Robustness", ["ablation, sensitivity,", "nested CV, benchmarks"])
# one bracket from the fold loop to the three evaluation boxes
xb = 3.185
ax.plot([xb, xb], [fy, 1.03], color=K, lw=LW)
ax.plot([1.05, 5.32], [1.03, 1.03], color=K, lw=LW)
for xc in (1.05, 3.185, 5.32):
    arrow(xc, 1.03, xc, ye + he)
ax.text(xb + 0.06, 1.10, "fold-level results", ha="left", va="center", fontsize=FS - 0.5, style="italic")

for ext, kw in (("pdf", {}), ("png", {"dpi": 300})):
    fig.savefig(f"Fig1_workflow_protocolB.{ext}", **kw)
