"""
Sample script to use dataanalytics.get_contributors_tokens(contributor_addresses) properly
"""

import myfilehandler as mfh
import dataanalytics as da


INPUT_FILE_PATH = '/Users/lfvarela/Google Drive/Datum/Datum Pre Sale.csv'
OUTPUT_DIR = 'Results/'


def run():
    transactions = mfh.spreadsheet_to_dicts(INPUT_FILE_PATH)

    contributors = da.get_contributors(transactions)
    contributor_addresses = [c['address'] for c in contributors]

    contributor_tokens = da.get_contributors_tokens(contributor_addresses)
    mfh.list_of_dicts_to_csv(contributor_tokens, OUTPUT_DIR + 'Tokens Contributors Hold')


if __name__ == '__main__':
    run()
