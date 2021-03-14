import os
import math
from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import pytz
from matplotlib.ticker import IndexLocator

from .time_utils import group_by

DZ = pytz.timezone('Africa/Algiers')

def plot_download(
    data,
    minor=None,
    major=None,
    fmt=None,
    autofmt=True,
    save_to=None,
    xlabel='Time',
    ylabel='Download (Mbps)',
):
    fig, ax = plt.subplots()
    if not isinstance(data, list):
        data = [data]

    for d in data:
        ax.plot('timestamp', 'download', data=d)

    # format the ticks
    if major:
        ax.xaxis.set_major_locator(major)
    if minor:
        ax.xaxis.set_minor_locator(minor)
    if fmt:
        ax.xaxis.set_major_formatter(fmt)

    ax.set_yticks(list(range(0, 21, 1)))
    ax.set_ylim(0, 20)

    ax.grid(True)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    if autofmt:
        fig.autofmt_xdate()
        
    if save_to:
        plt.savefig(save_to, dpi=200)
    
    return fig, ax


def plot_all(
    df: pd.DataFrame,
    directory,
    scope='1-day',
):
    all_min = group_by(df, scope=scope, agg='min')
    all_max = group_by(df, scope=scope, agg='max')

    duration = df.timestamp.max() - df.timestamp.min()
    number_of_days = duration.days
    max_ticks = 10

    interval = math.ceil(number_of_days / max_ticks)

    days = mdates.DayLocator(interval=interval)
    hours = mdates.HourLocator(interval=4)
    days_fmt = mdates.DateFormatter('%d %b %Y')

    save_to = os.path.join(directory, 'all.png')

    aggregated_by = scope.replace('-', ' ')
    xlabel = f'Time (Aggregated by {aggregated_by})'

    plot_download(
        # minor=hours,
        major=days,
        fmt=days_fmt,
        data=[all_min, all_max],
        save_to=save_to,
        xlabel=xlabel,
    )


def plot_last_10_days(
    df: pd.DataFrame,
    directory,
    scope='4-hours',
):
    now = datetime.now(tz=DZ)
    aday = timedelta(days=10)
    last_10_days = df[df.timestamp.map(lambda t: now - t <= aday)]
    last_10_days_min = group_by(last_10_days, scope=scope, agg='min')
    last_10_days_max = group_by(last_10_days, scope=scope, agg='max')

    days = mdates.DayLocator()
    hours = mdates.HourLocator(interval=4)
    days_fmt = mdates.DateFormatter('%d %b %Y')

    save_to = os.path.join(directory, 'last_10_days.png')

    aggregated_by = scope.replace('-', ' ')
    xlabel = f'Time (Aggregated by {aggregated_by})'

    plot_download(
        minor=hours,
        major=days,
        fmt=days_fmt,
        data=[last_10_days_min, last_10_days_max],
        save_to=save_to,
        xlabel=xlabel,
    )


def plot_today(
    df: pd.DataFrame,
    directory,
    scope='1-hour',
):
    now = datetime.now(tz=DZ)
    aday = timedelta(days=1)
    today = df[df.timestamp.map(lambda t: now - t <= aday)]

    today_min = group_by(today, scope=scope, agg='min')
    today_max = group_by(today, scope=scope, agg='max')

    hours_major = mdates.HourLocator(interval=4)
    hours_minor = mdates.HourLocator()
    days_fmt = mdates.DateFormatter('%H:%M')

    save_to = os.path.join(directory, 'today.png')

    aggregated_by = scope.replace('-', ' ')
    xlabel = f'Time (Aggregated by {aggregated_by})'

    return plot_download(
        minor=hours_minor,
        major=hours_major,
        fmt=days_fmt,
        data=[today_min, today_max],
        autofmt=False,
        save_to=save_to,
        xlabel=xlabel,
    )


plot_functions = [
    plot_all,
    plot_last_10_days,
    plot_today,
]
