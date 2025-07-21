"""
Large-scale SIMBAD-based statistical analysis of black hole (BH) object associations
with strong gravitational lenses using ~13,000 confident lenses.

This script:
- Loads the full lens catalog from the 'lenscat' package.
- Filters confident strong lenses with valid redshift.
- Processes lenses in batches of 50 to manage SIMBAD query loads.
- For each batch and radius (10', 15', 20'), queries SIMBAD for BH-type objects
  near each lens and matching random sky positions avoiding any lenses.
- Performs statistical tests (Chi-squared, Poisson) comparing BH counts around lenses
  versus random sky points.
- Outputs batch-wise and overall statistical summaries.

Dependencies:
- lenscat
- astroquery
- astropy
- numpy
- pandas
- scipy

Run this script to reproduce macro-scale statistical results on BH clustering near lenses.
"""

# Install packages if running in notebook (comment out if running as script)
# !pip install lenscat astropy astroquery scipy pandas numpy

import random
import time
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
from scipy.stats import chi2_contingency, poisson
from lenscat import catalog

def generate_random_points(n_points, all_coords, min_sep_arcmin=20):
    points = []
    attempts = 0
    max_attempts = n_points * 100

    while len(points) < n_points and attempts < max_attempts:
        ra_rand = random.uniform(0, 360)
        dec_rand = random.uniform(-90, 90)
        coord = SkyCoord(ra=ra_rand * u.deg, dec=dec_rand * u.deg)
        sep = coord.separation(all_coords).arcminute
        if np.all(sep > min_sep_arcmin):
            points.append(coord)
        attempts += 1

    if len(points) < n_points:
        print(f"⚠️ Only generated {len(points)} random points after {attempts} attempts")
    return points

def query_bh_counts(coord, radius_arcmin=10):
    radius = radius_arcmin * u.arcmin
    try:
        result = custom_simbad.query_region(coord, radius=radius)
        if result is None:
            return 0
        count = sum(any(bh in otype for bh in bh_types) for otype in result['OTYPE'])
        return count
    except Exception as e:
        print(f"SIMBAD query failed at {coord.to_string('hmsdms')}: {e}")
        return None

# Setup SIMBAD query object
custom_simbad = Simbad()
custom_simbad.TIMEOUT = 60
custom_simbad.remove_votable_fields('*')
custom_simbad.add_votable_fields('otype')

bh_types = ['BH', 'BHXRB', 'XRB', 'BLAZAR', 'AGN', 'QSO']

print("Loading lens catalog...")
df = catalog.to_pandas()

# Filter strong lenses with valid redshift
df_strong = df[df['grading'].isin(['confident', 'probable'])].copy()
df_strong['z'] = pd.to_numeric(df_strong['zlens'], errors='coerce')
df_strong = df_strong.dropna(subset=['z']).reset_index(drop=True)
print(f"Strong lenses with redshift: {len(df_strong):,}")

# Use only confident lenses for analysis
df_confident = df_strong[df_strong['grading'] == 'confident'].copy()
print(f"Confident lenses with redshift: {len(df_confident):,}")

# Batch setup
batch_size = 50
batches = [df_confident.iloc[i:i + batch_size] for i in range(0, len(df_confident), batch_size)]
print(f"Total batches: {len(batches)}")

# All lens coords for random point exclusion
all_lens_coords = SkyCoord(ra=df_confident['RA'].values * u.deg,
                           dec=df_confident['DEC'].values * u.deg)

radii = [10, 15, 20]
results = []

for batch_i, batch_df in enumerate(batches, 1):
    print(f"\nProcessing batch {batch_i} with {len(batch_df)} lenses...")
    lens_coords = SkyCoord(ra=batch_df['RA'].values * u.deg, dec=batch_df['DEC'].values * u.deg)

    # Generate random points avoiding all lenses
    random_points = generate_random_points(len(batch_df), all_lens_coords, min_sep_arcmin=20)

    for radius in radii:
        print(f"  Radius = {radius} arcmin")

        # Query BH counts for lenses
        lens_counts = []
        for coord in lens_coords:
            c = query_bh_counts(coord, radius)
            while c is None:
                time.sleep(5)
                c = query_bh_counts(coord, radius)
            lens_counts.append(c)

        # Query BH counts for random points
        random_counts = []
        for coord in random_points:
            c = query_bh_counts(coord, radius)
            while c is None:
                time.sleep(5)
                c = query_bh_counts(coord, radius)
            random_counts.append(c)

        lens_positive = sum(c > 0 for c in lens_counts)
        random_positive = sum(c > 0 for c in random_counts)
        n_lens = len(lens_counts)
        n_random = len(random_counts)

        contingency = [[lens_positive, n_lens - lens_positive],
                       [random_positive, n_random - random_positive]]
        chi2, p_val, _, _ = chi2_contingency(contingency)

        mean_lens = np.mean(lens_counts)
        mean_random = np.mean(random_counts)
        total_lens = sum(lens_counts)
        total_random = sum(random_counts)
        poisson_p = poisson.sf(total_lens - 1, total_random)

        results.append({
            'batch': batch_i,
            'radius_arcmin': radius,
            'lens_positive_frac': lens_positive / n_lens,
            'random_positive_frac': random_positive / n_random,
            'chi2_pvalue': p_val,
            'mean_lens_count': mean_lens,
            'mean_random_count': mean_random,
            'poisson_pvalue': poisson_p
        })

        print(f"    Lenses with BH≥1: {lens_positive}/{n_lens} ({lens_positive / n_lens:.3f})")
        print(f"    Randoms with BH≥1: {random_positive}/{n_random} ({random_positive / n_random:.3f})")
        print(f"    Chi2 p-value: {p_val:.4g}, Poisson p-value: {poisson_p:.4g}")
        print(f"    Mean BH counts — Lenses: {mean_lens:.2f}, Randoms: {mean_random:.2f}")

df_results = pd.DataFrame(results)
print("\nAll batches completed. Summary:")
print(df_results)
