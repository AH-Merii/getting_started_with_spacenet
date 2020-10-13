import pandas as pd
import numpy as np
from pathlib import Path
import re

data_path = Path(
    "/home/ahm/Datascience/Satellite Imagery Detection/getting_started_with_spacenet/processedBuildingLabels/data"
)


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


def dict_to_dataframe(d):
    col = list(d.keys())[0]
    df = pd.DataFrame(d)
    df["image_number"] = df[col].map(lambda x: extract_image_number(x))

    df["image_number"] = df["image_number"].astype(int)

    df.sort_values(by=["image_number"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def get_dataframe_from_data(data_path=data_path):
    d = read_all_data(data_path=data_path)
    df = dict_to_dataframe(d)

    return df


if __name__ == "__main__":

    d = read_all_data(data_path=data_path)
    df = dict_to_dataframe(d)
    print(df.head())
    print(df["3band"][7])
    print(df["8band"][7])
    print(df["geojson"][7])
    print("complete")
