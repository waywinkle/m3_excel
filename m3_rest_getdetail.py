__author__ = 'JMiddleton'
from requests.auth import HTTPBasicAuth
import requests
from bs4 import BeautifulSoup
from settings import settings

USER = settings['user']
PASSWORD = settings['password']
BASE = settings['base_meta_url']
PROGRAM = 'MMS200MI'
TRANSACTION = 'CpyItmBasic'
API_PARAMS = {}


def m3_get(url, params):
    auth = HTTPBasicAuth(USER, PASSWORD)
    resp = requests.get(url, auth=auth, params=params)
    return resp.text


def build_url(base, program):
    return base + '/' + program + '/'


def parse_mi_detail(xml, transaction, include_field_info=None):
    soup = BeautifulSoup(xml, "html.parser")

    trans = soup.find('transaction', {'transaction': transaction})

    mi_fields = []
    fields = trans.findAll('field')
    for field in fields:
        if include_field_info:
            mi_fields.append([field['description'],
                              field['fieldtype'],
                              field['length'],
                              field['mandatory'],
                              field['name']
                              ])
        else:
            mi_fields.append([field['description'],
                              field['name']
                              ])

    return mi_fields


def get_mi_detail(program, transaction):
    url = build_url(BASE, PROGRAM)
    results = m3_get(url, API_PARAMS)

    return parse_mi_detail(results, TRANSACTION)

def main():
    parsed_results = get_mi_detail(PROGRAM, TRANSACTION)

    for i in parsed_results:
        print(i)


if __name__ == '__main__':
    main()