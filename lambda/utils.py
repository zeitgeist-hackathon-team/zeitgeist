import boto3

dynamo = boto3.resource('dynamodb', 'us-west-2')
TABLE_NAME = 'questions'

client = dynamo.Table(TABLE_NAME)



