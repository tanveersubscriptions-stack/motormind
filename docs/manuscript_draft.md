# MotorMind: An Open-Source Motor-Imagery Brain-Computer Interface Built on Public EEG Data

**Author(s):** Tanveer Gouse Sayyad — Independent researcher

**Status:** Results and abstract are filled in with real numbers from a
20-subject run. Two things still need your input before this is ready to
post: (1) your name above, and (2) the CSP spatial patterns description in
Results — look at `web/assets/figures/csp_patterns.png` yourself and
describe what you actually see, since that's not something to guess at.

---

## Abstract

Brain-computer interfaces (BCIs) that decode imagined movement from EEG
underpin assistive technologies for people with paralysis or locked-in
syndrome, but most published implementations require specialized hardware
or institutional resources. This project builds and evaluates a classic
motor-imagery BCI pipeline — Common Spatial Patterns (CSP) combined with
Linear Discriminant Analysis (LDA) — entirely from public data and
open-source tools, with no lab access or EEG hardware required. Using 20
subjects (1,349 trials) from the PhysioNet EEG Motor Movement/Imagery
Dataset, the pipeline classified imagined left-hand, right-hand, and
foot movement with 54.9% mean cross-subject accuracy against a 33.3%
chance baseline. Performance was uneven: both-feet trials were decoded
reliably (~73% precision/recall), while left- and right-hand trials were
frequently confused with each other (~46-56%), consistent with the close
cortical proximity of the two hands' motor representations. Per-subject
accuracy ranged widely, from 31.9% to 81.3%, underscoring that
motor-imagery BCI performance is highly individual-dependent even with
identical preprocessing. All code, data-processing scripts, and an
interactive demo are released openly to support reuse and verification.

## 1. Introduction

Brain-computer interfaces (BCIs) that decode imagined movement from EEG are
a foundational technology for restoring communication and control to people
with paralysis or locked-in syndrome — conditions where the intention to
move is preserved even though the connection to the limb is not. The
underlying decoding problem — distinguishing which movement a person is
imagining, purely from scalp EEG — has a long research history built
heavily on a small number of open datasets.

This project asks a narrower, achievable version of that question:
**can a classic, lightweight signal-processing pipeline (Common Spatial
Patterns + Linear Discriminant Analysis), built from scratch with no
specialized hardware, reliably distinguish imagined left-hand, right-hand,
and feet movement using a public dataset?**

## 2. Related work

[Optional but strengthens the paper. 1-2 paragraphs summarizing 2-4 prior
motor-imagery BCI papers and how this project's approach compares —
e.g., CSP+LDA as a classic baseline vs. more recent deep-learning approaches
like EEGNet. Keep claims about other papers paraphrased in your own words,
not quoted.]

## 3. Methods

### 3.1 Dataset

We used the PhysioNet EEG Motor Movement/Imagery Dataset (Goldberger et al.,
2000; Schalk et al., 2004), a public, de-identified dataset of 64-channel
EEG recordings from 109 subjects performing and imagining left fist, right
fist, and both-feet movements, cued by an on-screen target. We used
20 subjects (subjects 1-20) and 1,349 trials total across all three
classes (left fist: 455, right fist: 445, both feet: 449).

### 3.2 Preprocessing

Raw recordings were band-pass filtered between 7-30 Hz to isolate the mu
and beta sensorimotor rhythms. Epochs were extracted from -1 s to +4 s
relative to each movement cue. [State here if you changed these defaults,
and why.]

### 3.3 Feature extraction and classification

We used Common Spatial Patterns (CSP; Ramoser, Muller-Gerking, &
Pfurtscheller, 2000) with 6 components and Ledoit-Wolf shrinkage
regularization to extract spatial filters that maximize variance
differences between classes, followed by Linear Discriminant Analysis
(LDA) for classification.

### 3.4 Evaluation

Models were trained and evaluated per subject using 5-fold stratified
cross-validation, with accuracy averaged across subjects. Chance level for
this 3-class problem is 33.3%.

## 4. Results

- **Mean cross-subject accuracy: 54.9%** (chance = 33.3%), pooled accuracy
  across all held-out folds: 55.1%.
