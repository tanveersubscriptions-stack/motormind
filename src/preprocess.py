"""
preprocess.py

Turns raw PhysioNet EEGMMIDB .edf recordings into clean, labeled epochs
ready for classification.

Pipeline:
  1. Load each subject's raw recordings for the motor-imagery runs.
  2. Standardize channel names and set the standard 10-10 montage.
  3. Band-pass filter 7-30 Hz (covers the mu and beta rhythms that
     change power during imagined movement -- this is the classic
     frequency band used in motor-imagery BCI research).
  4. Epoch around each cue (-1s to +4s) and label by imagined class:
       0 = left fist
       1 = right fist
       2 = both feet
     (We drop the "both fists" condition to keep this a clean 3-class
     problem; you can add it back in by editing EVENT_ID below.)
  5. Save one epochs file per subject to data/processed/

Usage:
    python src/preprocess.py --subjects 1 2 3 4 5
"""

import argparse
import os
import mne
from mne.datasets import eegbci

# Runs 4/8/12 alternate left-fist (event 'T1') vs right-fist (event 'T2').
# Runs 6/10/14 alternate both-fists (event 'T1') vs both-feet (event 'T2').
LEFT_RIGHT_RUNS = [4, 8, 12]
FEET_RUNS = [6, 10, 14]

EVENT_ID_LR = {"left_fist": 1, "right_fist": 2}       # T1, T2 in left/right runs
EVENT_ID_FEET = {"both_feet": 3}                       # T2 in feet runs

TMIN, TMAX = -1.0, 4.0
FILTER_LOW, FILTER_HIGH = 7.0, 30.0


def load_subject_epochs(subject):
    """Load and epoch one subject's left/right/feet imagery trials."""
    all_epochs = []

    # --- Left vs right fist runs ---
    raw_fnames = eegbci.load_data(subject, LEFT_RIGHT_RUNS, path="data/raw")
    raws = [mne.io.read_raw_edf(f, preload=True) for f in raw_fnames]
    raw = mne.concatenate_raws(raws)
    eegbci.standardize(raw)
    raw.set_montage("standard_1005", on_missing="ignore")
    raw.filter(FILTER_LOW, FILTER_HIGH, fir_design="firwin", skip_by_annotation="edge")

    # T1 -> left_fist (code 1), T2 -> right_fist (code 2)
    events, _ = mne.events_from_annotations(raw, event_id=dict(T1=1, T2=2))
    epochs_lr = mne.Epochs(
        raw, events, event_id=EVENT_ID_LR, tmin=TMIN, tmax=TMAX,
        baseline=None, preload=True, picks="eeg",
    )
    all_epochs.append(epochs_lr)

    # --- Both feet runs (we only keep the feet condition, T2) ---
    raw_fnames = eegbci.load_data(subject, FEET_RUNS, path="data/raw")
    raws = [mne.io.read_raw_edf(f, preload=True) for f in raw_fnames]
    raw = mne.concatenate_raws(raws)
    eegbci.standardize(raw)
    raw.set_montage("standard_1005", on_missing="ignore")
    raw.filter(FILTER_LOW, FILTER_HIGH, fir_design="firwin", skip_by_annotation="edge")

    # T1 -> "both fists" (unwanted, dumped on throwaway code 99), T2 -> both_feet (code 3).
    # Codes must not collide with 1/2 above or concatenation silently drops a class.
    events, _ = mne.events_from_annotations(raw, event_id=dict(T1=99, T2=3))
    epochs_feet = mne.Epochs(
        raw, events, event_id=EVENT_ID_FEET, tmin=TMIN, tmax=TMAX,
        baseline=None, preload=True, picks="eeg",
    )
    all_epochs.append(epochs_feet)

    combined = mne.concatenate_epochs(all_epochs)
    return combined


def main():
    parser = argparse.ArgumentParser(description="Preprocess PhysioNet EEGMMIDB data")
    parser.add_argument("--subjects", type=int, nargs="+", default=list(range(1, 21)))
    args = parser.parse_args()

    os.makedirs("data/processed", exist_ok=True)

    for subj in args.subjects:
        print(f"Processing subject {subj:03d} ...")
        try:
            epochs = load_subject_epochs(subj)
            out_path = f"data/processed/subj{subj:03d}-epo.fif"
            epochs.save(out_path, overwrite=True)
            print(f"  Saved {len(epochs)} epochs -> {out_path}")
        except Exception as e:
            print(f"  Skipped subject {subj:03d}: {e}")

    print("\nDone. Next step: python src/train_model.py")


if __name__ == "__main__":
    main()
