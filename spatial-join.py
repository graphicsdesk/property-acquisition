#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
from tqdm import tqdm
import shapefile
import json
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def format_date(date):
    if date == '':
        return None
    date = date.split(' ')[0]
    m, d, y = date.split('/')
    return y + m.zfill(2) + d.zfill(2)


def spatial_join():
    _, acris_path, parties_path, dtm_path, output_path = sys.argv

    documents = defaultdict(list)

    with open(parties_path) as f:
        document_parties = json.load(f)

    with open(acris_path) as f:
        for doc in json.load(f):
            if doc['DocumentType'] in ['DEED', 'MORTGAGE', 'DEED, OTHER']:
                doc['parties'] = document_parties[doc['document_id']]
                documents[doc['Block'] + '-' + doc['Lot']].append(doc)

    with shapefile.Reader(dtm_path) as r, \
            shapefile.Writer(output_path) as w:
        w.field('block', 'N', size=10)
        w.field('lot', 'N', size=5)
        w.field('party_type', 'C', size=1)
        w.field('party1')
        w.field('party2')
        w.field('document_type', 'C')
        w.field('doc_date', 'D')
        w.field('recorded_date', 'D')

        for shaperec in tqdm(r.iterShapeRecords(), total=len(r)):
            record = shaperec.record
            key = f"{record['BLOCK']}-{record['LOT']}"

            if key in documents:
                for doc in documents[key]:
                    w.record(block=record['BLOCK'],
                             lot=record['LOT'],
                             party_type=doc['Party Type/Other'],
                             party1=doc['parties'][0],
                             party2=doc['parties'][1],
                             document_type=doc['DocumentType'],
                             doc_date=format_date(doc['Doc Date']),
                             recorded_date=format_date(doc['Recorded/Filed']))
                    w.shape(shaperec.shape)


if __name__ == '__main__':
    spatial_join()
