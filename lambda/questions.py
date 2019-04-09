
import boto3
import json
from pprint import pprint

DYNAMO = boto3.client('dynamodb', 'us-west-2')
TABLE_NAME = 'questions'


def get_random_question():

    # return DYNAMO.scan(TableName = TABLE_NAME)

    return {
        'id': 'random-uuid-id',
        'question': 'what\'s your most frequently visted website below?',
        'answers': {
            'reddit': 3,
            'medium': 234,
            'techcrunch': 13
        },
        'other': {
            'hackernoon': 1,
            'hackernews': 2
        }
    } # todo echo

def post_question(body):
    pass


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
        'GET': get_random_question,
        # 'POST': lambda dynamo, x: dynamo.put_item(**x)
        'POST': lambda body: post_question(body)
    }

    op = event['httpMethod']

    if op in operations:
        # payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[op]())
    else:
        return respond(ValueError('Unsupported method "{}"'.format(op)))


# pprint(lambda_handler(
#     {
#         'httpMethod': 'GET'
#     },
#     None
# ))
