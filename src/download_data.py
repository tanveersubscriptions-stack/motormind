"""
download_data.py

Downloads the PhysioNet EEG Motor Movement/Imagery Dataset (eegbci) using
MNE's built-in fetcher. This dataset is public, de-identified, and free to
use for research and teaching -- no IRB approval needed on your end since
the original collection was already IRB-approved and the data is openly
released for reuse (cite it -- see README.md).

Dataset reference:
Goldberger AL, Amaral LAN, Glass L, et al. PhysioBank, PhysioToolkit, and
PhysioNet: Components of a New Research Resource for Complex Physiologic
Signals. Circulation. 2000.

Schalk G, McFarland DJ, Hinterberger T, Birbaumer N, Wolpaw JR.
BCI2000: A General-Purpose Brain-Computer Interface (BCI) System.
IEEE Transactions on Biomedical Engineering. 2004.

Usage:
    python src/download_data.py --subjects 1 2 3 4 5

If you omit --subjects, it downloads the first 20 subjects (a reasonable
sample for a passion project -- the full set is 109 subjects and is large).
"""

import argparse
from mne.datasets import eegbci


def main():
    parser = argparse.ArgumentParser(description="Download PhysioNet EEGMMIDB data")
    parser.add_argument(
        "--subjects",
        type=int,
        nargs="+",
        default=list(range(1, 21)),
        help="Subject numbers to download (1-109). Default: subjects 1-20.",
    )
    # Runs 4, 8, 12 = imagined LEFT vs RIGHT fist
    # Runs 6, 10, 14 = imagined BOTH FISTS vs BOTH FEET
    parser.add_argument(
        "--runs",
        type=int,
        nargs="+",
        default=[4, 8, 12, 6, 10, 14],
        help="Which experimental runs to download per subject.",
    )
    args = parser.parse_args()

    print(f"Downloading {len(args.subjects)} subjects, runs {args.runs} ...")
    for subj in args.subjects:
        paths = eegbci.load_data(subj, args.runs, path="data/raw", update_path=True)
        print(f"  Subject {subj:03d}: {len(paths)} files -> data/raw/")

    print("\nDone. Raw .edf files are in data/raw/")
    print("Next step: python src/preprocess.py")


if __name__ == "__main__":
    main()
