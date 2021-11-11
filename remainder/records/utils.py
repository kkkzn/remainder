import base64
import io

import datetime 
from dateutil.parser import parse

import numpy as np
import matplotlib.pyplot as plt


def try_parse(dt_like_str):
    try:
        dt = parse(dt_like_str)
        return dt
    except ValueError:
        return None


def encode_daily_record_graph(date: list, sleep: list, up: list, bed: list):
    # initialize the plot
    plt.clf()

    plt.rcParams['figure.subplot.bottom'] = 0.16
    
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True, figsize=(8.0, 6.0))

    # Set shared x-axis (= date)
    x = date

    # Set graph title
    ax1.set_title(f'Record for the past {len(date)} days')

    # Graph for SLEEP HOUR
    ax1.plot(x, sleep)
    ax1.grid()
    ax1.set_ylabel('sleep hour')
    # Set y-axis (min: 4hrs, max: 10hrs)
    ax1.set_ylim([
        datetime.timedelta(days=0, hours=4, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=10, seconds=0*60).total_seconds()
    ])
    ax1.set_yticks([
        datetime.timedelta(days=0, hours=5, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=6, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=7, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=8, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=9, seconds=0*60).total_seconds()
    ])
    ax1.set_yticklabels([
        '5 hrs',
        '6 hrs',
        '7 hrs',
        '8 hrs',
        '9 hrs'
    ])

    # Graph for UP TIME
    ax2.plot(x, up)
    ax2.grid()
    ax2.set_ylabel('wake-up time')
    # Set y-axis (min: 5:00, max: 10:59)
    ax2.set_ylim([
        datetime.timedelta(days=0, hours=5, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=10, seconds=59*60).total_seconds()
    ])
    ax2.set_yticks([
        datetime.timedelta(days=0, hours=6, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=7, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=8, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=9, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=10, seconds=0*60).total_seconds()
    ])
    ax2.set_yticklabels([
        '6:00',
        '7:00',
        '8:00',
        '9:00',
        '10:00'
    ])


    # Graph for BED TIME
    ax3.plot(x, bed)
    ax3.grid()
    ax3.set_ylabel('bed time')
    # Set y-axis (min: 21:00, max: 02:59)
    ax3.set_ylim([
        datetime.timedelta(days=0, hours=21, seconds=0*60).total_seconds(),
        datetime.timedelta(days=1, hours=2, seconds=59*60).total_seconds()
    ])
    ax3.set_yticks([
        datetime.timedelta(days=0, hours=22, seconds=0*60).total_seconds(),
        datetime.timedelta(days=0, hours=23, seconds=0*60).total_seconds(),
        datetime.timedelta(days=1, hours=0, seconds=0*60).total_seconds(),
        datetime.timedelta(days=1, hours=1, seconds=0*60).total_seconds(),
        datetime.timedelta(days=1, hours=2, seconds=0*60).total_seconds()
    ])
    ax3.set_yticklabels([
        '22:00',
        '23:00',
        '00:00',
        '01:00',
        '02:00'
    ])

    plt.xticks(x, rotation=90)

    # encoding
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url
