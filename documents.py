#!/usr/bin/env python3

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import multiprocessing as mp
import itertools
import asyncio
import requests
import json
import sys

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_parties():

    with open(sys.argv[2]) as f:
        documents = list(
            set(doc['document_id'] for doc in json.load(f)
                if doc['DocumentType'] in ['DEED', 'MORTGAGE', 'DEED, OTHER']))

    async def get_document(doc_id, client):
        async with client.get(
                'https://a836-acris.nyc.gov/DS/DocumentSearch/DocumentDetail',
                params=(('doc_id', doc_id), )) as response:
            soup = BeautifulSoup(await response.read(), 'lxml')
            party_names = []

            for party_table in soup.body.find_all(
                    'table', recursive=False)[3].td.find_all(
                        'table', recursive=False)[2].find_all('tr',
                                                              recursive=False):
                name = party_table.td.div.font.text.strip()
                if name != '':
                    party_names.append(name)

            return (doc_id, party_names)

    async def get_all_documents():
        async with ClientSession(headers={'user-agent': USER_AGENT}) as client:

            tasks = [get_document(doc_id, client) for doc_id in documents]
            return [
                await f
                for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))
            ]

    sys.stdout.write(json.dumps(dict(asyncio.run(get_all_documents()))))


def scrape_acris():

    with open('./party-search/names.json') as f:
        names = json.load(f)

    def search_name(session, name):
        cookies = {
            '__RequestVerificationToken_L0RT':
            'Pd9WJCBuNHbm8mveovl484x0TLGVr6zODB2JbY3yu+YB869EJOvp1KEpmBUQpj0euo9a8D3ndTzMDDu3lUweC5ZAaT9VYxHjYfqAGGMDXMsvRmqT2KBUmhOH8MKZL77wu6I84+aw+qXtSNnMTf7n59cYJrHxZTf5RYIoDYVOvZc=',
        }
        headers = {'user-agent': USER_AGENT}
        data = {
            '__RequestVerificationToken':
            'Ur6XUdRsPQXwOFJshdldobB6iY8ZTdcCj+oWldpt/jHPCxsN7WfRQFqcf0sdYP9Eb4wBYMi5oDWHYPShKU0w1FiyZHPjfW9WbFFPamJFDTc+nsPT/oR9Z320sre66M3L/3EIvd4YxucWOvm+b71KIBPFiJx2DYZEQYC04+H1bh4=',
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

        with session.post(
                'https://a836-acris.nyc.gov/DS/DocumentSearch/PartyNameResult',
                data=data,
                headers=headers,
                cookies=cookies) as response:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return {'time': time, 'name': name, 'html': response.text}

    output = []
    with requests.Session() as session:
        for name in tqdm(names):
            output.append(search_name(session, name))

    sys.stdout.write(json.dumps(output))


def scrape_acris_old():

    cookies = {
        '__RequestVerificationToken_L0RT':
        'Pd9WJCBuNHbm8mveovl484x0TLGVr6zODB2JbY3yu+YB869EJOvp1KEpmBUQpj0euo9a8D3ndTzMDDu3lUweC5ZAaT9VYxHjYfqAGGMDXMsvRmqT2KBUmhOH8MKZL77wu6I84+aw+qXtSNnMTf7n59cYJrHxZTf5RYIoDYVOvZc=',
    }

    with open(sys.argv[2]) as f:
        names = json.load(f)

    async def search_name(name, client):
        data = {
            '__RequestVerificationToken':
            'Ur6XUdRsPQXwOFJshdldobB6iY8ZTdcCj+oWldpt/jHPCxsN7WfRQFqcf0sdYP9Eb4wBYMi5oDWHYPShKU0w1FiyZHPjfW9WbFFPamJFDTc+nsPT/oR9Z320sre66M3L/3EIvd4YxucWOvm+b71KIBPFiJx2DYZEQYC04+H1bh4=',
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

        async with client.post(
                'https://a836-acris.nyc.gov/DS/DocumentSearch/PartyNameResult',
                data=data) as response:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            eprint(len(await response.text()))
            return {'time': time, 'name': name, 'html': await response.text()}

    async def search_all_names():
        async with ClientSession(headers={'user-agent': USER_AGENT},
                                 cookies=cookies) as client:
            tasks = [search_name(name, client) for name in names][:2]
            return [
                await f
                for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))
            ]

    sys.stdout.write(json.dumps(asyncio.run(search_all_names())))


def parse_search_page(doc):
    soup = BeautifulSoup(doc['html'], 'lxml')

    output = []
    headers = None

    for row in soup.form.tbody.table.find_all('tr', recursive=False):
        values = row.find_all('td', recursive=False)
        if headers is None:
            headers = [
                v.font.text.strip().replace('  ',
                                            '').replace('/\n', '/').replace(
                                                '\n', ' ').replace('\r ', '')
                for v in values
            ]
            headers[0] = 'document_id'
            continue

        # Onclicks are formatted like: JavaScript:go_detail("FT_1330008712333")
        document = dict(zip(headers[1:], [v.text.strip() for v in values[1:]]))
        document[headers[0]] = values[0].font.input['onclick'][-18:-2]

        output.append(document)

    return output


def parse_results():
    with open(sys.argv[2]) as f:
        documents = json.load(f)

    pool = mp.Pool(mp.cpu_count())
    results = list(
        tqdm(pool.imap(parse_search_page, [doc for doc in documents]),
             total=len(documents)))
    pool.close()

    print(json.dumps(list(itertools.chain.from_iterable(results)), indent=2))

    # Store search critera and date in the output as metadata
    # output['meta'] = soup.body.find_all('table', recursive=False)[3].table.font.find_next(
    # 'font').text.replace(u'\xa0', u' ').replace('  ', '').replace(':\n', ':').replace('\n\n', '\n').strip()


if __name__ == '__main__':
    {
        '-scrape-acris': scrape_acris,
        '-parse-results': parse_results,
        '-get-parties': get_parties,
    }[sys.argv[1]]()
