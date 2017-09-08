# DataAnalytics.py

# TODO: Planning on learning numpy, Pandas and Matplotlib for data analysis and visualization. Also start using
#   Python notebooks
# TODO: Import data from etherscan, instead from a file

'''
From Daniel:
so we need to know what time of the day / which days / and / who were the largest contributors
 (other data vectors analysis welcomed)
so we know when to apply the most ad spend at what time / what day.
we also want to publish those results in a infographic
'''

import xlrd  # Library for developers to extract data from Microsoft Excel (tm) spreadsheet files
import datetime
import csv
import re  # Regex library


def run():
    transactions = load_transactions("Presale Data.csv")

    contributors = get_contributors(transactions)
    list_of_dicts_to_csv(contributors, "Contributors by Contribution")

    txs_by_time = get_txs_by_time(transactions, 6)
    list_of_dicts_to_csv(txs_by_time, "Transactions By Time UTC (6 buckets)")

    txs_by_day = get_txs_by_day(transactions)
    list_of_dicts_to_csv(txs_by_day, "Transactions By Day")


def list_of_dicts_to_csv(dictionaries, filename='default.csv'):
    if re.search('\.csv$', filename) is None:
        filename += '.csv'

    with open(filename, 'w') as csvfile:
        fieldnames = dictionaries[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for d in dictionaries:
            writer.writerow(d)


def load_transactions(file):
    """
    :param file: file to load. As of now it can be either an .xls or .csv file
    :return: list of transactions.
    """
    if re.search('\.csv$', file) is not None:
        return load_transactions_csv(file)

    if re.search('\.xls$', file) is not None:
        return load_transactions_xls(file)


def load_transactions_csv(csv_file):
    transactions = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if re.search('Error', row['Status']) is None:
                transactions.append(row)
    return transactions


def load_transactions_xls(xls_file):
    """
    transaction keys: ['Txhash', 'Blockno', 'UnixTimestamp', 'DateTime', 'From', 'To', 'ContractAddress',
    'Value_IN(ETH)', 'Value_OUT(ETH)', 'CurrentValue @ $345.93/Eth', 'Historical $Price/Eth', 'Status',
    'ErrCode', 'Type', '', '']
    :return: list of all transactions, where each transaction is a dictionary with keys gotten from first row in file
    """
    workbook = xlrd.open_workbook(xls_file)
    sheet = workbook.sheet_by_index(0)

    transaction_keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

    transactions = []
    for row_index in range(1, sheet.nrows):
        transaction = {transaction_keys[col_index]: sheet.cell(row_index, col_index).value
                       for col_index in range(sheet.ncols)}
        if re.search('Error', str(transaction['Status'])) is None:
            transactions.append(transaction)

    return transactions


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


def timestamp_to_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp))


def minutes_to_time_str(time_):
    """
    :param time_: time of day in minutes
    :return: time of day represented as a string. i. e. minutes_to_time_str(80) return 01:20
    """
    time_ = time_ / 60
    return '{0:02.0f}:{1:02.0f}'.format(*divmod(time_ * 60, 60))


def timestamp_to_time_of_day(timestamp):
    """
    :param timestamp: unix timestamp i. e. something like 1504688532.0
    :return: time of day in minutes, on UTC timezone. i. e. if returns 80, time would be 01:20 UTC
    """
    dt = timestamp_to_datetime(timestamp)
    return dt.hour * 60 + dt.minute


def timestamp_to_day_of_week(timestamp):
    dt = timestamp_to_datetime(timestamp)
    return dt.date().weekday()


def print_txs_by_time(txs_by_time):
    print('Transaction info:')
    for bucket in txs_by_time:
        print(bucket['time_str'] + ' : num transactions : ' + str(bucket['num_transactions'])
              + ' : value: ' + str(bucket['total_value']))
    print()


def create_time_intervals_list(num_buckets):
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
        bucket['time_str'] = minutes_to_time_str(l_b) + '-' + minutes_to_time_str(u_b)

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
    buckets, interval = create_time_intervals_list(num_buckets)

    for tx in transactions:
        tx_time = timestamp_to_time_of_day(tx['UnixTimestamp'])
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
        tx_day = timestamp_to_day_of_week(tx['UnixTimestamp'])
        buckets[tx_day]['num_transactions'] += 1
        buckets[tx_day]['total_value'] += float(tx['Value_IN(ETH)'])

        # Add transaction to weekday/weekend bucket
        weekday_weekend_index = 7 if tx_day in list(range(5)) else 8
        buckets[weekday_weekend_index]['num_transactions'] += 1
        buckets[weekday_weekend_index]['total_value'] += float(tx['Value_IN(ETH)'])

    return buckets


if __name__ == '__main__':
    run()
