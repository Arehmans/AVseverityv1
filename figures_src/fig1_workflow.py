import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family":"DejaVu Sans"})
W,H=7.2,5.6
fig=plt.figure(figsize=(W,H)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")
INK="#1f2328"; MUTED="#5b6169"; BLUE="#2b6cb0"; BLUEF="#eaf2fb"; GREEN="#2f855a"; GREENF="#eaf6ef"; ORG="#b7791f"; GREYF="#f3f4f5"
FS=6.6; TF=7.2
def box(x,y,w,h,title,lines=(),ec=INK,tc=INK,fs=FS):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.01,rounding_size=0.05",fc="white",ec=ec,lw=0.9))
    ax.text(x+w/2,y+h-0.08,title,ha="center",va="top",fontsize=TF,fontweight="bold",color=tc)
    for i,l in enumerate(lines):
        ax.text(x+w/2,y+h-0.30-i*0.17,l,ha="center",va="top",fontsize=fs,color=INK)
def arr(x1,y1,x2,y2,c=INK,ls="-"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=8,color=c,lw=0.9,ls=ls,shrinkA=0,shrinkB=0))
def band(y,h,label,fc,ec):
    ax.add_patch(FancyBboxPatch((0.06,y),W-0.12,h,boxstyle="round,pad=0.01,rounding_size=0.08",fc=fc,ec=ec,lw=0.9))
    ax.text(0.14,y+h-0.06,label,ha="left",va="top",fontsize=7.4,fontweight="bold",color=ec)
# A
band(4.35,1.18,"A  Data and redundancy diagnosis",GREYF,MUTED)
box(0.18,4.45,2.1,0.8,"1. AV crash dataset",["California DMV, n = 324","189 predictors","Minor 237 · Moderate 52 · None 35"])
box(2.5,4.45,1.75,0.8,"2. Preprocessing",["Cleaning, encoding","Variable types recorded"])
box(4.47,4.45,2.55,0.8,"3. Redundancy diagnosis",["Euclidean vs Manhattan top-3",r"$O_i=|N_E(i)\cap N_M(i)|/3$; mean 0.762","MDST unique samples: 29.3%"])
arr(2.28,4.85,2.5,4.85); arr(4.25,4.85,4.47,4.85)
# B
band(1.5,2.75,"B  Protocol B: 10 repeats × 5-fold stratified CV; all steps fitted inside each training fold",BLUEF,BLUE)
box(0.18,3.0,1.1,0.85,"Training fold",["real records","only (~259)"],ec=BLUE)
box(0.18,1.62,1.1,0.85,"Test fold",["real records","only (~65)"],ec=BLUE)
box(1.48,3.0,0.95,0.85,"4. Scaler",["fitted on","training fold"],ec=BLUE)
box(2.63,3.0,0.95,0.85,"5. RFE-100",["linear SVM,","training fold"],ec=BLUE)
ax.add_patch(FancyBboxPatch((3.78,2.25),2.1,1.6,boxstyle="round,pad=0.01,rounding_size=0.05",fc="white",ec=ORG,lw=1.1))
ax.text(4.83,3.77,"6. Oversampling",ha="center",va="top",fontsize=TF,fontweight="bold",color=ORG)
for i,(l,b) in enumerate([("RA-MDST (proposed):",True),("3 Euclidean + 3 Manhattan-",False),("exclusive neighbors;",False),
                          (r"bounded pairwise interpolation",False),("RA-MDST-TP: valid discrete values",False)]):
    ax.text(4.83,3.55-i*0.17,l,ha="center",va="top",fontsize=FS,fontweight="bold" if b else "normal")
ax.plot([3.9,5.76],[2.68,2.68],color="#aaa",lw=0.5)
ax.text(4.83,2.63,"Comparators: MDST, ROS, SMOTE,",ha="center",va="top",fontsize=6.1,color=MUTED)
ax.text(4.83,2.46,"B-SMOTE, ADASYN, SMOTE-NC, none",ha="center",va="top",fontsize=6.1,color=MUTED)
box(6.05,3.0,0.97,0.85,"7. Classifier",["10 models"],ec=BLUE)
box(6.05,1.62,0.97,0.85,"8. Predict",["test fold","(real only)"],ec=BLUE)
arr(1.28,3.42,1.48,3.42,BLUE); arr(2.43,3.42,2.63,3.42,BLUE); arr(3.58,3.42,3.78,3.42,BLUE); arr(5.88,3.42,6.05,3.42,BLUE)
arr(6.535,3.0,6.535,2.47,BLUE)
arr(1.28,1.9,6.05,1.9,BLUE,"--")
ax.text(2.55,1.86,"transformed with training-fold scaler and features;",ha="center",va="top",fontsize=6.0,color=BLUE)
ax.text(2.55,1.70,"never used for fitting or oversampling",ha="center",va="top",fontsize=6.0,color=BLUE)
arr(0.73,4.45,0.73,3.85,MUTED)
# C
band(0.06,1.36,"C  Analysis (all claims based on Protocol B)",GREENF,GREEN)
box(0.18,0.16,2.2,0.95,"Predictive performance",["accuracy, macro-F1, balanced","accuracy, QWK; corrected tests,","Holm, 95% CI, effect sizes"],ec=GREEN)
box(2.5,0.16,2.2,0.95,"Synthetic-data quality",["uniqueness, near-duplicates,","spread, intrusion,","invalid values"],ec=GREEN)
box(4.82,0.16,2.2,0.95,"Robustness",["ablation, sensitivity, nested CV,","partial balancing, ordinal,","SHAP, 6 benchmarks"],ec=GREEN)
arr(6.535,1.62,6.535,1.42,GREEN); arr(4.3,2.25,4.3,1.42,ORG)
fig.savefig("Fig1_workflow_protocolB.pdf"); fig.savefig("Fig1_workflow_protocolB.png",dpi=300)
