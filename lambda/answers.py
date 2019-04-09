import boto3
import json

DYNAMO = boto3.client('dynamodb', 'us-west-2')

def post_answer(payload):
    print("posted beeeitch!!", payload)


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
        'POST': post_answer,
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
            'question_id': 1,
            'answer': 'Python'
        }
    },
    None
))