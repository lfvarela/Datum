"""
Sample script for Datum's data analytics platform. You can run this file and it should export the relevant CSV files
that we are producing from Etherscan.io transactions. Make sure you have the correct INPUT_FILE_PATH
for the transaction file you're trying to analyse. Feel free to modify parameters and play around with it.
"""


import myfilehandler as mfh
import dataanalytics as da


INPUT_FILE_PATH = 'Presale Data.csv'


def run():
    transactions = mfh.spreadsheet_to_dicts(INPUT_FILE_PATH)

    contributors = da.get_contributors(transactions)
    mfh.list_of_dicts_to_csv(contributors, 'Contributors by Contribution')

    txs_by_time = da.get_txs_by_time(transactions, 6)
    mfh.list_of_dicts_to_csv(txs_by_time, 'Transactions By Time UTC (6 buckets)')

    txs_by_day = da.get_txs_by_day(transactions)
    mfh.list_of_dicts_to_csv(txs_by_day, 'Transactions By Day')


if __name__ == '__main__':
    run()
