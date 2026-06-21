"""
train_model.py

Trains the classic motor-imagery BCI pipeline (Common Spatial Patterns +
Linear Discriminant Analysis) on the preprocessed epochs, evaluates it
with cross-validation, and exports two things:

  1. web/assets/figures/  - confusion matrix + CSP spatial pattern plots
  2. web/data/results.json - everything the website needs to render the
     "Results" section and the live in-browser demo (model accuracy,
     per-subject scores, and a handful of example trials with their
     true/predicted labels and confidence scores).

CSP + LDA reference:
Ramoser H, Muller-Gerking J, Pfurtscheller G. Optimal spatial filtering of
single trial EEG during imagined hand movement. IEEE Trans Rehabil Eng. 2000.

Usage:
    python src/train_model.py
"""

import glob
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mne
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report

CLASS_NAMES = ["left_fist", "right_fist", "both_feet"]
LABEL_MAP = {"left_fist": 0, "right_fist": 1, "both_feet": 2}
DEMO_CHANNEL_CANDIDATES = ["C3", "Cz", "C4"]
N_DEMO_TRIALS_PER_CLASS = 3
N_TRACE_POINTS = 150


def load_subject(path):
    epochs = mne.read_epochs(path, preload=True, verbose=False)
    inv_event_id = {v: k for k, v in epochs.event_id.items()}
    y = np.array([LABEL_MAP[inv_event_id[code]] for code in epochs.events[:, 2]])
    X = epochs.get_data(copy=False)
    return epochs, X, y


def build_pipeline():
    csp = CSP(n_components=6, reg="ledoit_wolf", log=True, norm_trace=False)
    lda = LinearDiscriminantAnalysis()
    return Pipeline([("CSP", csp), ("LDA", lda)])


def downsample_trace(channel_data, n_points=N_TRACE_POINTS):
    idx = np.linspace(0, len(channel_data) - 1, n_points).astype(int)
    trace = channel_data[idx]
    trace = (trace - trace.mean()) / (trace.std() + 1e-9)
    return [round(float(v), 3) for v in trace]


