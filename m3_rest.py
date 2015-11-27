__author__ = 'JMiddleton'
from requests.auth import HTTPBasicAuth
import requests
import pprint
from settings import settings
import json

USER = settings['user']
PASSWORD = settings['password']
BASE = settings['base_exec_url']
PROGRAM = 'MMS200MI'
TRANSACTION = 'CpyItmBasic'
HEADERS = {'Accept': 'application/json'}
MAXRECS = 2
MI_PARAMS = {'BUAR': 900, 'ITNO': 'CLAB01005TESTa6', 'STAT': 10, 'ITTY': 'Z95', 'RESP': 'MOVEX', 'ITCL': '9200', 'UNMS': 'EA', 'FUDS': '0.45um RC Syringe Filter', 'ITDS': '0.45um RC Syringe Filter', 'ITGR': 'CON', 'CITN': 'Z95000'}


def m3_get(url, params, auth_dict):
    auth = HTTPBasicAuth(auth_dict['user'], auth_dict['password'])
    resp = requests.get(url, auth=auth, params=params, headers=HEADERS)
    return resp.json()


def build_mi_url(base, program, transaction, max_recs, return_columns):
    url = base + '/' + program + '/' + transaction + \
          ';maxrecs=' + str(max_recs)
    if return_columns:
        url += ';returncols=' + ','.join(return_columns)

    return url

def rest_update_call(program, transaction, params, auth_dict):
    url = build_mi_url(BASE, program, transaction, 100, [])
    result = m3_get(url, params, auth_dict)

    if result.get('@type') == 'ServerReturnedNOK':
        return result['@type'] + '\n' + result['Message']
    else:
        return 'OK'

def main():
    results = rest_update_call(PROGRAM, TRANSACTION, MI_PARAMS, {'user':USER, 'password':PASSWORD})

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(results)


if __name__ == '__main__':
    main()