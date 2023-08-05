#!/usr/bin/env python3

import argparse
import csv
import logging
import random
from timeit import default_timer as timer

import redis

def main():
    parser = argparse.ArgumentParser(description='Retrive all keys and get it unitl interrupt')
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
    key_list = [ x for x in redis_client.keys() ]
    logging.info(f'...{len(key_list)} keys.')
    end = timer()
    logging.info('Elapse {:3.6f}s'.format(end - start))
    logging.info(type(key_list))

    while True:
        start = timer()    
        k=random.sample(key_list, 1)[0]
        try:
            xml=redis_client.get(k)[0:64]
        except:
            xml='not found'
        end = timer()
        logging.info('Elapse {:3.6f}s xml={}'.format(end - start,xml))


if __name__ == '__main__':
    main()

