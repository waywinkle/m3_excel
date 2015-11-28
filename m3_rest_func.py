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
MI_PARAMS = {'BUAR': 900, 'ITNO': 'CLABTEST06', 'STAT': 10, 'ITTY': 'Z95', 'RESP': 'MOVEX', 'ITCL': '9200', 'UNMS': 'EA', 'FUDS': '0.45um RC Syringe Filter', 'ITDS': '0.45um RC Syringe Filter', 'ITGR': 'CON', 'CITN': 'Z95000'}


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

    # return result['MIRecord'][0]['NameValue']
    return process_result(result)


def process_result(result):
    if result.get('@type') == 'ServerReturnedNOK':
        return result['@type'] + ' : ' + remove_extra_space(result['Message'])
    else:
        return result['Program'] + ':' + result['Transaction'] + ', ' + \
               'Name=' + result['MIRecord'][0]['NameValue'][0]['Name'] + ', ' + \
               'Value=' + result['MIRecord'][0]['NameValue'][0]['Value']


def remove_extra_space(string):
    last = ''
    new_string = ''
    for i in string:
        if last == ' ' and i == ' ':
            pass
        else:
            new_string += i
        last = i

    return new_string


def main():
    results = rest_update_call(PROGRAM, TRANSACTION, MI_PARAMS, {'user':USER, 'password':PASSWORD})

    print(type(results))

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(results)


if __name__ == '__main__':
    main()