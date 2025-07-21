from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import random

def query_gaia_starlist_rect(ra_center, dec_center, width_arcmin=5, height_arcmin=10, n_stars=100, output_file='gaia_starlist.txt'):
    # Convert center to SkyCoord
    center = SkyCoord(ra_center, dec_center, unit=(u.deg, u.deg), frame='icrs')

    # Convert arcsec to degrees
    width_deg = (width_arcmin * u.arcmin).to(u.deg).value
    height_deg = (height_arcmin * u.arcmin).to(u.deg).value

    # Compute RA and Dec bounds
    ra_min = center.ra.deg - width_deg / 2
    ra_max = center.ra.deg + width_deg / 2
    dec_min = center.dec.deg - height_deg / 2
    dec_max = center.dec.deg + height_deg / 2

    # ADQL box query
    query = f"""
    SELECT TOP {n_stars}
        source_id, ra, dec, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE ra BETWEEN {ra_min} AND {ra_max}
      AND dec BETWEEN {dec_min} AND {dec_max}
    ORDER BY phot_g_mean_mag ASC
    """
    job = Gaia.launch_job_async(query)
    results = job.get_results()

    # Write starlist
    with open(output_file, 'w') as f:
        f.write(f"# Starlist centered at RA={center.ra.to_string(u.hour, sep=':')}, Dec={center.dec.to_string(sep=':')}\n")
        for i, row in enumerate(results):
            name = f"Gaia_{i+1:03d}"
            coord = SkyCoord(ra=row['ra']*u.deg, dec=row['dec']*u.deg)
            ra_h, ra_m, ra_s = coord.ra.hms
            sign, dec_d, dec_m, dec_s = coord.dec.signed_dms
            dec_d = sign * dec_d

            line = f"{name:<15} {int(ra_h):02d} {int(ra_m):02d} {ra_s:05.2f} {int(dec_d):+03d} {int(dec_m):02d} {abs(dec_s):04.1f} 2000.0 vmag={row['phot_g_mean_mag']:.2f} priority={random.randint(1,2000)}\n"
            f.write(line)

    # Output center info
    print("✅ Starlist generated!")
    print(f"RA center  = {center.ra.to_string(u.hour, sep=':')}")
    print(f"Dec center = {center.dec.to_string(sep=':')}")
    print(f"Saved to   = {output_file}")

# Example call — replace RA/Dec with your actual center
query_gaia_starlist_rect(
    ra_center=189.2363745,              # RA in degrees
    dec_center=62.240944,               # Dec in degrees
    width_arcmin=5,
    height_arcmin=10,
    n_stars=104,
    output_file='gaia_starlist.txt'
)
