#!/usr/bin/env python3
import sys
import json
import pymongo
from datetime import datetime

DO_TRANSACTIONS = False
FILENAME = 'PaymentFile_123456789.json'
INSTRUCTIONS_COLL_NAME = 'instructions'
FILES_PROCESSED_COLL_NAME = 'files_processed'

connection = pymongo.MongoClient('mongodb://localhost:27017,localhost:27027,localhost:27037/?replicaSet=TestRS')
db = connection['payments']
instructions_coll = db[INSTRUCTIONS_COLL_NAME]
#instructions_coll.drop()
instructions_coll.create_index([('file_id', pymongo.ASCENDING), ('batch_id', pymongo.ASCENDING), ('instruction_id', pymongo.ASCENDING)], unique=True)
#instructions_coll.create_index([('file_id', pymongo.ASCENDING), ('batch_id', pymongo.ASCENDING)])
instructions_coll.create_index([('batch_id', pymongo.ASCENDING)])
filesprocs_coll = db[FILES_PROCESSED_COLL_NAME]
filesprocs_coll.create_index([('file_id', pymongo.ASCENDING)], unique=True)
count = 0;
file_id = 'unknown'

with open(FILENAME) as json_file:
    data = json.load(json_file)
    file_id = int(data['file_id'])
    #filesprocs_coll.delete_one({'file_id': file_id})
    org_id = int(data['org_id'])
    filedate = datetime.strptime(data['datetime']['$date'],'%Y-%m-%dT%H:%M:%SZ'),

    if filesprocs_coll.find_one({'file_id': file_id}):
        print(f'Skip file: {file_id}')
        sys.exit(0)    
    
    for batch in data['batches']:
        batch_id = batch['batch_id']

        with connection.start_session() as session:
            with session.start_transaction():            
                tx_session = session if DO_TRANSACTIONS else None  
                          
                if instructions_coll.find_one({'file_id': file_id, 'batch_id': batch_id}):
                    print(f'Skip file batch: {file_id} - {batch_id}')
                    continue                                  
                
                for instruction in batch['instructions']:
                    instructions_coll.insert_one({
                            'file_id': file_id,
                            'file_org_id': org_id,
                            'file_date': filedate[0],
                            'batch_id': batch_id,
                            'instruction_id': instruction['instruction_id'],
                            'amount': instruction['amount'],
                            'payer': instruction['payer'],
                            'payee': instruction['payee'],
                    }, session=tx_session)
                    count += 1

    filesprocs_coll.insert_one({'file_id': file_id})
    
    print(f'{count} records for file id "{file_id}" have been inserted - using transsctions: {DO_TRANSACTIONS}')
print()
