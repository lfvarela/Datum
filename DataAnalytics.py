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


def run():
    transactions = get_transactions()
    contributors = get_contributors(transactions)
    print_tuple_list(contributors, "Contributor address: value contributed")
    txs_by_time = get_txs_by_time(transactions, 6)
    print_txs_by_time(txs_by_time)


def print_tuple_list(l, message=None):
    """
    Prints all entries from a list of tuples in the form: "key: value"
    :param l: list to be printed
    :param message: optional print message
    :return: None
    """
    if message is not None:
        print(message)
    for k, v in l:
        print(str(k) + ': ' + str(v))
    print()


def get_transactions():
    """
    transaction keys: ['Txhash', 'Blockno', 'UnixTimestamp', 'DateTime', 'From', 'To', 'ContractAddress',
    'Value_IN(ETH)', 'Value_OUT(ETH)', 'CurrentValue @ $345.93/Eth', 'Historical $Price/Eth', 'Status',
    'ErrCode', 'Type', '', '']
    :return: list of all transactions, where each transaction is a dictionary with keys gotten from first row in file
    """
    workbook = xlrd.open_workbook("20170906 Datum XLS.xls")
    sheet = workbook.sheet_by_index(0)

    transaction_keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

    transactions = []
    for row_index in range(1, sheet.nrows):
        transaction = {transaction_keys[col_index]: sheet.cell(row_index, col_index).value
                       for col_index in range(sheet.ncols)}
        transactions.append(transaction)

    return transactions


def sort_dict_by_value(d):
    """
    :param d: dictionary to be sorted
    :return: sorted dictionary by value
    """
    s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    return s


def get_contributors(transactions):
    """
    :param transactions:
    :return: Sorted list of tuples, where each tuple has the form (contributor address, value_in). Sorted by value_in
    """
    contributors = {}
    for tx in transactions:
        contributor = tx['From']
        if contributor in contributors:
            contributors[contributor] += tx['Value_IN(ETH)']
        else:
            contributors[contributor] = tx['Value_IN(ETH)']
    return sort_dict_by_value(contributors)


def minutes_to_time_str(time_):
    """
    :param time_: time of day in minutes
    :return:
    """
    time_ = time_ / 60
    return '{0:02.0f}:{1:02.0f}'.format(*divmod(time_ * 60, 60))


def timestamp_to_time_of_day(timestamp):
    """
    :param timestamp: unix timestamp i. e. something like 1504688532.0
    :return: time of day in minutes, on UTC timezone. i. e. if returns 80, time would be 01:20 UTC
    """
    dt = datetime.datetime.utcfromtimestamp(int(timestamp))
    return dt.hour * 60 + dt.minute


def print_txs_by_time(txs_by_time):
    print('Transaction info:')
    for bucket in txs_by_time:
        print(bucket['time_str'] + ' : num transactions : ' + str(bucket['num_transactions'])
              + ' : value: ' + str(bucket['total_value']))
    print()


def create_time_intervals_list(num_buckets):
    """
    :param num_buckets: number of time buckets. i. e. if 2, 2 buckets: one for 00:00-12:00 and one for 12:00-24:00
    :return:
        [0]: list of bucket dictionaries with relevant data. Keys for each bucket are:
        'lower_bound' : lower bound of bucket in minutes (inclusive)
        'upper_bound' : upper bound of bucket in minutes (exclusive)
        'time_str' : string representation of bounds, H:M-H-M
        'num_transactions' : number of transactions made in the interval (initialized to 0)
        'total_value' : total value of transactions made during time period (initialized to 0), in ETH
        [1]: interval between buckets
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
    TODO: add docs
    """

    buckets, interval = create_time_intervals_list(num_buckets)

    for tx in transactions:
        tx_time = timestamp_to_time_of_day(tx['UnixTimestamp'])
        index = int(tx_time / interval)
        buckets[index]['num_transactions'] += 1
        buckets[index]['total_value'] += tx['Value_IN(ETH)']

    return buckets


if __name__ == '__main__':
    run()
