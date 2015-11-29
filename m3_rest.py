__author__ = 'JMiddleton'
from requests.auth import HTTPBasicAuth
from requests import get
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
MI_PARAMS = {'BUAR': 900, 'ITNO': 'CLABTEST08', 'STAT': 10, 'ITTY': 'Z95', 'RESP': 'MOVEX', 'ITCL': '9200', 'UNMS': 'EA', 'FUDS': '0.45um RC Syringe Filter', 'ITDS': '0.45um RC Syringe Filter', 'ITGR': 'CON', 'CITN': 'Z95000'}


class M3_rest:

    def __init__(self,
                 url,
                 program,
                 transaction,
                 parameters,
                 username,
                 password,
                 return_column=None
                 ):

        self.request_url = self._build_mi_url(url, program, transaction, 10, [])
        self.auth = HTTPBasicAuth(username, password)
        self.parameters = parameters

    def _build_mi_url(self, base_url, program, transaction, max_recs, return_columns):
        url = base_url + '/' + program + '/' + transaction + \
              ';maxrecs=' + str(max_recs)
        if return_columns:
            url += ';returncols=' + ','.join(return_columns)
        return url

    def m3_get(self):
        resp = get(self.request_url,
                   auth=self.auth,
                   params=self.parameters,
                   headers={'Accept': 'application/json'})
        result = resp.json()

        return self._process_result(result)

    def _process_result(self, result):
        if result.get('@type') == 'ServerReturnedNOK':
            return result['@type'] + ' : ' + self._remove_extra_space(result['Message'])
        else:
            return 'Transaction OK! : ' + \
                result['Program'] + ':' + result['Transaction'] + ', ' + \
                'Name=' + result['MIRecord'][0]['NameValue'][0]['Name'] + ', ' + \
                'Value=' + result['MIRecord'][0]['NameValue'][0]['Value']

    def _remove_extra_space(self, string):
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
    mi = M3_rest(BASE,
                 PROGRAM,
                 TRANSACTION,
                 MI_PARAMS,
                 USER,
                 PASSWORD)

    result = mi.m3_get()

    print(type(result))

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(result)

if __name__ == '__main__':
    main()