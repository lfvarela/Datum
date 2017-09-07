# DataAnalytics.py

# TODO: Import data from etherscan, instead from a file

'''
From Daniel:
so we need to know what time of the day / which days / and / who were the largest contributors
 (other data vectors analysis welcomed)
so we know when to apply the most ad spend at what time / what day.
we also want to publish those results in a infographic
'''

import xlrd  # Library for developers to extract data from Microsoft Excel (tm) spreadsheet files


def run():
    transactions = get_transactions()
    contributors = get_contributors(transactions)
    print_tuple_list(contributors)


def print_tuple_list(l):
    """
    Prints all entries from a list of tuples in the form: "key: value"
    :param d: dictionary to be printed
    :return: None
    """
    for k, v in l:
        print(str(k) + ': ' + str(v))


def get_transactions():
    """
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
    for transaction in transactions:
        contributor = transaction['From']
        if contributor in contributors:
            contributors[contributor] += transaction['Value_IN(ETH)']
        else:
            contributors[contributor] = transaction['Value_IN(ETH)']
    return sort_dict_by_value(contributors)


if __name__ == '__main__':
    run()
