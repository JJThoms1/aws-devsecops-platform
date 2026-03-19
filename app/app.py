import json
import os
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'devsecops-items'))

def handler(event, context):
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')

    if path == '/health':
        return response(200, {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

    if path == '/items' and method == 'GET':
        return get_items()

    if path == '/items' and method == 'POST':
        body = json.loads(event.get('body') or '{}')
        return create_item(body)

    if path.startswith('/items/') and method == 'GET':
        item_id = path.split('/')[-1]
        return get_item(item_id)

    if path.startswith('/items/') and method == 'DELETE':
        item_id = path.split('/')[-1]
        return delete_item(item_id)

    return response(404, {'error': 'Not found'})

def get_items():
    result = table.scan()
    return response(200, {'items': result.get('Items', [])})

def create_item(body):
    item = {
        'id': str(uuid.uuid4()),
        'name': body.get('name', ''),
        'description': body.get('description', ''),
        'created_at': datetime.utcnow().isoformat()
    }
    table.put_item(Item=item)
    return response(201, item)

def get_item(item_id):
    result = table.get_item(Key={'id': item_id})
    item = result.get('Item')
    if not item:
        return response(404, {'error': 'Item not found'})
    return response(200, item)

def delete_item(item_id):
    table.delete_item(Key={'id': item_id})
    return response(200, {'message': 'Deleted'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'Strict-Transport-Security': 'max-age=31536000'
        },
        'body': json.dumps(body)
    }
