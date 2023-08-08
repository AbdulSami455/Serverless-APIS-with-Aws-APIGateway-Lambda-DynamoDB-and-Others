import boto3
import json
import logging

from custom_encoder import CustomEncoder
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbtablename = 'Product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbtablename)

getmethod = 'GET'
postmethod = 'POST'
patchmethod = 'PATCH'
deletemethod = 'DELETE'
healthpath = '/health'
productpath = '/product'
productspath = '/products'


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getmethod and path == healthpath:
        response = buildResponse(200)
    elif httpMethod == getmethod and path == productpath:
        response = getProduct(event['queryStringParameters']['productid'])
    elif httpMethod == getmethod and path == productspath:
        response = getProducts()
    elif httpMethod == postmethod and path == productpath:
        response = saveProduct(json.loads(event['body']))
    elif httpMethod == patchmethod and path == productpath:
        requestbody = json.loads(event['body'])
        response = modifyProduct(requestbody['productid'], requestbody['updatekey'], requestbody['updatevalue'])
    elif httpMethod == deletemethod and path == productpath:
        requestbody = json.loads(event['body'])
        response = deleteProduct(requestbody['productid'])
    else:
        response = buildResponse(404, 'Not Found')
    return response


def getProduct(productid):
    try:
        response = table.get_item(
            Key={
                'productid': productid
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, 'Product not found')
    except Exception as e:
        logger.error(str(e))
        return buildResponse(500, 'Internal Server Error')


def getProducts():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return buildResponse(200, items)
    except Exception as e:
        logger.error(str(e))
        return buildResponse(500, 'Internal Server Error')


def saveProduct(product):
    try:
        table.put_item(Item=product)
        return buildResponse(201, 'Product saved successfully')
    except Exception as e:
        logger.error(str(e))
        return buildResponse(500, 'Internal Server Error')


def modifyProduct(productid, updatekey, updatevalue):
    try:
        table.update_item(
            Key={'productid': productid},
            UpdateExpression=f"SET {updatekey} = :val",
            ExpressionAttributeValues={':val': updatevalue}
        )
        return buildResponse(200, 'Product updated successfully')
    except Exception as e:
        logger.error(str(e))
        return buildResponse(500, 'Internal Server Error')


def deleteProduct(productid):
    try:
        table.delete_item(Key={'productid': productid})
        return buildResponse(200, 'Product deleted successfully')
    except Exception as e:
        logger.error(str(e))
        return buildResponse(500, 'Internal Server Error')


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response
