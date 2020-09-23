import requests
from aiohttp import ClientSession
import asyncio
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'

def sync_search_name(name):

    cookies = {
        '__RequestVerificationToken_L0RT':
        'Pd9WJCBuNHbm8mveovl484x0TLGVr6zODB2JbY3yu+YB869EJOvp1KEpmBUQpj0euo9a8D3ndTzMDDu3lUweC5ZAaT9VYxHjYfqAGGMDXMsvRmqT2KBUmhOH8MKZL77wu6I84+aw+qXtSNnMTf7n59cYJrHxZTf5RYIoDYVOvZc=',
    }

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

    response = requests.post(
            'https://a836-acris.nyc.gov/DS/DocumentSearch/PartyNameResult',
            data=data,headers={'user-agent': USER_AGENT},cookies=cookies)
    print(len(response.content))

async def async_search_name(name, client):

    cookies = {
        '__RequestVerificationToken_L0RT':
        'Pd9WJCBuNHbm8mveovl484x0TLGVr6zODB2JbY3yu+YB869EJOvp1KEpmBUQpj0euo9a8D3ndTzMDDu3lUweC5ZAaT9VYxHjYfqAGGMDXMsvRmqT2KBUmhOH8MKZL77wu6I84+aw+qXtSNnMTf7n59cYJrHxZTf5RYIoDYVOvZc=',
    }

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
            data=data,headers={'user-agent': USER_AGENT},cookies=cookies) as response:
        print(await response.read())

async def main():
    async with ClientSession() as client:
        await async_search_name('COLUMBIA UNIVERSITY (TRUSTEES OF)', client)

# asyncio.run(main())

async def main():
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None, 
            sync_search_name,
            'COLUMBIA UNIVERSITY (TRUSTEES OF)',
        )
        for i in range(10)
    ]
    for response in await asyncio.gather(*futures):
        pass

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

responses = [
    sync_search_name('COLUMBIA UNIVERSITY (TRUSTEES OF)')
    for i in range(20)
]