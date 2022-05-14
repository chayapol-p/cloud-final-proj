import os

import boto3


TABLE_NAME = os.environ.get('TABLE_NAME')
REGION = os.environ.get('REGION')
dynamo_client = boto3.client("dynamodb", region_name=REGION)


def put_dynamo(dynamo_client, user_id, resource_key, data):
    return dynamo_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "user_id": {"S": user_id},
            "resource_key": {"S": resource_key},
            "data": {"M": data},
        },
    )


def create_user_handler(username, password, **kwargs):
    data_insert = {
        "username": {"data": username, "is_secret": False},
        "password": {"data": password, "is_secret": False},
    }
    # put_dynamo(random_value,'base','username',userInput['username'])
    # put_dynamo(random_value,'base','password',userInput['password'])
    try:
        put_dynamo(username, "base", data_insert)
    except Exception as e:
        print(repr(e))
        return {
            "success": False,
            # "data": "201 Created"
            "data": repr(e),
        }
    # data = dynamo_client.scan(TableName=TABLE_NAME, FilterExpression=Attr("resource_key").eq("base") & Attr("data").contains("username"))

    return {
        "success": True,
        # "data": "201 Created"
        "data": "",
    }


def login_handler():
    print("Test Pass")
