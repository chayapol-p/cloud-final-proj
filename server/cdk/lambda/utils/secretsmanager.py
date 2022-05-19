import os
import base64
import json

import boto3
from botocore.exceptions import ClientError


# Define neccessary constant and boto3
REGION = os.environ.get("REGION")
secretsmanager_client = boto3.client("secretsmanager", region_name=REGION)


# Function to create new secret
def create_secret(name, secret_value):
    try:
        # Create new secret
        response = secretsmanager_client.create_secret(
            Name=name, SecretString=secret_value
        )
        print("Created secret %s.", name)
    except ClientError:
        # If Error, raise
        print("Couldn't create secret %s.", name)
        raise
    else:
        return response


# Function to update th secret
def put_secret(name, secret_value):
    # Check if this secret is existed
    secret_dict = get_secret(name)
    print(secret_value)
    # Update new secret_value with input secret_value
    secret_dict.update(secret_value)
    print("secret_dict:", secret_dict)
    # Dump into JSON string
    secret_value = json.dumps(secret_dict)
    try:
        # Put new secret_value to SSM
        response = secretsmanager_client.put_secret_value(
            SecretId=name, SecretString=secret_value
        )
        print("Value put in secret %s.", name)
    except ClientError:
        # If Error, raise
        print("Couldn't put to secret %s.", name)
        raise
    else:
        return response


# Function to get the secret
def get_secret(name):
    try:
        # Get whole secret value from SSM by the input name
        response = secretsmanager_client.get_secret_value(SecretId=name)
    except ClientError:
        # If Error, raise
        print("This secret is not exist.")
        raise
    else:
        return json.loads(response["SecretString"])


# Function to get only one value from the secret
def get_secret_value(name, key_name):
    try:
        # Get whole secret value from SSM by the input name
        response = secretsmanager_client.get_secret_value(SecretId=name)
    except ClientError:
        # If Error, raise
        print("This secret is not exist.")
        raise
    else:
        # Return only one key from input key_name
        return json.loads(response["SecretString"])[key_name]
