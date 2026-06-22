# MotorMind: An Open-Source Motor-Imagery Brain-Computer Interface Built on Public EEG Data

**Author(s):** Tanveer Sayyad — Independent researcher

**Status:** Complete draft

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

Motor-imagery BCI research has been shaped significantly by the
availability of the PhysioNet dataset used here. The classic approach —
Common Spatial Patterns combined with a linear classifier — was
established by Ramoser, Muller-Gerking, and Pfurtscheller (2000) and
has remained a strong baseline for decades. CSP works by finding spatial
filters that maximize the ratio of EEG signal variance between imagined
movement classes, making it well-suited to the lateralized power changes
in the mu (8-12 Hz) and beta (13-30 Hz) bands that accompany motor
imagery. On this same dataset in 2-class (left vs. right hand)
configurations, published CSP+LDA results typically range from around
60-80% accuracy, with substantial variation across subjects.

More recent work has explored deep learning approaches. Lawhern et al.
(2018) introduced EEGNet, a compact convolutional neural network designed
specifically for EEG classification that generalizes across BCI paradigms
without extensive preprocessing. EEGNet and related architectures have
shown competitive or superior performance to CSP+LDA on some datasets,
particularly when sufficient training data is available. The present work
does not compare directly against these methods; CSP+LDA was chosen as a
transparent, well-understood baseline that is straightforward to implement
and interpret from a neuroscience standpoint. A comparison against EEGNet
on this dataset is a natural direction for future work.

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
relative to each movement cue. Default parameters were used without
modification.

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
- CSP spatial patterns (see `web/assets/figures/csp_patterns.png`): The
  first three components (CSP 1–3) are left-lateralized, with CSP 1
  showing a focal peak in the left frontal region and CSP 2–3 showing
  strong activation centered over the left central-parietal area near
  electrode C3 — the scalp position overlying the left motor cortex,
  which controls the contralateral (right) hand. CSP 4 and 5 show
  bilateral focal spots: a sharp peak in the right central-parietal
  region (near CP4/P4) and a complementary focus in the left central
  region (near C3/CP3), consistent with the model learning the spatial
  contrast between left- and right-hand cortical representations. CSP 6
  is more diffuse and bilateral, suggesting it captures noise or
  artifact variance rather than a clean motor signal.
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
- Only 20 of the 109 available subjects were used, which limits the
  generalizability of the cross-subject accuracy estimate.
- No artifact rejection was applied beyond the band-pass filter;
  ocular and muscle artifacts may have contributed noise to some trials.

## 7. Future work

The most natural next step is a direct comparison against a modern
deep-learning baseline such as EEGNet (Lawhern et al., 2018) to
quantify how much the left/right-hand confusion documented here is
a fundamental limit of the EEG signal versus a limit of the CSP+LDA
approach. Cross-subject transfer — training on some subjects and
evaluating on a held-out subject without any retraining — is another
important test not addressed here. Finally, a small pilot recording
session on a research-grade EEG system would allow this pipeline to
be validated on original data collected under controlled conditions,
rather than solely on a pre-existing public dataset.

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

Lawhern VJ, Solon AJ, Waytowich NR, Gordon SM, Hung CP, Lance BJ.
EEGNet: a compact convolutional neural network for EEG-based
brain-computer interfaces. *Journal of Neural Engineering*.
2018;15(5):056013.

---

### Notes for posting to OSF Preprints

- OSF Preprints (osf.io/preprints) requires no institutional affiliation —
  list yourself as an independent researcher if that's accurate.
- You'll need a short plain-language summary in addition to the abstract;
  reuse the "Why this project" section of the README for that.
- Link the GitHub repo from the preprint so reviewers/readers can verify
  and rerun everything.
