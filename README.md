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

## Key Results

### Large-Scale SIMBAD Query (~13,941 Lenses)

Queried SIMBAD around **~13,941** confident/probable lenses with valid redshift, compared to matched random sky fields with the same number of points at radii 10′, 15′, and 20′.

| Radius     | BH in Lenses (%) | BH in Random (%) | Mean BH Count (Lens) | Mean BH Count (Random) |
|------------|------------------|------------------|---------------------|-----------------------|
| 10 arcmin  | 63.5%            | 35.4%            | 7.90                | 1.74                  |
| 15 arcmin  | 68.2%            | 40.0%            | 17.03               | 3.90                  |
| 20 arcmin  | 71.6%            | 44.0%            | 28.97               | 6.90                  |

Statistical tests (Chi-squared, Binomial, Poisson, KS) show p-values < 1e-100 for all radii, **strongly confirming** a significant excess of BH-type objects near lenses compared to random sky fields.

---

### Medium-Scale Spatial Clustering (1000 Lenses)

Subsamples of 1000 lenses were analyzed for spatial clustering, showing that 77% of lens fields contain at least one BH-type object compared to only 21% of random fields. The mean BH-type object count near lenses (28.76) greatly exceeds that of random fields (2.48), with a Kolmogorov-Smirnov test statistic of 0.22 (p ≈ 0), confirming significant clustering differences.

---

## Visualizations

### 📊 Histogram: BH Counts Near Lenses vs. Random Fields

![BH Histogram](images/Histogram.lenses.png)

**Description:** Histogram comparing the number of BH-type objects per field around strong gravitational lenses (blue) and matched random sky positions (orange). Each field covers a 20′ radius. The x-axis shows BH-type object counts; the y-axis is normalized probability.  
**Key Insight:** BH-type objects occur far more frequently near lenses than in randomly selected sky regions.

---

### 🌌 Spatial Scatter Plot: BH Object Locations

![Spatial Plot](images/spatial.png)

**Description:** Scatter plot of BH-type object positions around 1000 strong lenses (left) and 1000 matched random fields (right). Each dot represents a SIMBAD-classified BH-type object within a 20′ radius of the center.  
**Key Insight:** A higher concentration of BH-type objects is evident in lens fields compared to random fields, supporting spatial correlation.

---

### 📈 Cumulative Distribution Function (CDF)

![CDF Plot](images/cdf.png)

**Description:** Cumulative distribution of BH-type object counts in lens vs. random fields. The plot shows the fraction of fields with a BH count less than or equal to a given value.    
**Key Insight:** Lenses have a systematically higher probability of hosting multiple BH-type objects than random fields.

---

## Ripley's K Function Spatial Clustering

