import boto3
import json
from utils import client
from boto3.dynamodb.conditions import Key

def post_answer(payload):
    # Expect the payload to be in this format:
    """
    expected payload from the request
    {
        "id": "quesiton_id",
        "answers": ["A", "B"]
        }
    """
    print("payload: \n", payload)
    question_id = payload.get("id")
    response = client.query(
        KeyConditionExpression=Key('id').eq(question_id)
    )
    item = response['Items'][0]
    print(type(item))
    print("item: \n", item)
    for answer in payload["answers"]:
        votes = item["answers"].get(answer)
        item["answers"].update({answer: votes + 1})

    print("updated item: \n", item)
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
        'POST': lambda payload: post_answer(payload),
        # todo 'POST': lambda dynamo, x: dynamo.put_item(**x)
    }

    op = event['httpMethod']

    if op in operations:
        return respond(None, operations[op](event['body']))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(op)))


print(lambda_handler(
    {
        'httpMethod': 'POST',
        'body': {
            'id': "1",
            'answers': ['Python']
        }
    },
    None
))