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

    start = timer()
    for k in random.sample(key_list,10):
     try:
       print(redis_client.get(k).decode('utf-8'))
     except:
       print(f'{k} not found')
    end = timer()
    print(f'Elapse {end - start}s')

if __name__ == '__main__':
    main()

