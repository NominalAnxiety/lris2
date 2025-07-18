import pandas as pd
import numpy as np

# --- Generate mock Gaia input data ---
np.random.seed(42)  # for reproducibility

N_TOTAL = 104  # 100 science + 4 alignment

# Centered at RA=157.5, Dec=20.0 with ±0.15° variation
ra_vals = 157.5 + np.random.uniform(-0.15, 0.15, N_TOTAL)
dec_vals = 20.0 + np.random.uniform(-0.15, 0.15, N_TOTAL)
magnitudes = np.random.uniform(9.5, 15.0, N_TOTAL)  # realistic Gaia G mag range

gaia_data = pd.DataFrame({
    'ra': ra_vals,
    'dec': dec_vals,
    'phot_g_mean_mag': magnitudes
})




from astropy.coordinates import SkyCoord
import astropy.units as u

# Sort by brightness (ascending)
gaia_data = gaia_data.sort_values('phot_g_mean_mag').reset_index(drop=True)

# Format RA/Dec into WMKO starlist format
def format_coord(ra_deg, dec_deg):
    coord = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame='icrs')
    ra_str = coord.ra.to_string(unit=u.hour, sep=' ', precision=2, pad=True)
    dec_str = coord.dec.to_string(sep=' ', alwayssign=True, precision=2, pad=True)
    return ra_str, dec_str

# Create formatted lines for science and alignment stars
lines = []
center_ra = gaia_data['ra'].mean()
center_dec = gaia_data['dec'].mean()

# Science targets (entries 4–103)
for i in range(4, 104):
    star = gaia_data.iloc[i]
    name = f'Gaia{i - 3:04d}'  # Gaia0001 to Gaia0100
    ra_str, dec_str = format_coord(star['ra'], star['dec'])
    vmag = f"{star['phot_g_mean_mag']:.2f}"
    line = f"{name:<16}{ra_str} {dec_str} 2000.0 vmag={vmag}"
    lines.append(line)

# Alignment stars (entries 0–3)
for i in range(4):
    star = gaia_data.iloc[i]
    name = f'GaiaAlign{i+1:02d}'
    ra_str, dec_str = format_coord(star['ra'], star['dec'])
    vmag = f"{star['phot_g_mean_mag']:.2f}"
    line = f"{name:<16}{ra_str} {dec_str} 2000.0 vmag={vmag}"
    lines.append(line)

# Save to file
with open("keck_starlist.txt", "w") as f:
    f.write(f"# Starlist centered at RA={center_ra:.5f}, Dec={center_dec:.5f}, from mock Gaia data\n")
    f.write("# 100 science targets + 4 alignment stars\n")
    for line in lines:
        f.write(line + "\n")

print("✅ Starlist saved to 'keck_starlist.txt'")
