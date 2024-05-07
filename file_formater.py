import os
import fortranformat as ff
from pandas import isna
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from datetime import date, datetime
from functools import reduce

# Funciton to read a layer (row)
def soil_line_read(line, format_list):
    fmt = '1X'
    for n, field in enumerate(line.split()):
        if n != 0:
            fmt += ',1X'
        if field.replace('.', '') == '-99':
            fmt += ',A5'
        else:
            fmt += ',' + format_list[n]
    return ff.FortranRecordReader(fmt).read(line)


def soil_line_write(fields, line_fmt):
    fmt = '1X'
    for n, field in enumerate(fields):
        if n != 0:
            fmt += ',1X'
        if isna(field):
            fields[n] = '-99'
            fmt += ',A5'
        else:
            fmt += ',' + line_fmt[n]
    return ff.FortranRecordWriter(fmt).write(fields)

def soil_location_write(fields):
    fmt = '1X,A12,A12,1X,'
    for field in fields[2:4]:
        if not isinstance(field, float):
            fmt += 'A8,1X,'
        else:
            fmt += 'F8.3,1X,'
    fmt += 'A36'
    return ff.FortranRecordWriter(fmt).write(fields)

def weather_station(fields):
    fmt = '2X,A4,2(1X,F8.3),1X,I5'
    for n, field in enumerate(fields[4:], 4):
        fmt += ',1X'
        if isna(field):
            if (n + 1) == len(fields):
                fields[n] = ''
            else:
                fields[n] = '-99'
            fmt += ',A5'
        else:
            if (n + 1) == len(fields):
                fmt += ",I5"
            else:
                fmt += ',F5.1'
    return ff.FortranRecordWriter(fmt).write(fields) + '\n'

def weather_data_header(fields):
    fmt = f'{len(fields)}(1X,A5)'
    return '@  DATE' + ff.FortranRecordWriter(fmt).write(fields) + '\n'

def weather_data(fields):
    fmt = f'A7,{len(fields)}(1X,F5.1)'
    return ff.FortranRecordWriter(fmt).write(fields) + '\n'

class Weather_folder():
    """
        TReAD files names and the full names
    """
    def __init__(self, folder_path: str, weather_var: list, year_range: list = range(1980, 2022)):
        # Extract filenames in the director
        filenames = {var: os.listdir(folder_path + var) for var in weather_var}

        # Link path to All filenames in filepaths
        filepaths = {wth: [os.path.join(folder_path + wth + "/", f) for f in filenames[wth]] for wth in weather_var}

        self.filenames = filenames # Dict: Var(Key): filename(Variables)
        self.filepaths = filepaths # Dict: Var(Key): filepath(Variables)
        self.vars = weather_var

    # Read files for a specific year
    def read_file(self, year: int) -> dict:
        # Extract specific year's filenames
        filenames = {v: [fnames for fnames in self.filepaths[v] if fnames.endswith(f'{year}.csv')][0] for v in self.vars}

        # Save file as a dictionary
        data_frames = {}

        for v, path in filenames.items():

            # Read file
            df = pd.read_csv(path)

            # Select unusual column
            drop_cols = [col for col in df.columns if col.startswith('Unnamed')]

            # Drop unusual column
            df.drop(columns = drop_cols, inplace = True)

            # Turn to GeoDataFrame
            geo_df = gpd.GeoDataFrame(
                data = df,
                geometry = [Point(xy) for xy in zip(df['LON'], df['LAT'])],
                crs="EPSG:4326"  # Ensure coordinates are in WGS 84
            )

            # Transform to TWD97 coordinate
            geo_df.to_crs(3826, inplace = True)

            # Drop LON and LAT columns.
            geo_df.drop(columns = ['LON', 'LAT'], inplace = True)

            # Buffer
            geo_df['geometry'] = geo_df.buffer(0.05, cap_style = 'square')

            # Melt data frame into "long table"
            geo_df = pd.melt(geo_df, id_vars = ('geometry'), var_name = 'Date', value_name = v)

            # Datetime format
            geo_df['Date'] = pd.to_datetime(geo_df['Date'], format = "%Y%m%d")

            # Transform to WGS84 coordinate
            geo_df.to_crs(4326, inplace = True)

            # Save Data Frame as a Key: value dictionary
            data_frames[v] = geo_df

        # # Assuming dfs is a list of DataFrames that all contain a column named 'Key'
        # df_merged = reduce(lambda left, right: pd.merge(left, right, on = ['geometry', 'Date'], how = 'left'), data_frames.values())

        # df_merged.dropna(subset = ['SRAD', 'TMAX', 'TMIN', 'RAIN'], inplace = True)


        return data_frames


