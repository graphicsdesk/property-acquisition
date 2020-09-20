#!/usr/bin/env python3

import sys
import json


def filter_parties():
    names = set()

    with open(sys.argv[2]) as f:
        for line in f:
            name = line.strip()
            if 'COLUMBIA UNIV' in name or ('MORNINGSIDE HEIGHTS' in name and 'CORP' in name):
                names.add(name)

    sys.stdout.write(json.dumps(list(names)))


def get_all_parties():
    filename = sys.argv[2]

    with open(filename) as f:
        next(f)

        start_index = len('2005111100124001,P,2,')

        for line in f:
            i = start_index

            if line[i] == '"':
                end_char = '"'
                i += 1
            else:
                end_char = ','

            while i < len(line) and line[i] != end_char:
                sys.stdout.write(line[i])
                i += 1
            sys.stdout.write('\n')


if __name__ == '__main__':
    {
        '-all-parties': get_all_parties,
        '-filter-parties': filter_parties,
    }[sys.argv[1]]()
