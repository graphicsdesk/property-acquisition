#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
from tqdm import tqdm
import shapefile
import json
import sys


def spatial_join():
    _, acris_path, parties_path, dtm_path, output_path = sys.argv

    documents = defaultdict(list)

    with open(parties_path) as f:
        document_parties = json.load(f)

    with open(acris_path) as f:
        for doc in json.load(f)['documents']:
            if (doc['DocumentType'] in ['DEED', 'MORTGAGE', 'DEED, OTHER']
                    and doc['Doc Date'] != ''):
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
        w.field('date', 'D')

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
                             date=datetime.strftime(
                                 datetime.strptime(doc['Doc Date'],
                                                   '%m/%d/%Y'), '%Y%m%d'))
                    w.shape(shaperec.shape)


if __name__ == '__main__':
    spatial_join()
