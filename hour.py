def hour(crimedt):
    """convert a datetime value from the crime dataset into a datetime object, rounding down to the hour"""

    date, time = crimedt.split('T')
    year, month, day = date.split('-')
    hour, *_ = time.split(':')

    return dt.datetime(int(year), int(month), int(day), int(hour))