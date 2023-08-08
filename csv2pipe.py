#!/usr/bin/env python3

import csv
import sys
import xml.etree.ElementTree as ET

def main():
    try:
        csv_reader = csv.reader(sys.stdin)
        header = next(csv_reader)
        for (recno, row) in enumerate(csv_reader):
            redis_key = row[0]
            root = ET.Element("data")
            item = ET.SubElement(root, "item")
            for i, field in enumerate(row):
                ET.SubElement(item, header[i]).text = field
            print('SET "usr:{}" "{}"'.format(redis_key, ET.tostring(root, encoding='utf-8').decode()), flush=True)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

