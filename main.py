#! /home/mohammedi/workspace/speedtest/venv/bin/python
from pathlib import Path

from speedtest_monitor.speed_utils import (
    measure,
    parse_speed,
    print_speed,
    save_speed_csv,
    save_speed_graphs,
    PathLike,
)

HOME = Path.home()

BASE = HOME / 'speedtest'


def main(
    download: bool = True,
    upload: bool = False,
    csv_path: PathLike = BASE / 'speedtest.csv',
    graphs_path: PathLike = BASE / 'graphs',
):
    speed = measure(download, upload)
    speed_dict = parse_speed(speed)
    print_speed(speed_dict)
    save_speed_csv(speed_dict, csv_path)
    save_speed_graphs(csv_path, graphs_path)


if __name__ == '__main__':
    main()
