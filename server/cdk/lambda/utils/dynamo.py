import os

import boto3
from boto3.dynamodb.conditions import Key


# Define neccessary constant and boto3
TABLE_NAME = os.environ.get("TABLE_NAME")
REGION = os.environ.get("REGION")
dynamo_client = boto3.client("dynamodb", region_name=REGION)
dynamo = boto3.resource("dynamodb", region_name=REGION)
table = dynamo.Table(TABLE_NAME)


# Function to put datas to dynamo
def put_dynamo(user_id, resource_key, data):
    # Put Data to dynamo
    return table.put_item(
        Item={
            "user_id": user_id,
            "resource_key": resource_key,
            "data": data,
        },
    )


# Functon to get resource from user
def get_user_resource(user_id, resource_key):
    # get data from dynamo
    data = table.get_item(Key={"user_id": user_id, "resource_key": resource_key})

    if "Item" not in data:
        # This user_id is not exist, raise the error
        raise ValueError("This user_id is not exist.")
    else:
        # Else return user data
        item = data["Item"]

        return {"success": True, "resource": item["data"]}


# Functon to get base resource for login
def get_user_base(user_id):
    return get_user_resource(user_id, "base")


# Functon to get application_count for app prefix in resource_key
def get_user_app_count(user_id):
    return get_user_resource(user_id, "application_count")


# Functon to query the resource by its name
def get_user_resource_begins_with(user_id, resource):
    # Query data from dynamo where user_id is the one who request and resource_key name is exact with input resource name
    data = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
        & Key("resource_key").begins_with(resource + "_")
    )

    if "Items" not in data:
        # This Item is not exist, raise the error
        raise ValueError("No resource was found for this user.")
    else:
        # Else return user data
        items = data["Items"]
        print("List resource:", data)
        return {"success": True, "resources": items}
