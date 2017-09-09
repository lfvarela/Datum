"""
This module includes methods to convert between some useful time quantities. Objects we use include
datetime, time, and the unix timestamp.
"""

import datetime


def timestamp_to_day_of_week(timestamp):
    """
    Converts a unix timestamp to the day of the week int representation. i. e. 0 for Monday.
    :param timestamp: unix timestamp
    :return: int that represents day of the week
    """
    dt = timestamp_to_datetime(timestamp)
    return dt.date().weekday()


def timestamp_to_datetime(timestamp):
    """
    Converts a unix timestamp to its datetime equivalent
    :param timestamp: unix timestamp
    :return: datetime equivalent of timestamp
    """
    return datetime.datetime.utcfromtimestamp(int(timestamp))


def minutes_to_time_str(time_):
    """
    Converts time of day in minutes to a time string in the form 'H:M' i. e. minutes_to_time_str(80) returns 01:20.
    :param time_: time of day in minutes
    :return: 'time_' of day represented as a string
    """
    time_ = time_ / 60
    return '{0:02.0f}:{1:02.0f}'.format(*divmod(time_ * 60, 60))


def timestamp_to_time_of_day(timestamp):
    """
    Converts a unix timestamp into the time of the day (in minutes), on UTC timezone.
    i. e. if timestamp_to_time_of_day(x) returns 80, 80 represents 01:20 UTC
    :param timestamp: unix timestamp
    :return: time of day in minutes
    """
    dt = timestamp_to_datetime(timestamp)
    return dt.hour * 60 + dt.minute
