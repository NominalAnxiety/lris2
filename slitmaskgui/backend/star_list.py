"""
This will convert the Apparent RA and Dec to milimeters and give a position in milimeters for the blah blah blah
"""


PLATE_SCALE = 0.712515 #(mm/arcsecond) this is the estimated one
MOSFIRE_PLATE_SCALE = 0.72449 #(mm/arcseond) this is the plate scale for mosfire idk if its the same

from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
import pandas as pd
import numpy as np
from slitmaskgui.input_targets import TargetList
import math as m

#Ra and Dec --> angle Degrees

RA="12 36 56.72988"
Dec="+62 14 27.3984"

temp_center = (189.2363745,62.240944) #Ra, Dec
temp_center = SkyCoord(ra=RA,dec=Dec,unit=(u.hourangle,u.deg))

temp_width = .7
temp_pa = 0

#I think the height, width = 10', 5' both in arcminutes
#formula for it in arcseconds: 1/PLATE_SCALE*height

#right ascension is counterclockwise relative to the north pole
#declination is up

#I will go through a json payload and send back something that 
#the slit row display, target list display, the slit mask display, and the CSU can use

#the input_targets function will give us a json payload
"""
I currently don't factor in PA because I don't know how to
I also assume that RA and DEC are aligned with the x and y axis
while that probably isn't right i'll just get something down for now
"""
class stars_list:
    def __init__(self,payload):
        self.payload = payload
        self.center = temp_center
        self.slit_width = temp_width
        self.pa = temp_pa

        self.complete_json()
        
        #what this will do is have many functions with converstions
    def decimal_to_mm(x):
    #Need to take the difference from the center 
        pass
    def calc_center(center,ra,dec):
        pass

    def complete_json(self): #maybe will rename this to complete payload
        for obj in self.payload:
            star = SkyCoord(obj["ra"],obj["dec"], unit=(u.hourangle, u.deg), frame='icrs')
            separation = self.center.separation(star)  # returns an angle
            obj["center distance"] = float(separation.to(u.arcmin).value)

            delta_ra = (star.ra - self.center.ra).to(u.arcsec)
            delta_dec = (star.dec - self.center.dec).to(u.arcsec)

            delta_ra_proj = delta_ra * np.cos(self.center.dec.radian) # Correct for spherical distortion

            # Convert to mm
            x_mm = float(delta_ra_proj.value * PLATE_SCALE)
            y_mm = float(delta_dec.value * PLATE_SCALE)

            # Save or print results
            obj["x_mm"] = x_mm
            obj["y_mm"] = y_mm


            #ok this is not how you do this bc I will only take in x and just don't care about y right now (i'll care later)

        

    
    def send_target_list(self):
        pass

    def send_interactive_slit_list(self):
        #have to convert it to dict {bar_num:(position,star_name)}
        return self.payload
    
    def send_mask_bar_list(self):
        pass