__author__ = 'jessem'

from excel_read import get_excel_data
from m3_rest import M3_rest
import pprint
import openpyxl as xl
from settings import settings
import time

WORKBOOK = '/home/jessem/PycharmProjects/excel_interface/MMS200MI.xlsx'
AUTH = {'user': settings['user'], 'password': settings['password']}
BASE = settings['base_exec_url']

def process_file(file, username, password):
    transactions = get_excel_data(file)

    for mi in transactions:
        mi_object = M3_rest(BASE, mi['program'], mi['transaction'], mi['parameters'], username, password)
        mi['result'] = mi_object.m3_get()
        ws = mi['result_cell']['ws']
        result_cell = ws.cell(row = mi['result_cell']['row'], column = mi['result_cell']['column'])
        print(result_cell.value)
        print(mi['result'])
        result_cell.value = mi['result']
        print(result_cell.value)

    return transactions


def main():
    results = process_file(WORKBOOK, settings['user'], settings['password'])

    pp = pprint.PrettyPrinter(indent=4)

    for i in results:
        pp.pprint(i['result'])


if __name__ == '__main__':
    main()