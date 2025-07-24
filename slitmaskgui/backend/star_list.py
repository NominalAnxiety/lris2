"""
This will convert the Apparent RA and Dec to milimeters and give a position in milimeters for the blah blah blah
"""


PLATE_SCALE = 0.7272 #(mm/arcsecond) on the sky
CSU_HEIGHT = PLATE_SCALE*60*10 #height of csu in mm (height is 10 arcmin)
CSU_WIDTH = PLATE_SCALE*60*5 #width of the csu in mm (widgth is 5 arcmin)


from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
import pandas as pd
import numpy as np
from slitmaskgui.input_targets import TargetList
from slitmaskgui.backend.mask_gen import SlitMask
import math as m

#Ra and Dec --> angle Degrees

RA="12 36 56.72988"
Dec="+62 14 27.3984"

#temp_center = (189.2363745,62.240944) #Ra, Dec
temp_center = SkyCoord(ra=RA,dec=Dec,unit=(u.hourangle,u.deg))

temp_width = .7
temp_pa = 0


#dimensions are 213.76 mm x 427.51 mm I think but have no clue

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
import json
class StarList:
    def __init__(self,payload,RA,Dec,slit_width=0,pa=0):
        self.payload = json.loads(payload)
        self.center = SkyCoord(ra=RA,dec=Dec,unit=(u.hourangle,u.deg))
        self.slit_width = slit_width
        self.pa = pa

        self.complete_json()
        #self.calc_mask()
        

    def complete_json(self): #maybe will rename this to complete payload
        for obj in self.payload:
            star = SkyCoord(obj["ra"],obj["dec"], unit=(u.hourangle, u.deg), frame='icrs')
            separation = self.center.separation(star)  # returns an angle
            obj["center distance"] = float(separation.to(u.arcmin).value)

            delta_ra = (star.ra - self.center.ra).to(u.deg) #from center
            delta_dec = (star.dec - self.center.dec).to(u.arcsec) #from center
            #this math does not work because it
            if delta_ra.value > 180:  # If RA difference exceeds 180 degrees, wrap it
                delta_ra -= 360 * u.deg
            elif delta_ra.value < -180:
                delta_ra += 360 * u.deg

            delta_ra = delta_ra.to(u.arcsec)
            delta_ra_proj = delta_ra * np.cos(self.center.dec.radian) # Correct for spherical distortion

            # Convert to mm
            x_mm = float(delta_ra_proj.value * PLATE_SCALE)
            y_mm = float(delta_dec.value * PLATE_SCALE)

            obj["x_mm"] = x_mm
            obj["y_mm"] = y_mm

            
            #ok this is not how you do this bc I will only take in x and just don't care about y right now (i'll care later)
    def calc_mask(self):
        slit_mask = SlitMask(self.payload)
        return slit_mask.calc_y_pos()

    def send_target_list(self):
        return [[x["name"],x["priority"],x["vmag"],x["ra"],x["dec"],x["center distance"]] for x in self.payload]

    def send_interactive_slit_list(self):
        #have to convert it to dict {bar_num:(position,star_name)}
        #imma just act rn like all the stars are in sequential order
        #I am going to have an optimize function that actually gets the right amount of stars with good positions
        #its going to also order them by bar
        total_pixels = 252 #in the future I will pass this n from interactive slit mask so that will always be correct on resize
        self.interactive_mask = self.calc_mask()
        
        slit_dict = {}
        _max = 72
        for i,obj in enumerate(self.interactive_mask):
            if _max <= 0:
                break
            slit_dict[i] = (240+(obj["x_mm"]/(CSU_WIDTH))*total_pixels,obj["bar_id"],obj["name"])

            _max -= 1

        return json.dumps(slit_dict)
    
    def send_row_widget_list(self):
        #again, I am going to ignore the y position of the stars when placing them, I will worry about that later
        row_list =[]
        _max = 72
        for obj in self.payload:
            if _max <= 0:
                break
            row_list.append([obj["bar_id"],obj["x_mm"],self.slit_width])
            _max -= 1
        sorted_row_list = sorted(row_list, key=lambda x: x[0])
        return sorted_row_list
