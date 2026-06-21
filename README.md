# MotorMind — decoding imagined movement from EEG

An open-source motor-imagery brain-computer interface (BCI). It classifies
whether a person is imagining moving their **left hand**, **right hand**, or
**feet**, using EEG signals alone, built entirely on free public data.

**[Live site →](https://tanveersubscriptions-stack.github.io/motormind/)** &nbsp;&middot;&nbsp; **[Preprint →](#)** (add once published)

## Why this project

People with paralysis or locked-in syndrome can still generate motor-cortex
signals when they imagine moving, even though the signal never reaches the
limb. BCIs read that imagined-movement signal and decode it into a control
command. This project rebuilds the classic version of that decoding
pipeline from scratch, on the same public dataset BCI researchers have used
for two decades, so it's achievable solo with just a laptop.

## What's in this repo

```
motormind/
├── requirements.txt
├── src/
│   ├── download_data.py   # fetches the PhysioNet EEGMMIDB dataset
│   ├── preprocess.py      # filters + epochs the raw recordings
│   └── train_model.py     # trains CSP+LDA, evaluates, exports results
├── web/
│   ├── index.html         # the project website (single file, deployable as-is)
│   └── assets/figures/    # confusion matrix + CSP pattern plots (generated)
└── docs/
    └── manuscript_draft.md  # research write-up template (OSF-preprint style)
```

## Setup

You'll need a machine with internet access (this pipeline downloads ~1-2 GB
of EEG data from PhysioNet, depending on how many subjects you include).

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the pipeline

Run these three scripts in order. By default they use subjects 1-20 (a
good-sized sample for a passion project); pass `--subjects` to change that.

```bash
python src/download_data.py            # downloads raw .edf files to data/raw/
python src/preprocess.py               # filters + epochs -> data/processed/
python src/train_model.py              # trains the model, evaluates, exports results
```

`train_model.py` will print per-subject accuracy as it runs, then write:

- `web/data/results.json` — everything the website needs (accuracy, per-subject
  scores, and a handful of example trials with predictions)
- `web/assets/figures/confusion_matrix.png`
- `web/assets/figures/csp_patterns.png`

## Updating the website with your real results

The website ships with **clearly-labeled placeholder data** so it works
out of the box, but those numbers are *not real* — they're illustrative.
**Before you publish, present, or share this site, replace them:**

1. Open `web/data/results.json` (generated above).
2. Open `web/index.html` and find the `RESULTS` constant near the top of
   the `<script>` tag — it's commented `PLACEHOLDER DATA`.
3. Replace the object's contents with your real `results.json` data.
4. Reload the page. The "Status: pipeline not yet run on real data" note
   in the Results section will disappear automatically once
   `generated_from` is no longer `"placeholder"` — set it to
   `"real_pipeline"` (the script already does this).

You can preview the site locally with:

```bash
cd web && python -m http.server 8000
# then open http://localhost:8000
```

## Personalizing the research log

The "Research log" section on the site has bracketed prompts
(`[Write 2-3 sentences on...]`). Replace them with your real notes — what
you tried, what broke, what you learned. That narrative is the part of a
passion project that actually reads as genuine, so don't skip it or leave
it generic.

## Publishing your findings

Once you have real results, here's a realistic path to making this count
as a genuine, citable piece of public research:

1. **Open-source the code.** Push this repo to GitHub with the included
   `LICENSE` (MIT). This alone is real community impact — anyone can run,
   verify, or build on your pipeline.
2. **Post a preprint on [OSF Preprints](https://osf.io/preprints).** It's
   free, requires no institutional affiliation, and gives you a permanent,
   citable DOI. Use `docs/manuscript_draft.md` as your starting point.
3. **Stretch goal — [JOSS](https://joss.theoj.org/)** (Journal of Open
   Source Software). If you polish the pipeline into clean, tested,
   documented, reusable software, JOSS is a real peer-reviewed venue with
   no institutional gatekeeping. Higher bar, but a genuine publication.
4. **Write a public-facing post** (Medium, a personal blog, dev.to). This
   is what actually drives the "community impact" side — a technical
   write-up that anyone curious about BCIs can find and read.

## Data and ethics note

This project uses the PhysioNet EEG Motor Movement/Imagery Dataset — public,
de-identified, and released for reuse under PhysioNet's open data terms. The
original collection was already IRB-approved; you don't need separate
approval to analyze it, but you do need to cite it (see below).

## Citations

- Goldberger AL, Amaral LAN, Glass L, et al. *PhysioBank, PhysioToolkit, and
  PhysioNet: Components of a New Research Resource for Complex Physiologic
  Signals.* Circulation. 2000.
- Schalk G, McFarland DJ, Hinterberger T, Birbaumer N, Wolpaw JR. *BCI2000:
  A General-Purpose Brain-Computer Interface (BCI) System.* IEEE
  Transactions on Biomedical Engineering. 2004.
- Ramoser H, Muller-Gerking J, Pfurtscheller G. *Optimal spatial filtering
  of single trial EEG during imagined hand movement.* IEEE Trans Rehabil
  Eng. 2000.
- Gramfort A, Luessi M, Larson E, et al. *MEG and EEG data analysis with
  MNE-Python.* Frontiers in Neuroscience. 2013.

## License

MIT — see `LICENSE`.
