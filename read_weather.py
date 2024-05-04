# import numpy as np
import pandas as pd
import os
import re
from file_formater import Weather_folder
import geopandas as gpd

data_path = "D:/315Lab/DATA/TReAD_sub3/"
wth_variable = ('SRAD', 'TMAX', 'TMIN', 'RAIN')
start_year = 1980
end_year = 2021


class TReAD_filename():
   def __init__(self, filename: str, index: int = 4):
      """
      Extract TReADXXXX_XXX_XXX_XXX_year.csv pattern, change 'index' to extract different location.
      """
      # Define split pattern
      pattern = r'[_\.]'

      # split the string
      parts = re.split(pattern, filename)

      # Extract year location
      self.year = int(parts[index])
   def __str__(self):
      return f"This TReAD file for year: {self.year}"

# Weather folder's object
weather = Weather_folder(data_path, wth_variable)

data = weather.read_file(1980)

# Spatial join (if the points align exactly or are very close, adjust 'op' accordingly, e.g., 'intersects', 'within', etc.)

# Query: LON = 122.1, LAT = 25.5 just in SRAD
print(data['SRAD'].query("LON = 122.1, LAT = 25.5"))



print(data)
