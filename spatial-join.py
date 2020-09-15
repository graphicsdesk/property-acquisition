#!/usr/bin/env python3

from collections import defaultdict
from datetime import datetime
import shapefile
import sys
import json


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def hash_lot(doc):
    return doc['Block'] + '-' + doc['Lot']


def spatial_join(): # 50s
    documents = defaultdict(list)

    with open(sys.argv[2]) as f:
        # print(len([x for x in json.load(f)['documents'] if x['DocumentType'] == 'DEED' and x['Doc Date'] != '']))
        for doc in json.load(f)['documents']:
            if doc['DocumentType'] == 'DEED' and doc['Doc Date'] != '':
                documents[doc['Block'] + '-' + doc['Lot']].append(doc['Doc Date'])

    with shapefile.Reader('Digital_Tax_Map_20200828/DTM_Tax_Lot_Polygon.shp') as r, \
            shapefile.Writer('test.shp') as w:
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
                    print('yeet')


def main():
    {
        '-spatial-join': spatial_join,
    }[sys.argv[1]]()


if __name__ == '__main__':
    main()
