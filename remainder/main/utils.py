import base64
import datetime
import pytz
from decimal import Decimal, ROUND_HALF_UP
import io

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


# set to draw a chart (.png) on the server side
mpl.use('Agg')


def simplify(dt: datetime, to_time: bool = True) -> str:
    simplified = str(dt)[10:-3]
    if not to_time:
        simplified = str(dt)[:10]
    return simplified


def hour_min(second: int):
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    return h, m


def get_scalers(records: list):
    up_dts = [data.up for data in records]
    bed_dts = [data.to_bed for data in records]

    # create a datetime object for the beginning of the day which up-time belongs to
    # e.g. %Y-%m-%d %H:%M => %Y-%m-%d 00:00
    base_dts = [datetime.datetime.combine(up_dt.date(), datetime.time.min) for up_dt in up_dts]
    # create a datetime object for the beginning of the day before
    prev_dts = [base_dt - datetime.timedelta(days=1) for base_dt in base_dts]
    
    # TIMEDELTA between up(or bed)-time and the beginning of the day
    up_deltas = [up - base_dt for up, base_dt in zip(up_dts, base_dts)]
    bed_deltas = [bed - prev_dt for bed, prev_dt in zip(bed_dts, prev_dts)]

    # SLEEP SECOND
    sleep_sec = [up.timestamp() - bed.timestamp() for up, bed in zip(up_dts, bed_dts)]

    return base_dts, up_deltas, bed_deltas, sleep_sec


# calculate the average
def avg_delta(deltas: list):
    series = pd.Series(deltas)
    avg_td = series.sum() / len(series)
    return str(avg_td)


def estimate_remaining_of_today(sleep_sec: float, up_time: datetime, tz: str):
    # calculate the average time of being awake
    being_awake = str(86400.0 - sleep_sec)
    # round-up
    being_awake = Decimal(str(being_awake)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

    # [estimated bed_time] = [wake-up time] + [average time of being awake]
    up_unix = int(up_time.timestamp())
    bed_time_unix = up_unix + being_awake
    bed_time = datetime.datetime.fromtimestamp(float(bed_time_unix))

    # [remainder of the day] = [estimated bed_time] - [current time]
    # To support different timezones, current time and bed time are made timezone aware
    current_time_aware = datetime.datetime.now(pytz.timezone(tz))
    bed_time_aware = pytz.timezone(tz).localize(bed_time)
    remaining_sec = (bed_time_aware - current_time_aware).total_seconds()

    return bed_time, int(remaining_sec)


def config_pie(remaining_sec: int, up_time: datetime, tz: str):
    # default config: draw an empty pie chart
    config = {
        'data': [0, 0, 100],
        'labels': ['', '', ''],
        'title': ''
    }

    # If estimated_bed_time has passed, return base data-set
    if remaining_sec < 0:
        config['title'] = '[Record for Today must be added]'

    else:
        current_time_aware = datetime.datetime.now(pytz.timezone(tz))
        up_time_aware = pytz.timezone(tz).localize(up_time)
        remain = remaining_sec
        spent = int((current_time_aware - up_time_aware).total_seconds())
        wake_up_time = str(up_time)[11:-3]
        date = str(up_time.date())

        config['data'] = [0, remain, spent]

        config['labels'] = [
            'Woke up\n  at {}'.format(wake_up_time),
            'Remaining\n{0[0]}hr {0[1]}mins'.format(hour_min(remain)),
            'Spent\n{0[0]}hr {0[1]}mins'.format(hour_min(spent))
        ]

        config['title'] = date

    return config


def encode_pie_chart(config: dict):
    # define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:2]

    # initialize the plot
    plt.clf()

    # create pie chart
    plt.pie(config['data'], labels=config['labels'], colors=colors, autopct='%.0f%%', startangle=90)
    plt.gca().add_artist(plt.Circle((0, 0), 0.65, color='white'))
    plt.axis('equal')
    plt.suptitle(config['title'])
    plt.grid()

    # encoding
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url


def sql_query_to_csv(query_output, columns_to_exclude="") -> str:
    """ Converts output from a SQLAlchemy query to a .csv string.

    Cited from: https://palmo.xyz/post/20200217-sql-to-csv-in-python/

    Parameters:
    query_output (list of <class 'SQLAlchemy.Model'>): output from an SQLAlchemy query.
    columns_to_exclude (list of str): names of columns to exclude from .csv output.

    Returns:
    csv (str): query_output represented in .csv format.

    Example usage:
    users = db.Users.query.filter_by(user_id=123)
    csv = sql_query_to_csv(users, ["id", "age", "address"]
    """
    rows = query_output
    columns_to_exclude = set(columns_to_exclude)

    # create list of column names
    column_names = [i for i in rows[0].__dict__]
    for column_name in columns_to_exclude:
        column_names.pop(column_names.index(column_name))

    # add column titles to csv
    column_names.sort()
    csv = ", ".join(column_names) + "\n"

    # add rows of data to csv
    for row in rows:
        for column_name in column_names:
            if column_name not in columns_to_exclude:
                data = str(row.__dict__[column_name])
                # Escape (") symbol by preceeding with another (")
                # e.g. "XXX" => ""XXX""
                data.replace('"', '""')
                # Enclose each datum in double quotes so commas within are not treated as separators
                csv += '"' + data + '"' + ","
        csv += "\n"

    return csv
