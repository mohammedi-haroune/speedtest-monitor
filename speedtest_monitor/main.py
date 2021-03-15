#! /home/mohammedi/workspace/speedtest/venv/bin/python
import os
import argparse
from pathlib import Path

from speedtest_monitor.speed_utils import (
    install_cron,
    measure,
    parse_speed,
    print_speed,
    save_speed_csv,
    save_speed_graphs,
    PathLike,
)

DEFAULT = Path.home().joinpath('.speedtest').as_posix()

def parse_args():
    """The command line arguments parser"""
    parser = argparse.ArgumentParser(description='Measure internet speed then save the result and update the graphs')
    parser.add_argument('--output-dir', type=str, default=DEFAULT,
                        help='Where to save the output. Default to ~/.speedtest')
    parser.add_argument('--download', action="store_false", default=True,
                        help='Wether to measure download speed or not. Defaults to True')
    parser.add_argument('--upload', action="store_true", default=False,
                        help='Wether to measure upload speed or not. Defaults to False')
    parser.add_argument('--install-cron', action="store_true", default=False,
                        help='Install the crontab to the current user and quit. Defaults to False')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.install_cron:
        install_cron()
        exit()

    csv_path: PathLike = os.path.join(args.output_dir, 'speedtest.csv')
    graphs_path: PathLike = os.path.join(args.output_dir, 'graphs')
    speed = measure(args.download, args.upload)
    speed_dict = parse_speed(speed)
    print_speed(speed_dict)
    save_speed_csv(speed_dict, csv_path)
    save_speed_graphs(csv_path, graphs_path)


if __name__ == '__main__':
    main()
