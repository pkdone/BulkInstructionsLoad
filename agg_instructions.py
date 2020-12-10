#!/usr/bin/env python3
import pymongo
import time
from pprint import pprint

connection = pymongo.MongoClient('mongodb://localhost:27017,localhost:27027,localhost:27037/?replicaSet=TestRS')
db = connection['payments']
coll = db['instructions']

pipeline = [
    {'$group': {
        '_id': None, 
        'instructions_count': {'$sum': 1},
        'payments_balanced': {'$sum': '$amount'},    
    }},    
    {'$unset': '_id'},    
]

while True:
    result = coll.aggregate(pipeline)
    pprint(list(result))
    time.sleep(1)

