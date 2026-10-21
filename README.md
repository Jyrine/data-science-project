# Palmer Penguins: What Explains Body Mass Variation?

A small, fully reproducible exploratory data analysis project. It studies how
much of the variation in penguin body mass is explained by flipper length and
sex, and shows where a single pooled model is misleading.

## Problem / Research Question

**How well do flipper length and sex explain body mass across the three
Palmer penguin species, and does the flipper-mass relationship hold within
each species?**

Motivation: body mass is a common proxy for condition in ecological studies,
so it matters whether a simple morphological predictor works uniformly across
groups or only on average.

## Dataset Source and Usage Permissions

- **Source:** [palmerpenguins](https://github.com/allisonhorst/palmerpenguins)
  (`penguins.csv`), collected by Dr. Kristen Gorman at Palmer Station,
  Antarctica LTER ([palmerpenguins doc](https://allisonhorst.github.io/palmerpenguins/)).
- **Permission:** the dataset is published under the
  [CC0 1.0 public-domain dedication](https://creativecommons.org/publicdomain/zero/1.0/),
  so it is free to use, share, and modify with no restriction.
- 344 rows, 8 columns; 11 rows with missing measurements are dropped,
  leaving 333 complete cases.
- The CSV is included in `data/` so the analysis runs offline. No passwords,
  API keys, personal data, or restricted datasets are used.

## Methods and Tools

- **Language/libraries:** Python 3.13, pandas 3.0, matplotlib 3.11, NumPy.
- **Methods:**
  - listwise deletion of rows with missing morphometric values;
  - pooled ordinary least squares fit of `body_mass_g ~ flipper_length_mm`
    (R² = 0.76);
  - per-species fits to check that the slope is stable across groups;
  - group means and boxplots for the sex comparison.

## Key Findings and One Limitation

**Findings**

1. Pooled fit: flipper length alone explains **R² = 0.76** of body-mass
   variance (pooled slope ≈ 50 g per mm).
2. But the within-species slopes differ a lot — Adelie ≈ 33 g/mm
   (R² = 0.22) vs Gentoo ≈ 54 g/mm (R² = 0.51) — so the pooled slope is
   driven partly by species differences (Gentoo are both longest-flippered
   and heaviest, ~5.1 kg vs ~3.7 kg).
3. Within every species males average heavier than females
   (overall gap ≈ 683 g).

**One limitation**

This is an observational sample from only three species at three islands
during 2007–2009. The sex/mass and flipper/mass patterns describe this
population only; they cannot be generalized to other penguin populations or
read as causal effects.

## How to Run the Analysis

```bash
# 1. Create an environment (any Python >= 3.10 works)
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the analysis (writes figures/ and results/)
python analysis.py
```

Outputs: `figures/fig1_mass_vs_flipper.png`,
`figures/fig2_mass_by_sex.png`, and `results/summary.md`.

## Repository Structure

```
data-science-project/
├── analysis.py                  # full pipeline: load → fit → figures → summary
├── requirements.txt
├── data/penguins.csv            # CC0 source data (kept for offline runs)
├── figures/                     # generated visualizations
└── results/                     # generated summary tables
```
