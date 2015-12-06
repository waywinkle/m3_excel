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
TRANSACTION = 'CpyItmWhs'
HEADERS = {'Accept': 'application/json'}
MAXRECS = 2
#MI_PARAMS = {'BUAR': 900, 'ITNO': 'CLABTEST08', 'STAT': 10, 'ITTY': 'Z95', 'RESP': 'MOVEX', 'ITCL': '9200', 'UNMS': 'EA', 'FUDS': '0.45um RC Syringe Filter', 'ITDS': '0.45um RC Syringe Filter', 'ITGR': 'CON', 'CITN': 'Z95000'}
MI_PARAMS = {'CONO': 100, 'ITNO': 'CLAB1TEST13'}

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
        try:
            return self._process_result(resp.json())
        except ValueError:
            result_text = resp.text
            if '<h2>Unauthorized</h2>' in result_text:
                return 'Unauthorized user'

            return resp.text

    def _process_result(self, result):
        if result.get('@type') == 'ServerReturnedNOK':
            return result['@type'] + ' : ' + self._remove_extra_space(result['Message'])
        elif result.get('@type') == 'MandatoryInputFieldNotFound':
            return result['Message']
        else:
            return 'Transaction OK! : ' + \
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