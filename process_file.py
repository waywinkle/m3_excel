__author__ = 'jessem'

from excel_read import get_excel_data
from m3_rest import rest_update_call
import pprint

WORKBOOK = '/home/jessem/PycharmProjects/excel_interface/MMS200MI.xlsx'

def process_file(file):
    transactions = get_excel_data(file)

    for mi in transactions:
        for row in mi['process_rows']:
            mi['result'] = rest_update_call(mi['program'], mi['transaction'], row)

    return transactions


def main():
    results = process_file(WORKBOOK)

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(results)


if __name__ == '__main__':
    main()