# bh_lens_simbad_analysis.py
SIMBAD-based statistical study of black hole object associations with strong gravitational lenses
# Black Hole Association in Strong Lensing Candidates

## Overview

This project investigates the association between strong gravitational lensing candidates and black hole (BH) or BH-like objects using the SIMBAD astronomical database. We analyze a large catalog of lenses (~32,000 candidates) and compare the number of BH-type objects found near lens positions versus random sky positions.

---

## Data and Methodology

- **Lens Catalog:** Loaded directly from the `lenscat` Python package.
- **Lens Selection:** Strong lenses with grading "confident" or "probable" and a usable redshift (`zlens`).
- **Query Targets:** Objects classified as BH, BHXRB, XRB, BLAZAR, AGN, or QSO in SIMBAD.
- **Search Radii:** 10, 15, and 20 arcminutes around each lens.
- **Random Comparison:** Matched random sky coordinates generated with minimum separation from any lens to avoid overlap.
- **Batch Processing:** Lenses are processed in batches of 50 to manage query loads and allow progressive analysis.
- **Statistical Tests:** Chi-squared, binomial, Poisson, and Kolmogorov-Smirnov (KS) tests applied to assess significance of BH clustering near lenses versus random sky.

---

## Results after 50 Batches (2500 Lenses)

### Radius: 10 arcmin
- BH in Lenses: 1962 / 2500 (78.5%)
- BH in Random : 883 / 2500 (35.3%)
- Lens total BH objects: 21,037 (mean per field: 8.41)
- Random total BH objects: 4,116 (mean per field: 1.65)

### Radius: 15 arcmin
- BH in Lenses: 2062 / 2500 (82.5%)
- BH in Random : 1001 / 2500 (40.0%)
- Lens total BH objects: 47,382 (mean per field: 18.95)
- Random total BH objects: 9,252 (mean per field: 3.70)

### Radius: 20 arcmin
- BH in Lenses: 2111 / 2500 (84.4%)
- BH in Random : 1097 / 2500 (43.9%)
- Lens total BH objects: 83,653 (mean per field: 33.46)
- Random total BH objects: 16,459 (mean per field: 6.58)

---

## Interpretation

These results demonstrate a significant excess of BH-type objects clustered around strong lens candidates compared to random sky fields. This strong statistical association suggests lenses are located in BH-rich environments, a finding that warrants further astrophysical investigation.

---

## How to Run

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install lenscat astroquery astropy scipy pandas numpy matplotlib
3. Run the main analysis script to reproduce results.

## License

MIT License


---

If you want, I can help format the **analysis script** that you run for step 3 or draft a quick `main.py` script to upload along with this README. Just say the word!

