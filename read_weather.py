# import numpy as np
import pandas as pd
import os
import re
from file_formater import Weather_folder
import geopandas as gpd
from datetime import datetime

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
print(data)
# overlap_points = data.loc[data['Date'] == datetime(1980,1,1),]

# Spatial join (if the points align exactly or are very close, adjust 'op' accordingly, e.g., 'intersects', 'within', etc.)

# Query: LON = 122.1, LAT = 25.5 just in SRAD
# print(data['SRAD'].query("LON = 122.1, LAT = 25.5"))


# import matplotlib.pyplot as plt

# taiwan =  gpd.read_file("./raw/tw-shp/COUNTY_MOI_1090820.shp")
# taiwan.to_crs(4326, inplace = True)
# # Create a plot
# fig, ax = plt.subplots(figsize = (5, 6))

# # Plot Taiwan
# taiwan.plot(ax = ax, color = 'white', edgecolor = 'black')

# # Plot points
# ax.scatter(x = overlap_points['geometry'].x, y = overlap_points['geometry'].y, color = 'blue', alpha = 0.3)
# # ax.scatter(x = data['SRAD']['geometry'].x, y = data['SRAD']['geometry'].y, color = 'red', alpha = 0.3)

# # Optionally, set a title
# plt.title("Map from Shapefile")
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# # Optional: Limit the view to a specific area
# plt.xlim(119.9, 122.3)
# plt.ylim(21.8, 25.6)

# # Show the plot
# plt.show()
