"""
This module is used to handle read and write files from and to python data structures. The current version supports
conversion between spreadsheets (CSV and XLS) and lists of dictionaries.
"""

import re  # regex
import csv
import xlrd  # Library for developers to extract data from Microsoft Excel (tm) spreadsheet files


def list_of_dicts_to_csv(dictionaries, filename='default.csv'):
    """
    Exports a list of dictionaries into a csv file, where the first row are the keys of the first dictionary and all
    the rows after the first are the corresponding values. It is assumed that all dictionaries have the same set of
    keys, although keys do not have to be ordered.
    :param dictionaries: list of dictionaries
    :param filename: name of csv file that will be exported
    :return: None
    """
    if re.search('\.csv$', filename) is None:
        filename += '.csv'

    with open(filename, 'w') as csvfile:
        fieldnames = dictionaries[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for d in dictionaries:
            writer.writerow(d)


def spreadsheet_to_dicts(file):
    """
    Loads a spreadsheet into a list of dictionaries, where the keys of the dictionaries are the first row of the file, and the
    values are the corresponding rows.
    :param file: file to load. We currently handle .csv and .xls files
    :return: list of dictionaries
    """
    if re.search('\.csv$', file) is not None:
        return _load_csv(file)

    if re.search('\.xls$', file) is not None:
        return _load_xls(file)


def _load_csv(csv_file):
    transactions = []
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if re.search('Error', row['Status']) is None:
                transactions.append(row)
    return transactions


def _load_xls(xls_file):
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
