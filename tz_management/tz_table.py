import re
import pytz


def tz_table():
    common_timezones = pytz.common_timezones

    pattern = re.compile(r'(.*)/(.*)')

    table = []
    for entry in common_timezones:
        m = re.match(pattern, entry)
        if m is not None:
            tz = {
                'region': m.group(1),
                'city': m.group(2)
            }
            table.append(tz)

    return table
