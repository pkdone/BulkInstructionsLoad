#!/usr/bin/env python3
import os
import random
import time
from datetime import datetime

FILE_ID = '123456789'
ACCOUNTS = ['OrgA', 'OrgB', 'OrgC', 'BigComp', 'SuperEnterprise', 'AcmeCorp', 'BigCorp', 'XxCompany', 'BigBusiness', 'MediaBizz']
BATCH_AMOUNT = 100
INSTRUCTION_AMOUNTS = 5000
PAYMENT_AMOUNTS = [-999, 999]


file_path = f'./PaymentFile_{FILE_ID}.json'
os.remove(file_path) if os.path.exists(file_path) else None

with open(file_path, 'a') as jsonfile:
    jsonfile.write('{\n')
    jsonfile.write(f'  "file_id": {FILE_ID},\n')
    jsonfile.write(f'  "org_id": "{str(random.randint(10000000000, 99999999999))}",\n')
    jsonfile.write('  "datetime": {"$date": "2020-11-27T13:17:54Z"},\n')
    jsonfile.write('  "batches": [\n')
    is_first_batch = True

    for batch_count in range(BATCH_AMOUNT): 
        if not is_first_batch:
            jsonfile.write('    ,\n')

        jsonfile.write('    {\n')
        jsonfile.write(f'      "batch_id": {batch_count},\n')
        jsonfile.write(f'      "instructions": [\n')

        payment_index = 0
        instruction_list = []
        is_first_instruction = True

        for instruction_count in range(INSTRUCTION_AMOUNTS): 
            if not is_first_instruction:
                jsonfile.write('        ,\n')
                
            jsonfile.write('        {\n')
            jsonfile.write(f'          "instruction_id": {instruction_count},\n')
            jsonfile.write(f'          "amount": {PAYMENT_AMOUNTS[payment_index]},\n')
            jsonfile.write(f'          "payer": "{random.choice(ACCOUNTS)}",\n')
            jsonfile.write(f'          "payee": "{random.choice(ACCOUNTS)}",\n')
            jsonfile.write(f'          "payer_acc_num": {random.randint(0,9999999900)},\n')
            jsonfile.write(f'          "payer_sort_code": {random.randint(0,999999)},\n')
            jsonfile.write(f'          "payee_acc_num": {random.randint(0,9999999900)},\n')
            jsonfile.write(f'          "payee_sort_code": {random.randint(0,999999)},\n')
            jsonfile.write(f'          "narrative": "The xyz did abc and then thought about pqrs, and so on..."\n')
            payment_index = (payment_index + 1) % 2
            jsonfile.write('        }\n')
            is_first_instruction = False
        
        jsonfile.write('      ]\n')
        jsonfile.write('    }\n')
        is_first_batch = False

    jsonfile.write('  ]\n}\n')
    

print(f"1 file of {BATCH_AMOUNT} batches each containing {INSTRUCTION_AMOUNTS} instructions has been created at: {file_path}")
print()
#mongoexport -d payments -c dump -o PaymentFile1.json
