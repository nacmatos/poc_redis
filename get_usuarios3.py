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
        level=logging.INFO
    )

    redis_client = redis.Redis(host=args.redis_host, port=args.redis_port, db=args.redis_db, decode_responses=True)
    
    start = timer()
    logging.info(f'Retriving keys...')
    key_list = [ x for x in redis_client.scan_iter('*', count=10000) ]
    logging.info(f'...{len(key_list)} keys.')
    end = timer()
    logging.info('Elapse {:2.6f}s'.format(end - start))

    (n, nf, avg, min, max, hist) = (0, 0, 0, 99999999999, 0, {})

    while True:
      try:
          n+=1
          k=random.sample(key_list, 1)[0]
          start = timer()    
          try:
            xml=redis_client.get(k)[0:64]
          except KeyboardInterrupt:
            print('\nCTRL-C! Exiting...')
            break
          except:
            xml='not found'
            nf+=1
            logging.info(f'{k} XML not found')
          end = timer()
          elap = (end - start)*1000000
          avg += elap
          min = elap if elap < min else min;
          max = elap if elap > max else max
          hist[int(elap/50)] = hist.get(int(elap/50),0) + 1
          if elap > 250: logging.debug(f'key={k} elap={elap}us')
          if (n%10000)==0:
            logging.info(f'Min/Avg/Max us |  {min:3.1f} / {avg/n:3.1f} / {max:3.1f}')
            (n, avg, min, max) = (0, 0, 99999999999, 0)
      except KeyboardInterrupt:
        break

    logging.info(f'Not found keys: {nf}')
    logging.info('Histogram')
    for k in sorted(hist): logging.info(f'{(k+1)*50:4} | {hist[k]}')


if __name__ == '__main__':
    main()

