# MotorMind: An Open-Source Motor-Imagery Brain-Computer Interface Built on Public EEG Data

**Author(s):** [Your name] — [your affiliation, or "Independent researcher" if none]

**Status:** Draft — fill in bracketed sections once `src/train_model.py` has
been run on real data. Do not post this publicly until every `[TODO]` below
is replaced with real numbers from your own run.

---

## Abstract

[150-250 words. Write this last, once the rest of the paper is done. State
the question, the method in one sentence, the headline result (mean
accuracy vs. chance), and one sentence on why it matters.]

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
[N] subjects ([list which, or "subjects 1-20"]) and [N] trials per class
per subject.

### 3.2 Preprocessing

Raw recordings were band-pass filtered between 7-30 Hz to isolate the mu
and beta sensorimotor rhythms. Epochs were extracted from -1 s to +4 s
relative to each movement cue. [State here if you changed these defaults,
and why.]

### 3.3 Feature extraction and classification

We used Common Spatial Patterns (CSP; Ramoser, Muller-Gerking, &
Pfurtscheller, 2000) with [N] components and Ledoit-Wolf shrinkage
regularization to extract spatial filters that maximize variance
differences between classes, followed by Linear Discriminant Analysis
(LDA) for classification.

### 3.4 Evaluation

Models were trained and evaluated per subject using [k]-fold stratified
cross-validation, with accuracy averaged across subjects. Chance level for
this 3-class problem is 33.3%.

## 4. Results

[TODO — fill in once you've run src/train_model.py on real data]

- Mean cross-subject accuracy: **[X]%** (chance = 33.3%)
- Per-class precision/recall: [table or summary]
- Confusion matrix: see `web/assets/figures/confusion_matrix.png`
- CSP spatial patterns: see `web/assets/figures/csp_patterns.png` —
  [describe what scalp regions the patterns highlight, e.g. "centro-parietal
  electrodes contralateral to the imagined hand," only if that's what you
  actually observe]
- Variation across subjects: [note the spread — motor-imagery BCIs are
  known to vary a lot by subject; don't smooth this over]

## 5. Discussion

[1-2 paragraphs interpreting the results honestly. How does the accuracy
compare to chance and to typical published CSP+LDA results on this dataset
(often cited in the 60-80% range for 2-class problems — verify against
your own sources rather than asserting a number from memory)? What does
the per-subject variation suggest about generalizability?]

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
