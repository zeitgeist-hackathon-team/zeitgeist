import json
from pprint import pprint
from uuid import uuid4 as uuid
from boto3.dynamodb.conditions import Key
from copy import deepcopy
import decimal
import boto3
import string
from datetime import datetime
from random import random


TABLE_NAME = 'questions'
dynamo = boto3.resource('dynamodb', 'us-west-2')
client = dynamo.Table(TABLE_NAME)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)


def generate_uuids():
    """
    In order to narrow down the filter expression, we set 2 uuids as the start and end.
    The end uuid depends on the start uuid
    For instance, the start uuid is 'axxxxxxx-xxx..', then the end uuid would be 'bxxxxxxx-xxx...'
    If the start uuid starts with 'zzzxxxxx-xxx..', because 'z' is the biggest alphanumeric char, 
    we'll move on the next char and replace it with the next digit/letter 
    UUID is in the format of 8-4-4-4-12 for a total of 36 characters. We only look at the first 8 chars
    If the fist 8 chars are 'zzzzzzzz', then we generate a new start uuid and calculate the end uuid
    """
    uuid_start = str(uuid())
    while uuid_start.startswith("zzzzzzzz"):
        uuid_start = str(uuid())
    uuid_end = list(deepcopy(uuid_start))
    
    char_pool = list(string.digits) + \
        list(string.ascii_uppercase) + \
        list(string.ascii_lowercase) 
    # print(f"char_pool: {char_pool}")
    substitute_char = ''
    i = 0
    while i < 8:
        char_from_start_uuid = uuid_start[i]
        if char_from_start_uuid == "z":
            i += 1
            continue
        else:
            next_index_in_pool = char_pool.index(char_from_start_uuid) + 1
            substitute_char = char_pool[next_index_in_pool]
            break
    uuid_end[i] = substitute_char
    uuid_end = ''.join(uuid_end)
    print(f"generated uuids: {uuid_start}, {uuid_end}")
    return uuid_start, str(uuid_end)


def get_questions():
    random_uuid_start, random_uuid_end = generate_uuids()
    filter_expression = Key("randomId").between(random_uuid_start, random_uuid_end)
    questions = client.scan(FilterExpression = filter_expression)
    questions = questions["Items"]
    return questions
    

def get_random_question():
    """
    will return:
    {
        "id": "question_id",
        "question": "what is abc?",
        "answers": {"A": 10, "B": 20, "C": 30},
        'other': {
            'hackernoon': 1,
            'hackernews': 2
        }
    }
    for v1, we won't implement 'other'. So that would not be in response
    """
    questions = get_questions()
    count = len(questions) 
    while count == 0:
        questions = get_questions()
        count = len(questions) 
    pick = int(random() * count)
    question = questions[pick]
    
    return question


def generate_a_new_primary_id():
    """
    the payload with the newly posted question will only have the question and answers, 
    BE will generate an valid primary key id
    by 'valid', it means no existing question has the same primary key id.
    So we need to do a query first to make sure the newly generated id is valid
    """
    primary_id = str(uuid())
    response = client.query(
        KeyConditionExpression=Key('id').eq(primary_id)
    )
    if response["Items"] == []:
        return primary_id
    else:
        return generate_a_new_primary_id()


def post_question(payload):
    """
    expected payload from frontend
    {
        "question": "what is abc",
        "answers": ["A", "B", "C"]
    }
    """
    new_question = deepcopy(payload)
    new_question["answers"] = {}
    new_question.update(
        {"id": generate_a_new_primary_id(), 
        "postedAt": str(datetime.now()), 
        "randomId": str(uuid())}
        )
    for answer in payload["answers"]:
        new_question["answers"].update({answer: 0})
    
    print(f"the to be posted question is: {new_question}")
    client.put_item(Item=new_question)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res, cls = DecimalEncoder),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in  the payload to the
    DynamoDB API as a JSON body.
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'GET': lambda: get_random_question(),
        # 'POST': lambda dynamo, x: dynamo.put_item(**x)
        'POST': lambda payload: post_question(payload)
    }

    op = event['httpMethod']

    if op in operations:
        # payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        if op == "GET":
            return respond(None, operations[op]())
        elif op == "POST":
            return respond(None, operations[op](event['body']))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(op)))
