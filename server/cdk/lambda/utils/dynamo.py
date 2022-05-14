import os

import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.conditions import Key, Attr

deserializer = TypeDeserializer()


TABLE_NAME = os.environ.get("TABLE_NAME")
REGION = os.environ.get("REGION")
dynamo_client = boto3.client("dynamodb", region_name=REGION)
dynamo = boto3.resource("dynamodb", region_name=REGION)
table = dynamo.Table(TABLE_NAME)


def deserialize_data(data):
    return {k: deserializer.deserialize(v) for k, v in data.items()}


def put_dynamo(user_id, resource_key, data):
    return table.put_item(
        Item={
            "user_id": user_id,
            "resource_key": resource_key,
            "data": data,
        },
    )


def get_user_resource(user_id, resource_key):
    data = table.get_item(Key={"user_id": user_id, "resource_key": resource_key})

    if "Item" not in data:
        # This user_id is not exist, raise the error
        raise ValueError("This user_id is not exist.")
    else:
        # Else return user data
        item = data["Item"]

        return {"success": True, "resource": item["data"]}


def get_user_base(user_id):
    return get_user_resource(user_id, "base")


def get_user_app_count(user_id):
    return get_user_resource(user_id, "application_count")


def get_user_resource_begins_with(user_id, resource):
    data = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id) & Key("resource_key").begins_with(resource)
    )

    if "Items" not in data:
        # This user_id is not exist, raise the error
        raise ValueError("No resource was found for this user.")
    else:
        # Else return user data
        items = data["Items"]
        print("List resource:", data)
        return {"success": True, "resources": items}
