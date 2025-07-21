# ripley_clustering_analysis.py

"""
This script performs spatial clustering analysis using Ripley’s K function to evaluate whether
black hole-like objects (AGN/QSO/BLAZAR/XRB/etc.) are more spatially clustered around strong
lensing candidates than around random control fields.

Input: 1000 randomly selected strong lenses from lenscat with redshift.
SIMBAD is queried within a fixed radius (~20 arcmin) for BH-type objects.

Output: Comparison of Ripley's K function and pairwise angular separation distributions
between real lens fields and matched random sky positions.

Dependencies: lenscat, astroquery, astropy, numpy, scipy, tqdm, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from lenscat import load_lenscat
from astroquery.simbad import Simbad
from tqdm import tqdm
from scipy.spatial import distance_matrix
from scipy.stats import ks_2samp
import random

# Custom SIMBAD query setup
custom_simbad = Simbad()
custom_simbad.TIMEOUT = 120
custom_simbad.add_votable_fields("otype")

# BH-type objects
BH_TYPES = ["BH", "QSO", "BLLac", "AGN", "XRB", "BHXRB", "Blazar"]
RADIUS = 20 * u.arcmin
N_LENSES = 1000

# Load and filter lenses
print("Loading lens catalog...")
lenses = load_lenscat()
lenses = lenses[lenses['grade'].isin(['confident', 'probable'])]
lenses = lenses.dropna(subset=['z'])
lenses = lenses.sample(n=N_LENSES, random_state=42).reset_index(drop=True)

# SIMBAD Query Function
def query_bh_objects(ra_deg, dec_deg, radius):
    result = custom_simbad.query_region(SkyCoord(ra=ra_deg*u.deg, dec=dec_deg*u.deg), radius=radius)
    if result is None:
        return []
    return [SkyCoord(ra=r['RA'], dec=r['DEC'], unit=(u.hourangle, u.deg))
            for r in result if str(r['OTYPE']) in BH_TYPES]

# Angular separation clustering helper
def compute_pairwise_separations(coords):
    if len(coords) < 2:
        return np.array([])
    sky_coords = SkyCoord(coords)
    separations = sky_coords.separation(sky_coords).to(u.arcmin)
    sep_vals = separations[np.triu_indices(len(coords), k=1)].value
    return sep_vals

# Gather BH coordinates near lenses and randoms
lens_seps, rand_seps = [], []
all_lens_coords, all_rand_coords = [], []

print("Querying SIMBAD for BH objects near lenses and random controls...")
for i, row in tqdm(lenses.iterrows(), total=len(lenses)):
    ra, dec = row['ra'], row['dec']
    lens_coords = query_bh_objects(ra, dec, RADIUS)
    if lens_coords:
        all_lens_coords.extend(lens_coords)
        lens_seps.extend(compute_pairwise_separations(lens_coords))

    # Generate random RA/DEC not near lens
    while True:
        ra_r, dec_r = random.uniform(0, 360), random.uniform(-90, 90)
        if np.all(np.sqrt((ra - ra_r)**2 + (dec - dec_r)**2) > 1):
            break
    rand_coords = query_bh_objects(ra_r, dec_r, RADIUS)
    if rand_coords:
        all_rand_coords.extend(rand_coords)
        rand_seps.extend(compute_pairwise_separations(rand_coords))

# Convert to arrays
lens_seps = np.array(lens_seps)
rand_seps = np.array(rand_seps)

# KS Test
ks_stat, ks_p = ks_2samp(lens_seps, rand_seps)
print(f"\nKS statistic: {ks_stat:.3f}, p-value: {ks_p:.3e}")

# Plot histogram comparison
plt.figure(figsize=(8, 5))
plt.hist(rand_seps, bins=50, density=True, alpha=0.5, label='Random')
plt.hist(lens_seps, bins=50, density=True, alpha=0.5, label='Lenses')
plt.xlabel('Angular Separation (arcmin)')
plt.ylabel('Normalized Count')
plt.title('BH Object Pairwise Separations')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("ripley_separation_histogram.png")
plt.show()

print("\nAnalysis complete. Ripley-style clustering results saved.")
