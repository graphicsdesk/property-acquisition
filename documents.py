#!/usr/bin/env python3

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def scrape_acris():
    cookies = {
        '__RequestVerificationToken_L0RT': 'Pd9WJCBuNHbm8mveovl484x0TLGVr6zODB2JbY3yu+YB869EJOvp1KEpmBUQpj0euo9a8D3ndTzMDDu3lUweC5ZAaT9VYxHjYfqAGGMDXMsvRmqT2KBUmhOH8MKZL77wu6I84+aw+qXtSNnMTf7n59cYJrHxZTf5RYIoDYVOvZc=',
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }

    with open(sys.argv[2]) as f:
        names = json.load(f)

    sys.stdout.write('[')

    for i, name in enumerate(names):
        if i != 0:
            sys.stdout.write(',')

        data = {
            '__RequestVerificationToken': 'Ur6XUdRsPQXwOFJshdldobB6iY8ZTdcCj+oWldpt/jHPCxsN7WfRQFqcf0sdYP9Eb4wBYMi5oDWHYPShKU0w1FiyZHPjfW9WbFFPamJFDTc+nsPT/oR9Z320sre66M3L/3EIvd4YxucWOvm+b71KIBPFiJx2DYZEQYC04+H1bh4=',
            'hid_last': '',
            'hid_first': '',
            'hid_ml': '',
            'hid_suffix': '',
            'hid_business': name,
            'hid_selectdate': 'To Current Date',
            'hid_datefromm': '',
            'hid_datefromd': '',
            'hid_datefromy': '',
            'hid_datetom': '',
            'hid_datetod': '',
            'hid_datetoy': '',
            'hid_partype': '',
            'hid_borough': '0',
            'hid_doctype': 'All Document Classes',
            'hid_max_rows': '9999',
            'hid_page': '2',
            'hid_partype_name': 'All Parties',
            'hid_doctype_name': 'All Document Classes',
            'hid_borough_name': 'All Boroughs/Counties',
            'hid_ReqID': '',
            'hid_SearchType': 'PARTYNAME',
            'hid_ISIntranet': 'N',
            'hid_sort': ''
        }

        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = requests.post('https://a836-acris.nyc.gov/DS/DocumentSearch/PartyNameResult',
                                 headers=headers, cookies=cookies, data=data)

        sys.stdout.write(json.dumps(
            {
                'time': time,
                'name': name,
                'html': response.text
            }))

        eprint(f'{name}; response length: {len(response.text)}')

    sys.stdout.write(']')


def parse_results():
    with open(sys.argv[2]) as f:
        documents = json.load(f)

    output = {
        'documents': [],
        'meta': None,
    }

    for i, document in enumerate(documents):
        eprint(i)
        soup = BeautifulSoup(document['html'], 'lxml')

        headers = None

        for row in soup.form.tbody.table.find_all('tr', recursive=False):
            values = row.find_all('td', recursive=False)[1:]
            if headers is None:
                headers = [v.font.text.strip().replace('  ', '').replace(
                    '/\n', '/').replace('\n', ' ').replace('\r ', '') for v in values]
                continue

            output['documents'].append(dict(zip(headers, [v.text.strip() for v in values])))

    eprint(len(output['documents']))

    # Store search critera and date in the output as metadata
    # output['meta'] = soup.body.find_all('table', recursive=False)[3].table.font.find_next(
        # 'font').text.replace(u'\xa0', u' ').replace('  ', '').replace(':\n', ':').replace('\n\n', '\n').strip()

    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    {
        '-scrape-acris': scrape_acris,
        '-parse-results': parse_results,
    }[sys.argv[1]]()
