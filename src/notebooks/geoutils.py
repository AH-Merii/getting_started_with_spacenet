import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import re
import pickle5 as pickle

data_path = Path("./processedBuildingLabels/data/rasters_vectors")


def get_dirs(data_path=data_path):
    # extract   root dir names from data_path
    dir_paths = [directory for directory in data_path.iterdir()]
    dir_paths = sorted(dir_paths)

    return dir_paths


def initialize_dict_from_paths(paths):
    d = {dir.name: [] for dir in paths}
    return d


def read_all_data(data_path=data_path):
    dirs = get_dirs(data_path=data_path)

    geodataframes = {}

    d = initialize_dict_from_paths(paths=dirs)

    for dir_ in dirs:
        l = []
        l = get_dirs(dir_)
        d[dir_.name] = l
    return d


def extract_image_number(string):
    pattern = r"img(\d+)"
    image_number = re.findall(pattern=pattern, string=str(string))[0]

    return image_number

def extract_file_extension(string):
    pattern = r"\.(\w+)"
    file_extension = re.findall(pattern=pattern, string=str(string))[0]

    return file_extension

def dict_to_dataframe(d):
    col = list(d.keys())[0]
    df = pd.DataFrame.from_dict(d, orient="index")
    df = df.transpose()
    df.dropna(inplace=True)
    df["image_number"] = df[col].map(lambda x: extract_image_number(x))

    df["image_number"] = df["image_number"].astype(int)

    df.sort_values(by=["image_number"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def get_dataframe_from_data(data_path=data_path):
    d = read_all_data(data_path=data_path)
    df = dict_to_dataframe(d)

    return df

def get_geojson_shape(geojson_path):
    g = gpd.read_file(geojson_path)

    return g.shape


def read_pickle(path):
    with open(path, "rb") as f:
        df = pickle.load(f)

    return df


if __name__ == "__main__":

    d = read_all_data(data_path=data_path)

