#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
from tqdm import tqdm
import shapefile
import json
import sys


def spatial_join():
    acris_path = sys.argv[1]
    dtm_path = sys.argv[2]
    output_path = sys.argv[3]

    documents = defaultdict(list)

    with open(acris_path) as f:
        for doc in json.load(f)['documents']:
            if doc['DocumentType'] in [
                    'DEED', 'MORTGAGE', 'DEED, OTHER'
            ] and doc['Doc Date'] != '' and doc['Party Type/Other'] == '2':
                documents[doc['Block'] + '-' + doc['Lot']].append(doc)

    with shapefile.Reader(dtm_path) as r, \
            shapefile.Writer(output_path) as w:
        w.field('block', 'N', size=10)
        w.field('lot', 'N', size=5)
        w.field('party_type', 'C', size=1)
        w.field('document_type', 'C', size=30)
        w.field('date', 'D')

        for shaperec in tqdm(r.iterShapeRecords(), total=len(r)):
            rec = shaperec.record
            key = f"{rec['BLOCK']}-{rec['LOT']}"

            if key in documents:
                for doc in documents[key]:
                    w.record(block=rec['BLOCK'],
                             lot=rec['LOT'],
                             party_type=doc['Party Type/Other'],
                             document_type=doc['DocumentType'],
                             date=datetime.strftime(
                                 datetime.strptime(doc['Doc Date'], '%m/%d/%Y'),
                                 '%Y%m%d'))
                    w.shape(shaperec.shape)


if __name__ == '__main__':
    spatial_join()
