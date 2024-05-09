# import numpy as np
import pandas as pd
from file_formater import Weather_folder
import weather as wth
import concurrent.futures
from functools import partial

data_path = "D:/315Lab/DATA/TReAD_sub3/"
start_year = 1980
end_year = 2021


# Weather folder's object
weather = Weather_folder(data_path, ('SRAD', 'TMAX', 'TMIN', 'RAIN'))
grid_centroids = weather.unique_location()

def process_location(point, data):
    test_data = data[data['geometry'] == point]
    test_data.set_index("Date", inplace=True)
    df = test_data[['SRAD','TMAX','TMIN','RAIN']]
    weather_data = wth.Weather(df, {"SRAD": "SRAD", "TMAX": "TMAX", "TMIN": "TMIN", "RAIN": "RAIN"},
                                point.y, point.x)
    weather_data.write("./WTH")  # Ensure unique output directories or filenames


for yr in range(1980, 1982):
    print(f"Start for {yr}")
    df = weather.read_file(yr)
    write_wth_for_location = partial(process_location, data = df)
    # Using ThreadPoolExecutor to manage parallel execution
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        executor.map(write_wth_for_location, grid_centroids, chunksize = 2)

