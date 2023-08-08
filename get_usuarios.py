#!/usr/bin/env python3

import argparse
import csv
import logging
import random
from timeit import default_timer as timer

import redis

def main():
    parser = argparse.ArgumentParser(description='Retrive all keys and sample 10 and timeit')
    parser.add_argument('--redis_host', type=str, help='Redis host address', default='127.0.0.1')
    parser.add_argument('--redis_port', type=int, help='Redis port number', default=6379)
    parser.add_argument('--redis_db', type=int, help='Redis database number', default=0)
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )

    redis_client = redis.Redis(host=args.redis_host, port=args.redis_port, db=args.redis_db, decode_responses=True)
    
    start = timer()
    logging.info(f'Retriving keys...')
    key_list = [ x for x in redis_client.scan_iter('*', count=10000) ]
    logging.info(f'...{len(key_list)} keys.')
    end = timer()
    logging.info('Elapse {:3.6f}s'.format(end - start))

    start = timer()    
    for k in random.sample(key_list, 10):
        try:
            logging.info(redis_client.get(k)[0:64])
        except Exception as e:
            logging.error(f'{k} not found')
    end = timer()
    logging.info('Elapse {:3.6f}s'.format(end - start))


if __name__ == '__main__':
    main()

