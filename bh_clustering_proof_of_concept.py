
import pandas as pd
import numpy as np
import random
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
from lenscat import lenscat
from tqdm import tqdm
import os

from google.colab import drive
drive.mount('/content/drive')

# Prepare output directory
output_dir = "/content/drive/MyDrive/bh_clustering_batches/"
os.makedirs(output_dir, exist_ok=True)

# Configure SIMBAD
custom_simbad = Simbad()
custom_simbad.TIMEOUT = 120
custom_simbad.add_votable_fields("otype", "ra", "dec")

# Define BH-like types
bh_types = {"BH", "BH?","BLLac", "QSO", "AGN", "XRB", "LMXB", "HMXB", "BHXRB"}

# Load lens catalog and filter
df = lenscat.load()
lens_df = df[(df["grade"].isin(["A", "B"])) & (df["z"].notna())].reset_index(drop=True)
lens_df_sample = lens_df.sample(n=100, random_state=42).reset_index(drop=True)

# Store all results
results = []

# Main loop
for idx, row in tqdm(lens_df_sample.iterrows(), total=len(lens_df_sample)):
    lens_ra, lens_dec = row["ra"], row["dec"]
    lens_coord = SkyCoord(ra=lens_ra * u.deg, dec=lens_dec * u.deg, frame="icrs")

    # Random point avoiding known lenses
    while True:
        rand_ra, rand_dec = random.uniform(0, 360), random.uniform(-90, 90)
        sep = SkyCoord(rand_ra * u.deg, rand_dec * u.deg).separation(lens_df["ra"].values * u.deg, lens_df["dec"].values * u.deg)
        if np.all(sep > 0.3 * u.deg):  # ~18 arcmin
            break
    rand_coord = SkyCoord(ra=rand_ra * u.deg, dec=rand_dec * u.deg)

    # Query around real lens
    try:
        lens_query = custom_simbad.query_region(lens_coord, radius=15 * u.arcmin)
        lens_bh_count = sum(otype.decode("utf-8") in bh_types for otype in lens_query["OTYPE"]) if lens_query else 0
    except Exception as e:
        lens_bh_count = -1

    # Query around random point
    try:
        rand_query = custom_simbad.query_region(rand_coord, radius=15 * u.arcmin)
        rand_bh_count = sum(otype.decode("utf-8") in bh_types for otype in rand_query["OTYPE"]) if rand_query else 0
    except Exception as e:
        rand_bh_count = -1

    results.append({
        "Lens RA": lens_ra,
        "Lens DEC": lens_dec,
        "BH Count (Lens)": lens_bh_count,
        "BH Count (Random)": rand_bh_count,
        "Random RA": rand_ra,
        "Random DEC": rand_dec,
    })

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(output_dir, "bh_counts_100_lenses.csv"), index=False)

print("✅ Done. Results saved.")
