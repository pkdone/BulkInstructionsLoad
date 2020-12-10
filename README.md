# Demonstrates ingestion a file of batches of dummy payments into MongoDB where each batch of instructions is ingested as a transaction

1. Ensure you have Python 3 and MongoDB's PyMongo Driver installed and a MongoDB server is running on `localhost:27017`

2. Generate the sample JSON file of batches of payments

```console
./create_payment_data.py
```

3. Start a Python script which continuously shows the balance across all ingested payments + how many instructions have been ingested - ensure this is kept running

```console
./agg_instructions.py
```

4. In a separate terminal, start a Python script which loads the instructions file and for each batch of instructions inserts a document per instruction into the DB - this won't use a transaction per batch when first run because a variable in the file is set to false: `DO_TRANSACTIONS = False`

```console
./insert_payment_file.py
```

5. Look at the output of the `agg_instructions.py` script to see if it is NOT ingesting batches transactionally (some balances shown don't add up to zero and the amount of instructions ingested is not a round 5000 each time).

6. Using the Mongo Shell or Compass, delete the collections `payments.instructions` and `payments.files_processed`

7. Edit the file `insert_payment_file.py` and change the value of the variable to: `DO_TRANSACTIONS = True`

8. Start the Python script again which loads the instructions file and for each batch of instructions inserts a document per instruction into the DB - this time it will use a transaction per batch of instructions

```console
./insert_payment_file.py
```
9. Look at the output of the `agg_instructions.py` script to see if it IS ingesting batches transactionally (balances shown should always be zero and the amount of instructions ingested should always be a round 5000 each time.

10. From the Mongo Shell try some of the queries from the text file `queries.txt' including the final one which only shows a batch of instructions if the whole file has been ingested

