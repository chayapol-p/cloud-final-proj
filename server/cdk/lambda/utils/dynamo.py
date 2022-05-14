import os

import boto3


TABLE_NAME = os.environ.get('TABLE_NAME')
REGION = os.environ.get('REGION')
dynamo_client = boto3.client("dynamodb", region_name=REGION)


def put_dynamo(user_id, resource_key, data):
    return dynamo_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "user_id": {"S": user_id},
            "resource_key": {"S": resource_key},
            "data": {"M": data},
        },
    )
