import csv
import os
import typing
from textwrap import dedent

import pytz
import pandas as pd

import speedtest
from plot import plot_functions

PathLike = typing.Union[str, bytes, os.PathLike]

DZ = pytz.timezone('Africa/Algiers')

def measure(
    download: bool = True,
    upload: bool = False
) -> speedtest.Speedtest:
    servers = []
    # If you want to test against a specific server
    # servers = [1234]
    threads = None
    # If you want to use a single threaded test
    # threads = 1
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    if download:
        s.download(threads=threads)
    if upload:
        s.upload(threads=threads)
    return s


def parse_speed(speed: speedtest.Speedtest) -> dict:
    results_dict = speed.results.dict()
    return results_dict


def is_empty(path: PathLike) -> bool:
    if not os.path.exists(path):
        return True

    with open(path, 'r') as f:
        if f.read() == '':
            return True
    return False


FIELDS = ['timestamp', 'download', 'ping']


def save_speed_csv(speed_dict: dict, path: PathLike, fields: list = None) -> dict:
    if fields is None:
        fields = FIELDS

    row = {field: speed_dict[field] for field in fields}

    # Write csv header only if the file is empty
    writeheader = is_empty(path)

    with open(path, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if writeheader:
            writer.writeheader()
        writer.writerow(row)

    return row


def print_speed(speed_dict: dict):
    mbps = round(speed_dict['download'] / 10e5, 2)
    ping = int(speed_dict['ping'])
    format = dedent(f'''
    Download : {mbps:5.2f} Mbps
    Latency  : {ping:5d} ms
    ''').strip()
    print(format.format(mbps=mbps))


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df.download = df.download.map(lambda d: round(d/10e5, 2))
    df.timestamp = pd.to_datetime(df.timestamp).map(lambda t: t.astimezone(tz=DZ))
    df.index = df.timestamp
    return df


def save_speed_graphs(csv_path, directory):
    df = pd.read_csv(csv_path)
    df = preprocess(df)
    for plot in plot_functions:
        plot(df, directory)
