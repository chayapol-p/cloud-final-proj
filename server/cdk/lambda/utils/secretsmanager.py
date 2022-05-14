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
    secret_dict = get_secret(name)
    print(secret_value)
    secret_dict.update(secret_value)
    print('secret_dict:',secret_dict)
    secret_value = json.dumps(secret_dict)
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

def get_secret(name):
    try:
        response =secretsmanager_client.get_secret_value(SecretId=name)
    except ClientError:
        print("This secret is not exist.")
        raise
    else:
        return json.loads(response['SecretString'])


def get_secret_value(name, key_name):
    try:
        response =secretsmanager_client.get_secret_value(SecretId=name)
    except ClientError:
        print("This secret is not exist.")
        raise
    else:
        return json.loads(response['SecretString'])[key_name]