![Ripley's K Function Plot](images/Ripley_k_plot.png)



**Description:** Cumulative distribution of BH-type object counts in lens vs. random fields. The plot shows the fraction of fields with a BH count less than or equal to a given value.

**Key Insight:** Lenses have a systematically higher probability of hosting multiple BH-type objects than random fields, indicating a statistically significant excess of BH-like populations in the vicinity of strong gravitational lenses.


---

### Case Study: Bullet Cluster

We examined the **Bullet Cluster** (RA = 104.5°, Dec = −55.9°), a well-known merging galaxy cluster often cited in dark matter research. Using the same black hole–type object query method, we analyzed BH associations at 10′, 15′, and 20′ radii centered on the cluster position. In each case, the number of BH-type objects near the Bullet Cluster vastly exceeded the average in random fields:

| Radius        | BH Count (Bullet) | Mean BH Count (Random) | Poisson p-value    | KS p-value         |
|---------------|-------------------|-------------------------|---------------------|---------------------|
| 10 arcmin     | 4                 | 0.08                    | < 1 × 10⁻¹²         | < 1 × 10⁻⁴          |
| 15 arcmin     | 10                | 0.18                    | < 1 × 10⁻²³         | < 1 × 10⁻⁵          |
| 20 arcmin     | 15                | 0.3                     | < 1 × 10⁻³⁰         | < 1 × 10⁻⁶          |

**Key Insight:** The Bullet Cluster shows a highly significant overabundance of BH-type objects compared to expectations from random sky positions, consistent with the broader statistical trends across the full lens sample.

---

## Interpretation

These results reveal a pronounced excess and spatial clustering of BH-type objects around strong lens candidates, implying that lenses reside in environments rich with black hole-related phenomena. This statistical association points to additional factors influencing lens environments, which are not accounted for by conventional dark matter halo models. Such findings highlight the need for further astrophysical investigation beyond standard dark matter explanations.

---

## Limitations

- **SIMBAD Classification Biases:** Dependence on SIMBAD classifications means results may be affected by incomplete or inconsistent object labeling.

- **Lens Catalog Completeness and Confidence:** The lenscat catalog includes candidates with varying grading and potential selection biases impacting statistical robustness.

- **2D Projected Analysis:** Use of angular separations and fixed radii lacks full three-dimensional spatial information (redshift uncertainties and line-of-sight distances), limiting environmental precision.

- **Random Control Selection:** Random fields, although matched in galactic latitude and excluding known lenses, may still be subject to large-scale structure biases.

- **Computational Constraints:** Spatial clustering analysis was limited to a 1000-lens subsample; full-sample clustering analysis remains future work.

- **Observational and Model-Agnostic:** The study is statistical and observational without proposing a physical mechanism, thus astrophysical interpretations remain tentative. However, a physically motivated modeling system that may explain the observed BH clustering exists and will be explored in future work.

---

## AI Assistance

Parts of the code development and documentation for this project were supported by ChatGPT, an AI language model created by OpenAI. All scientific interpretations, analyses, and decisions remain the sole responsibility of the author.

---

## Code

### `simbad_based_statistical_study_of_black_hole_object_associations_with_strong_gravitational_lenses.py`

- **Description:** Performs a large-scale SIMBAD-based statistical analysis of black hole (BH) object associations with ~14,000 strong gravitational lenses.
- **Location:** [`simbad_based_statistical_study_of_black_hole_object_associations_with_strong_gravitational_lenses.py`](./simbad_based_statistical_study_of_black_hole_object_associations_with_strong_gravitational_lenses.py)
- **Functionality:** Loads the lens catalog from `lenscat`, filters for confident lenses with valid redshift, queries SIMBAD for BH-like objects (BH, QSO, AGN, etc.) near each lens and random sky controls. Performs batch statistical comparisons (Poisson, Chi-squared, binomial) at radii of 10′, 15′, and 20′.
- **Dependencies:** `lenscat`, `astroquery`, `astropy`, `numpy`, `pandas`, `scipy`, `tqdm`.
- **Usage:** Run this script to reproduce the macro-scale statistical results on BH clustering near lenses.

---

### `bh_clustering_proof_of_concept.py`

- **Description:** Proof-of-concept spatial clustering analysis of BH-type objects near a small sample (n=100) of strong gravitational lenses.
- **Location:** [`bh_clustering_proof_of_concept.py`](./bh_clustering_proof_of_concept.py)
- **Functionality:** Loads a small lens subset from `lenscat`, queries SIMBAD for BH-like objects near each lens and matched random points, computes pairwise angular separations, and compares clustering using histograms and cumulative distribution functions (CDFs).
- **Dependencies:** `lenscat`, `astroquery`, `astropy`, `numpy`, `pandas`, `matplotlib`, `scipy`.
- **Usage:** Run this script for quick exploratory analysis and spatial clustering visualization using Ripley-style statistics.

---

### `ripley_k_bh_lens_analysis_py.py`

- **Description:** Performs Ripley’s K function–style spatial clustering analysis of black hole (BH)-type objects around a medium sample (n=1000) strong gravitational lenses versus matched random sky fields, quantifying angular clustering differences.  
- **Location:** [`ripley_k_bh_lens_analysis_py.py`](./ripley_k_bh_lens_analysis_py.py)  
- **Functionality:** Loads BH object coordinate data for lenses and random fields, computes pairwise angular separations, plots histograms of separations, and applies a Kolmogorov-Smirnov (KS) test to assess clustering significance.  
- **Dependencies:** `numpy`, `pandas`, `astropy`, `matplotlib`, `scipy`.  
- **Usage:** Run this script after obtaining SIMBAD query data to analyze and visualize spatial clustering signatures using Ripley’s K–style statistics.

---

**Required packages for all scripts:**

```bash
pip install lenscat astroquery astropy pandas numpy scipy matplotlib tqdm
```
---

## License
MIT License

## Contact
For questions or collaboration inquiries, please open an issue or contact [mjay10016@gmail.com].






