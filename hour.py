# Eric Nordstrom
# UT Data Viz project #1

# date-time conversions specific to the Austin crime API


# dependencies
import datetime as dt


# functions

def hour(dt_str, midsep='T', round=True):
    """convert a datetime value from string-timestap format into a datetime object, rounding down to the hour if specified"""

    if len(dt_str) < 11:
        dt_str += midsep + '00:00:00'

    date, time = dt_str.split(midsep)
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')

    if round:
        minute, second = 0, 0

    return dt.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

def dt_from_string(dt_str, midsep='T', round_hour=True):
    """convert a datetime value from string-timestap format into a datetime object, rounding down to the hour if specified"""

    if len(dt_str) < 11:
        # assume missing time component
        dt_str += midsep + '00:00:00'

    # parse string
    date, time = dt_str.split(midsep)
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')

    # round
    if round_hour:
        minute, second = 0, 0

    # construct datetime object
    return dt.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

def dt_str(datetime, midsep='T'):
    """convert a datetime object into the datetime format used in the crime dataset"""

    return midsep.join(str(datetime).split())