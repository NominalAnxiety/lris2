"""
This will convert the Apparent RA and Dec to milimeters and give a position in milimeters for the blah blah blah
"""


PLATE_SCALE = 0.712515 #(mm/arcsecond) this is the estimated one
MOSFIRE_PLATE_SCALE = 0.72449 #(mm/arcseond) this is the plate scale for mosfire idk if its the same

from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
from slitmaskgui.input_targets import TargetList

#Ra and Dec --> angle Degrees
thing = SkyCoord("00:48:26.4 85:15:36", unit=(u.hour, u.deg), frame="icrs")
print(thing)

temp_center = (157.49999,20.00012)


#I will go through a json payload and send back something that 
#the slit row display, target list display, the slit mask display, and the CSU can use

#the input_targets function will give us a json payload

class stars_list:
    def __init__(self):
        pass
        #what this will do is have many functions with converstions
    def sexagesimal_to_decimal(ra_dec: tuple):
    #ra_dec = (RA,Dec)
        coord = SkyCoord(f"{ra_dec[0]} {ra_dec[1]}", unit=(u.hourangle, u.deg), frame='icrs')
        return (coord.ra.deg, coord.dec.deg)

    def decimal_to_mm(degree_tuple: tuple):
    #Need to take the difference from the center 
        pass

    def distance_from_center(self):
        pass
