"""
Module to perform analytics on Etherscan.io transactions. It works with Etherscan.io transaction files and keys as of
September 9, 2017. If Etherscan.io is to change the keys on their csv export files or API, we would need to modify
some parts of this module.
"""

import mytimeconversions as mtc


def get_contributors(transactions):
    """
    :param transactions:
    :return: Sorted list of tuples, where each tuple has the form (contributor address, value_in). Sorted by value_in
    """
    contributors = {}
    for tx in transactions:
        contributor = tx['From']
        if contributor in contributors:
            contributors[contributor] += float(tx['Value_IN(ETH)'])
        else:
            contributors[contributor] = float(tx['Value_IN(ETH)'])

    # Return a sorted list of contributors, while converting each contributor to a dict
    return [{'address': k, 'contributed (ETH)': contributors[k]}
            for k in sorted(contributors, key=lambda i: float(contributors[i]), reverse=True)]


def _create_time_intervals_list(num_buckets):
    """
    Helper method for get_txs_by_time
    :param num_buckets: see get_txs_by_time
    :return:
        [0]: list of bucket dictionaries with relevant data (see get_txs_by_time for keys)
        [1]: time interval between  of each buckets
    """
    time_buckets = []
    bucket_interval = 24 * 60 / num_buckets

    for i in range(num_buckets):
        bucket = dict()
        l_b = i * bucket_interval
        bucket['lower_bound'] = l_b

        u_b = l_b + bucket_interval
        bucket['upper_bound'] = u_b
        bucket['time_str'] = mtc.minutes_to_time_str(l_b) + '-' + mtc.minutes_to_time_str(u_b)

        bucket['num_transactions'] = 0
        bucket['total_value'] = 0

        time_buckets.append(bucket)
    return time_buckets, bucket_interval


def get_txs_by_time(transactions, num_buckets):
    """
    :param transactions: list of transactions, where each transaction is a dict
    :param num_buckets: number of time buckers. i. e. 2 would represent 00:00-12:00 and 12:00-24:00
    :return: list of bucket dictionaries with relevant data. Each bucket is a dict with the following keys:
            'lower_bound' : lower bound of bucket in minutes (inclusive)
            'upper_bound' : upper bound of bucket in minutes (exclusive)
            'time_str' : string representation of bounds, H:M-H-M
            'num_transactions' : number of transactions made in the interval (initialized to 0)
            'total_value' : total value of transactions made during time period (initialized to 0), in ETH
    """
    buckets, interval = _create_time_intervals_list(num_buckets)

    for tx in transactions:
        tx_time = mtc.timestamp_to_time_of_day(tx['UnixTimestamp'])
        index = int(tx_time / interval)
        buckets[index]['num_transactions'] += 1
        buckets[index]['total_value'] += float(tx['Value_IN(ETH)'])

    return buckets


def get_txs_by_day(transactions):
    """
    :param transactions: List of transactions
    :return: list of dictionaries, where each dict has the following keys:
            day: day of the week when transactions happened, note we include 'Weekday' and 'Weekend' too!
            num_transactions: number of transactions in specified day
            total_value: value contributed in specified day
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Weekday', 'Weekend']

    # Initialize buckets
    buckets = []
    for d in days:
        bucket = dict()
        bucket['day'] = d
        bucket['num_transactions'] = 0
        bucket['total_value'] = 0
        buckets.append(bucket)

    for tx in transactions:

        # Add transaction to day of the week
        tx_day = mtc.timestamp_to_day_of_week(tx['UnixTimestamp'])
        buckets[tx_day]['num_transactions'] += 1
        buckets[tx_day]['total_value'] += float(tx['Value_IN(ETH)'])

        # Add transaction to weekday/weekend bucket
        weekday_weekend_index = 7 if tx_day in list(range(5)) else 8
        buckets[weekday_weekend_index]['num_transactions'] += 1
        buckets[weekday_weekend_index]['total_value'] += float(tx['Value_IN(ETH)'])

    return buckets
