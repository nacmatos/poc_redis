#!/usr/bin/env python3

import csv
import argparse
import random
from timeit import default_timer as timer

import redis

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to XML and store in Redis')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('redis_host', type=str, help='Redis host address')
    parser.add_argument('redis_port', type=int, help='Redis port number')
    parser.add_argument('redis_db', type=int, help='Redis database number')
    args = parser.parse_args()

    redis_client = redis.Redis(host=args.redis_host, port=args.redis_port, db=args.redis_db)

    key_list=[]
    with open(args.csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for i, row in enumerate(csv_reader):
            key_list.append(row[0])

    while True:
        k=random.sample(key_list,1)
        start = timer()
        try:
            xml=redis_client.get(k[0]).decode('utf-8')
        except:
            xml='not found'
        end = timer()
        print(f'{end - start}s | {xml[0:35]}')

if __name__ == '__main__':
    main()

