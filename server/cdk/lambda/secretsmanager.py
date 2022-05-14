import os
import base64
import json

import boto3
from botocore.exceptions import ClientError


REGION = os.environ.get("REGION")
secretsmanager_client = boto3.client("secretsmanager", region_name=REGION)


def create_secret(name, secret_value):
    try:

        response = secretsmanager_client.create_secret(
            Name=name, SecretString=secret_value
        )
        print("Created secret %s.", name)
    except ClientError:
        print("Couldn't create secret %s.", name)
        raise
    else:
        return response


def put_secret(name, secret_value):
    try:

        response = secretsmanager_client.put_secret_value(
            SecretId=name, SecretString=secret_value
        )
        print("Value put in secret %s.", name)
    except ClientError:
        print("Couldn't put to secret %s.", name)
        raise
    else:
        return response


def test_create_secret_handler(name, secret_value):
    try:
        create_secret(name, secret_value)
        return {"success": True, "data": "Created"}
    except Exception as e:
        print("Create Error:", repr(e))
        return {"success": True, "data": repr(e)}