def main():
    os.makedirs("web/assets/figures", exist_ok=True)
    os.makedirs("web/data", exist_ok=True)

    subject_files = sorted(glob.glob("data/processed/subj*-epo.fif"))
    if not subject_files:
        raise SystemExit(
            "No processed epochs found in data/processed/. "
            "Run src/download_data.py then src/preprocess.py first."
        )

    pipeline = build_pipeline()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    per_subject_acc = []
    best_subject = {"id": None, "acc": -1, "epochs": None, "X": None, "y": None}
    all_y_true_pooled, all_y_pred_pooled = [], []

    for path in subject_files:
        subj_id = os.path.basename(path).replace("-epo.fif", "")
        epochs, X, y = load_subject(path)

        if len(np.unique(y)) < 3 or len(y) < 15:
            print(f"  Skipping {subj_id}: not enough trials/classes ({len(y)} trials)")
            continue

        scores = cross_val_score(pipeline, X, y, cv=cv, n_jobs=1)
        acc = scores.mean()
        per_subject_acc.append({"subject": subj_id, "accuracy": round(float(acc), 4),
                                 "n_trials": int(len(y))})
        print(f"  {subj_id}: {acc:.3f} accuracy over {len(y)} trials")

        y_pred = cross_val_predict(pipeline, X, y, cv=cv, n_jobs=1)
        all_y_true_pooled.extend(y.tolist())
        all_y_pred_pooled.extend(y_pred.tolist())

        if acc > best_subject["acc"]:
            best_subject.update({"id": subj_id, "acc": acc, "epochs": epochs, "X": X, "y": y})

    if not per_subject_acc:
        raise SystemExit("No subject had usable data. Check preprocessing step.")

    mean_acc = float(np.mean([s["accuracy"] for s in per_subject_acc]))
    n_trials_total = int(sum(s["n_trials"] for s in per_subject_acc))

    # --- Confusion matrix (pooled across all subjects' out-of-fold predictions) ---
    # Wrapped in try/except: a plotting failure here should never block results.json,
    # which is the output that actually matters for the website.
    try:
        cm = confusion_matrix(all_y_true_pooled, all_y_pred_pooled, labels=[0, 1, 2])
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(cm, cmap="Blues")
        ax.set_xticks(range(3)); ax.set_xticklabels(CLASS_NAMES, rotation=30, ha="right")
        ax.set_yticks(range(3)); ax.set_yticklabels(CLASS_NAMES)
        ax.set_xlabel("Predicted"); ax.set_ylabel("True")
        for i in range(3):
            for j in range(3):
                ax.text(j, i, str(cm[i, j]), ha="center", va="center")
        fig.tight_layout()
        fig.savefig("web/assets/figures/confusion_matrix.png", dpi=150)
        plt.close(fig)
        print("Wrote web/assets/figures/confusion_matrix.png")
    except Exception as e:
        print(f"  Warning: could not generate confusion matrix figure ({e}); continuing.")

    report = classification_report(all_y_true_pooled, all_y_pred_pooled,
                                    target_names=CLASS_NAMES, output_dict=True)

    # --- CSP spatial patterns, fit on the best subject (for the figure only) ---
    # Plotted via the low-level csp.patterns_ array + plot_topomap directly, rather
    # than CSP.plot_patterns(), since that wrapper's internals have changed across
    # MNE versions and can break depending on what's installed.
    best_pipeline = build_pipeline()
    best_pipeline.fit(best_subject["X"], best_subject["y"])
    csp = best_pipeline.named_steps["CSP"]
    try:
        from mne.viz import plot_topomap
        patterns = csp.patterns_  # shape (n_components, n_channels)
        n_plot = min(6, patterns.shape[0])
        fig, axes = plt.subplots(1, n_plot, figsize=(2.3 * n_plot, 2.6))
        if n_plot == 1:
            axes = [axes]
        for i in range(n_plot):
            plot_topomap(patterns[i], best_subject["epochs"].info, axes=axes[i], show=False)
            axes[i].set_title(f"CSP {i+1}", fontsize=10)
        fig.tight_layout()
        fig.savefig("web/assets/figures/csp_patterns.png", dpi=150)
        plt.close(fig)
        print("Wrote web/assets/figures/csp_patterns.png")
    except Exception as e:
        print(f"  Warning: could not generate CSP patterns figure ({e}); continuing.")

    # --- Demo trials for the website (drawn from the best-performing subject) ---
    demo_epochs, demo_X, demo_y = best_subject["epochs"], best_subject["X"], best_subject["y"]
    demo_pred = cross_val_predict(build_pipeline(), demo_X, demo_y, cv=cv, n_jobs=1)
    # decision_function-based pseudo-probabilities via softmax over LDA scores
    proba_pipeline = build_pipeline()
    proba_pipeline.fit(demo_X, demo_y)

    ch_names = demo_epochs.info["ch_names"]
    demo_channel = next((c for c in DEMO_CHANNEL_CANDIDATES if c in ch_names), ch_names[0])
    ch_idx = ch_names.index(demo_channel)

    demo_trials = []
    for class_id in [0, 1, 2]:
        class_indices = np.where(demo_y == class_id)[0][:N_DEMO_TRIALS_PER_CLASS]
        for idx in class_indices:
            probs = proba_pipeline.named_steps["LDA"].predict_proba(
                proba_pipeline.named_steps["CSP"].transform(demo_X[idx:idx + 1])
            )[0]
            demo_trials.append({
                "id": f"{best_subject['id']}_trial{int(idx)}",
                "channel": demo_channel,
                "true_label": CLASS_NAMES[class_id],
                "predicted_label": CLASS_NAMES[int(demo_pred[idx])],
                "confidence": {CLASS_NAMES[i]: round(float(probs[i]), 3) for i in range(3)},
                "trace": downsample_trace(demo_X[idx, ch_idx, :]),
            })

    results = {
        "generated_from": "real_pipeline",
        "model": "CSP(6 components) + LDA",
        "frequency_band_hz": [7, 30],
        "chance_level": round(1 / 3, 3),
        "mean_accuracy": round(mean_acc, 4),
        "n_subjects": len(per_subject_acc),
        "n_trials_total": n_trials_total,
        "per_subject_accuracy": per_subject_acc,
        "classification_report": report,
        "demo_subject": best_subject["id"],
        "demo_channel": demo_channel,
        "demo_trials": demo_trials,
    }

    with open("web/data/results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nMean cross-subject accuracy: {mean_acc:.3f} (chance = 0.333)")
    print("Wrote web/data/results.json")
    print("Wrote web/assets/figures/confusion_matrix.png and csp_patterns.png")
    print("\nNext: open web/index.html and paste the contents of web/data/results.json")
    print("into the RESULTS constant near the top of the <script> tag (see README).")


if __name__ == "__main__":
    main()
