#!/usr/bin/env python3

import argparse
import csv
import logging
import xml.etree.ElementTree as ET

import redis

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to XML and store in Redis')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('--redis_host', type=str, help='Redis host address', default='127.0.0.1')
    parser.add_argument('--redis_port', type=int, help='Redis port number', default=6379)
    parser.add_argument('--redis_db', type=int, help='Redis database number', default=0)
    parser.add_argument('--expire_time', type=int, help='Redis database number', default=172800)
    args = parser.parse_args()

    logging.basicConfig(
      format='%(asctime)s | %(levelname)s | %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S',
      level=logging.DEBUG
    )
    redis_client = redis.Redis(host=args.redis_host, port=args.redis_port, db=args.redis_db)

    with open(args.csv_file, 'r') as file:
        try:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for (recno, row) in enumerate(csv_reader):
                if (recno % 10000) == 0: logging.info(recno)
                redis_key = row[0] # Assuming the first column is the key for Redis
                root = ET.Element("data")
                item = ET.SubElement(root, "item")
                for i, field in enumerate(row):
                    ET.SubElement(item, header[i]).text = field
                redis_client.set(redis_key, ET.tostring(root, encoding='utf-8').decode(), ex=args.expire_time)
        except Exception as e:
            logging.error(e)

if __name__ == '__main__':
    main()

