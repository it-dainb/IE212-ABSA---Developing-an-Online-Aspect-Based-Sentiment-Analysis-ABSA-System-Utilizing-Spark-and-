from kafka import KafkaProducer
from time import sleep
from random import seed
from random import randint
import json
from confluent_kafka import Producer
import os

topic_name = 'ryhjlimi-shopee'
kafka_server = 'dory-01.srvs.cloudkafka.com:9094,dory-02.srvs.cloudkafka.com:9094,dory-03.srvs.cloudkafka.com:9094'
cert_folder = 'cert/'

conf = {
        'bootstrap.servers': kafka_server.split(",")[0],
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': 'ryhjlimi',
        'sasl.password': 'LuUoqLhDxrLrFDGjJPDxoaW1i4lnKaOl'
    }

p = Producer(**conf)

import sys

def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d]\n' %
                            (msg.topic(), msg.partition()))

import pandas as pd

df = pd.read_csv('data/electric.csv', encoding = 'utf-8')
df = df.sample(frac=1).reset_index(drop=True)

for index, row in df.iterrows():
    try:
        data = {
            'cmtid' : str(row['cmtid']),
            'comment' : row['comment'],
            'rating_star' : row['rating_star']
        }
        
        p.produce(topic_name, json.dumps(data, ensure_ascii = False).encode('utf-8'), callback=delivery_callback)
        
        print("SENT CMT_ID  :", data['cmtid'])
        print()
        print("STAR         :", data['rating_star'])
        print("CMT          :", data['comment'])
        print()
        print("-" * 10)
        print()
        
        sleep(5)
    except KeyboardInterrupt:
        p.flush()


p.flush()