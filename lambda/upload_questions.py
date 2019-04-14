import csv
import json
import boto3
from uuid import uuid4 as uuid
from datetime import datetime
from collections import OrderedDict

TABLE_NAME = 'questions'
dynamo = boto3.resource('dynamodb', 'us-west-2')
client = dynamo.Table(TABLE_NAME)

FILEPATH = "/Users/echowu/Downloads/Surveys.csv"
with open(FILEPATH, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        question = row["Question"]
        answers = json.loads(row["Answers"])
        answers = OrderedDict({k: 0 for k in answers})
        print(answers)
        question_id = str(uuid())
        randome_id = str(uuid())
        postedAt = str(datetime.now())
        payload = {"question": question, "answers": answers,
                   "id": question_id, "randomId": randome_id, "postedAt": postedAt}
        client.put_item(Item=payload)
        line_count += 1
    print(f'Processed {line_count} lines.')
