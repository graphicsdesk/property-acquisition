#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
import shapefile
import sys
import json


def spatial_join():
    acris_path = sys.argv[1]
    dtm_path = sys.argv[2]
    output_path = sys.argv[3]

    documents = defaultdict(list)

    with open(acris_path) as f:
        for doc in json.load(f)['documents']:
            if doc['DocumentType'] == 'DEED' and doc['Doc Date'] != '' and doc['Party Type/Other'] == '2':
                documents[doc['Block'] + '-' +
                          doc['Lot']].append(doc['Doc Date'])

    with shapefile.Reader(dtm_path) as r, \
            shapefile.Writer(output_path) as w:
        w.field('block', 'N', size=10)
        w.field('lot', 'N', size=5)
        w.field('date', 'D')

        for shaperec in r.iterShapeRecords():
            rec = shaperec.record
            key = f"{rec['BLOCK']}-{rec['LOT']}"

            if key in documents:
                for date in documents[key]:
                    w.record(block=rec['BLOCK'], lot=rec['LOT'], date=datetime.strftime(
                        datetime.strptime(date, '%m/%d/%Y'), '%Y%m%d'))
                    w.shape(shaperec.shape)


if __name__ == '__main__':
    spatial_join()
