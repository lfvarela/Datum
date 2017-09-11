"""
Sample script for Datum's data analytics platform. You can run this file and it should export the relevant CSV files
that we are producing from Etherscan.io transactions. Make sure you have the correct INPUT_FILE_PATH
for the transaction file you're trying to analyse. Feel free to modify parameters and play around with it.

This sample script gets the first k transactions up and until 3500 ETH were reached, and then deletes all the
transactions from the top 10 contributors so that those don't skew the results
"""

import sys
sys.path.append('../Modules')
import myfilehandler as mfh
import dataanalytics as da


INPUT_FILE_PATH = '/Users/lfvarela/Google Drive/Datum/Datum Pre Sale.csv'
OUTPUT_DIR = 'Results/'


def run():
    transactions = mfh.spreadsheet_to_dicts(INPUT_FILE_PATH)

    # Make list of transactions up until 3500 ETH
    transactions_3500 = []
    total_value = 0
    for i in range(len(transactions) - 1, -1, -1):  # Get them from back to front to get the first transactions
        tx = transactions[i]
        total_value += float(tx['Value_IN(ETH)'])
        transactions_3500.append(tx)
        if total_value >= 3500:
            break

    # Make set of addresses top 10 contributors for efficient lookup
    top_10_contributors = da.get_contributors(transactions)[:10]
    top_10_contributor_addresses = set()
    for cont in top_10_contributors:
        top_10_contributor_addresses.add(cont['address'])

    transactions_3500_no_top_10 = []
    for tx in transactions_3500:
        if tx['From'] not in top_10_contributor_addresses:
            transactions_3500_no_top_10.append(tx)

    mfh.list_of_dicts_to_csv(top_10_contributors, OUTPUT_DIR + 'Top 10 contributors from first 3500')

    txs_by_time = da.get_txs_by_time(transactions_3500_no_top_10, 6)
    mfh.list_of_dicts_to_csv(txs_by_time, OUTPUT_DIR + 'First 3500ETH Transactions By Time UTC No Top 10 Contributors')

    txs_by_day = da.get_txs_by_day(transactions_3500_no_top_10)
    mfh.list_of_dicts_to_csv(txs_by_day, OUTPUT_DIR + 'First 3500ETH Transactions By Day No Top 10 Contributors')

    txs_by_date = da.get_txs_by_date(transactions_3500_no_top_10)
    mfh.list_of_dicts_to_csv(txs_by_date, OUTPUT_DIR + ' First 3500ETH Transactions By Date No Top 10 Contributors')


if __name__ == '__main__':
    run()