- **Per-class performance** (precision / recall / F1):
  - Left fist: 0.456 / 0.475 / 0.465 (n=455)
  - Right fist: 0.466 / 0.463 / 0.464 (n=445)
  - Both feet: 0.741 / 0.715 / 0.728 (n=449)
- Confusion matrix: see `web/assets/figures/confusion_matrix.png`
- CSP spatial patterns: see `web/assets/figures/csp_patterns.png` —
  [look at your generated figure and describe what scalp regions the
  top components actually highlight; don't guess without looking]
- **Variation across subjects** was substantial: per-subject accuracy
  ranged from 31.9% (subject 19, below chance) to 81.3% (subject 1),
  with several subjects clustered close to chance (subjects 13, 19, and
  20 all below 36%) and several well above 70% (subjects 1, 7, 8, 11).
  This spread is large enough that the mean alone is a misleading summary
  of how well the pipeline works for any given individual.

## 5. Discussion

The model performs clearly above chance overall (54.9% vs. 33.3% on a
3-class problem), confirming that CSP+LDA recovers a real, decodable
signal from this dataset without any subject-specific tuning beyond
per-subject cross-validation. The result is not uniform across classes,
however: both-feet trials are detected substantially more reliably
(~73% precision/recall) than left-fist or right-fist trials, which are
frequently confused with each other (~46-56%). This is consistent with
the underlying neurophysiology — the cortical hand representations for
the left and right hand sit close together along the motor homunculus,
so the spatial EEG signature distinguishing them is inherently subtler
than the signature distinguishing hand movement from foot movement,
which originates from a more distant cortical region.

The per-subject spread (31.9%-81.3%) is at least as important a finding
as the mean accuracy. A handful of subjects performed at or below chance
despite identical preprocessing and modeling choices, which is a
well-documented phenomenon in the motor-imagery BCI literature sometimes
called "BCI illiteracy" — some individuals' EEG simply doesn't show a
strong, consistent imagined-movement signature with standard methods,
for reasons that aren't fully understood. This means a single
cross-subject accuracy number, on its own, overstates how reliably this
pipeline would work for any one new user without first checking whether
they're a "low-performing" subject.

## 6. Limitations

- This is a single from-scratch pipeline, not a systematic comparison
  against other published methods.
- The dataset's imagined-movement labels rely on subjects' self-reported
  compliance with the cue; there's no independent verification they were
  actually imagining the correct movement throughout each trial.
- Results are evaluated within-subject; no claims are made about a
  model trained on one person generalizing to a new person without
  recalibration.
- [Add your own — e.g. number of subjects used, channels excluded, etc.]

## 7. Future work

[Optional. E.g.: comparing CSP+LDA against a deep learning baseline like
EEGNet; testing cross-subject transfer; collecting a small amount of real
pilot data with a research-grade EEG system, if a mentorship connection
makes that possible.]

## References

Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PC, Mark RG,
Mietus JE, Moody GB, Peng CK, Stanley HE. PhysioBank, PhysioToolkit, and
PhysioNet: Components of a New Research Resource for Complex Physiologic
Signals. *Circulation*. 2000;101(23):e215-e220.

Schalk G, McFarland DJ, Hinterberger T, Birbaumer N, Wolpaw JR. BCI2000:
A General-Purpose Brain-Computer Interface (BCI) System. *IEEE Transactions
on Biomedical Engineering*. 2004;51(6):1034-1043.

Ramoser H, Muller-Gerking J, Pfurtscheller G. Optimal spatial filtering of
single trial EEG during imagined hand movement. *IEEE Transactions on
Rehabilitation Engineering*. 2000;8(4):441-446.

Gramfort A, Luessi M, Larson E, Engemann DA, Strohmeier D, Brodbeck C,
Goj R, Jas M, Brooks T, Parkkonen L, Hamalainen M. MEG and EEG data
analysis with MNE-Python. *Frontiers in Neuroscience*. 2013;7:267.

---

### Notes for posting to OSF Preprints

- OSF Preprints (osf.io/preprints) requires no institutional affiliation —
  list yourself as an independent researcher if that's accurate.
- You'll need a short plain-language summary in addition to the abstract;
  reuse the "Why this project" section of the README for that.
- Link the GitHub repo from the preprint so reviewers/readers can verify
  and rerun everything.
