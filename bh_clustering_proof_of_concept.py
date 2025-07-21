"""
Proof-of-concept spatial clustering analysis of BH-type objects near a small sample (n=100) of strong gravitational lenses.

This script:
- Loads a small subset of lenses from 'lenscat'.
- Queries SIMBAD for BH-type objects near each lens and matched random points.
- Computes angular separations between BH objects and lenses.
- Produces histograms and cumulative distribution functions (CDF) to compare clustering.

Dependencies: lenscat, astroquery, astropy, numpy, pandas, matplotlib, scipy

Run this script for quick exploratory spatial clustering analysis and visualization.
"""

import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
from lenscat import catalog

# Load small lens subset (~100)
print("Loading full catalog from lenscat package...")
df = catalog.to_pandas()
df_strong = df[df['grading'].isin(['confident', 'probable'])].copy()
df_strong['z'] = pd.to_numeric(df_strong['zlens'], errors='coerce')
df_strong = df_strong.dropna(subset=['z']).reset_index(drop=True)

lens_sample = df_strong.sample(n=100, random_state=42).reset_index(drop=True)
print(f"Sampled {len(lens_sample)} lenses for proof-of-concept.")

# Prepare SIMBAD query setup
custom_simbad = Simbad()
custom_simbad.TIMEOUT = 60
custom_simbad.remove_votable_fields('*')
custom_simbad.add_votable_fields('otype')

bh_types = ['BH', 'BHXRB', 'XRB', 'BLAZAR', 'AGN', 'QSO']

def query_bh_objects(coord, radius_arcmin=20):
    radius = radius_arcmin * u.arcmin
    try:
        result = custom_simbad.query_region(coord, radius=radius)
        if result is None:
            return []
        # Filter BH-type objects
        bh_objects = [row for row in result if any(bh in row['OTYPE'] for bh in bh_types)]
        return bh_objects
    except Exception as e:
        print(f"SIMBAD query failed at {coord.to_string('hmsdms')}: {e}")
        return []

# Generate random sky points avoiding lenses (approximate)
def generate_random_points(n_points, min_sep_arcmin=20):
    points = []
    attempts = 0
    max_attempts = n_points * 100
    all_coords = SkyCoord(ra=lens_sample['RA'].values * u.deg,
                          dec=lens_sample['DEC'].values * u.deg)
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

# Query BH objects for lenses and random fields
lens_bh_objects = []
random_bh_objects = []
lens_coords = SkyCoord(ra=lens_sample['RA'].values * u.deg,
                       dec=lens_sample['DEC'].values * u.deg)
random_coords = generate_random_points(len(lens_sample), min_sep_arcmin=20)

print("Querying SIMBAD for BH-type objects around lenses...")
for coord in lens_coords:
    objs = query_bh_objects(coord, radius_arcmin=20)
    lens_bh_objects.append(objs)
    time.sleep(1)  # throttle

print("Querying SIMBAD for BH-type objects around random points...")
for coord in random_coords:
    objs = query_bh_objects(coord, radius_arcmin=20)
    random_bh_objects.append(objs)
    time.sleep(1)  # throttle

# Flatten BH counts per field
lens_counts = [len(objs) for objs in lens_bh_objects]
random_counts = [len(objs) for objs in random_bh_objects]

# Histogram and CDF plots
plt.figure(figsize=(10, 6))
bins = np.arange(0, max(max(lens_counts), max(random_counts)) + 2) - 0.5
plt.hist(lens_counts, bins=bins, alpha=0.6, label='Lens Fields')
plt.hist(random_counts, bins=bins, alpha=0.6, label='Random Fields')
plt.xlabel('BH-type Object Count')
plt.ylabel('Number of Fields')
plt.title('Histogram of BH-type Objects Near Lenses vs Random Fields')
plt.legend()
plt.show()

# CDF plot
def cdf(data):
    sorted_data = np.sort(data)
    yvals = np.arange(1, len(sorted_data)+1) / float(len(sorted_data))
    return sorted_data, yvals

lens_x, lens_y = cdf(lens_counts)
random_x, random_y = cdf(random_counts)

plt.figure(figsize=(10, 6))
plt.step(lens_x, lens_y, label='Lens Fields', where='post')
plt.step(random_x, random_y, label='Random Fields', where='post')
plt.xlabel('BH-type Object Count')
plt.ylabel('CDF')
plt.title('Cumulative Distribution Function of BH-type Object Counts')
plt.legend()
plt.show()
