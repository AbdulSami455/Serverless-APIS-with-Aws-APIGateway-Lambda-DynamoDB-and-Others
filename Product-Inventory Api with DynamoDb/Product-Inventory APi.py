import boto3
import json
import logging
logger=logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbtablename='Product-inventory'
dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(dynamodbtablename)


getmethod='GET'
postmethod='POST'
patchmethod='PATCH'
deletemethod='DELETE'
healthpath='/health'
productpath='/product'
productspath='/products'


def lambda_handler(event,context):
    logger.info(event)
    httpMethod=event['httpMethod']
    path=event['path']
    if httpMethod==getmethod and path == healthpath:
       response=buildResponse(200)

def buildResponse(statusCode,body=None):
    response={
        'statusCode':statusCode,
        'header':{
            'Content-type':'applications/json',
            'Access-Control-allow-origin':'*'

        }
    }
    if body is not None:
        response['body']=json.dumps(body)
    return response