import json
from pprint import pprint
from uuid import uuid4 as uuid
from boto3.dynamodb.conditions import Key
from utils import client
from copy import deepcopy



def get_random_question():
    # TODO get a random UUID
    """
    will return:
    {
        "id": "question_id",
        "question": "what is abc?",
        "answers": {"A": 10, "B": 20, "C": 30}
    }

    """
    random_uuid = str(uuid())

    response = client.query(
        KeyConditionExpression=Key('id').eq("1")
    )
    item = response['Items']
    print(item)

def post_question(payload):
    """
    expected payload from frontend
    {
        "id": "question_id",
        "question": "what is abc",
        "answers": ["A", "B", "C"]
    }
    """
    item = deepcopy(payload)
    item["answers"] = {}
    for answer in payload["answers"]:
        item["answers"].update({answer: 0})
    client.put_item(Item=item)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
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
        'GET': get_random_question(),
        # 'POST': lambda dynamo, x: dynamo.put_item(**x)
        'POST': lambda payload: post_question(payload)
    }

    op = event['httpMethod']

    if op in operations:
        # payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        if op == "GET":
            return respond(None, operations[op])
        elif op == "POST":
            return respond(None, operations[op](event['body']))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(op)))


pprint(lambda_handler(
    {
        'httpMethod': 'GET',
        # 'body': {
        # "id": "3",
        # "question": "what is abc",
        # "answers": ["A", "B", "C"]
    # }
    },
    None
))
