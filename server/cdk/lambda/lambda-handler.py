import json
import os
import uuid
import boto3
import base64
import re


def main(event, context):

    dump = json.dumps(event)
    userInput = json.loads(dump)["queryStringParameters"]
    method = userInput['method']

    random_value = str(uuid.uuid4().hex)
    TABLE_NAME = os.environ.get('TABLE_NAME')
    REGION = os.environ.get('REGION')
    print(f'Random value is {random_value}')

    textractclient = boto3.client("textract", region_name=REGION)
    dynamo_client = boto3.client("dynamodb", region_name=REGION)
    table = boto3.resource('dynamodb').Table(TABLE_NAME)
    secrets = boto3.client('secretsmanager')

    def textract(picture_bytes):
        textract_response = textractclient.detect_document_text(
            Document={
                'Bytes': picture_bytes
            }
        )

        extractedText = ["card number", "GOOD THRU", "date", "provider"]
        for block in textract_response['Blocks']:
            if block["BlockType"] == "LINE":
                if re.match("(\d{4}[-\s]?){3}\d{3,4}", block["Text"]):
                    extractedText[0] = block["Text"]
                elif re.match("^(0[1-9]|1[0-2])\/?([0-9]{2})$", block["Text"]):
                    extractedText[2] = block["Text"]
        extractedText[-1] = textract_response['Blocks'][-1]["Text"]

        return extractedText

    def put_dynamo(user_id, resource_key, data):
        return table.put_item(
            Item={
                "user_id": user_id,
                "resource_key": resource_key,
                "data": data,
            }
        )

    def get_data(user_id, resource_key):
        data = table.get_item(
            Key={
                "user_id": user_id,
                "resource_key": resource_key
            },
            AttributesToGet=[
                'data',
            ],)['Item']['data']

        for key in data:
            if data[key]['is_secret']:
                secret_res = json.loads(secrets.get_secret_value(
                    SecretId=user_id)['SecretString'])
                data[key]['data'] = secret_res[data[key]['data']]

        return data

    # # data = dynamo_client.get_item(TableName=TABLE_NAME, Key={"username": {"S": username}})
    # data = dynamo_client.get_item(TableName=TABLE_NAME,)

    response = {
        "success": False,
        "data": 404
    }

    if method == 'newuser':

        # data_insert = {'username': {'data': userInput['username'], 'is_secret': False}, 'password': {'data': userInput['password'], 'is_secret': False}}

        try:
            secret_res = secrets.create_secret(
                Name=userInput['username'],
                SecretString=('{"%(id)s" : "%(password)s"}' % {
                              "id": random_value, "password": userInput['password']})
            )
            print(secret_res)
            data_insert = {'password': {
                "data": random_value, 'is_secret': True}}
            db_res = put_dynamo(userInput['username'], 'base', data_insert)
            print(db_res)

        except Exception as e:
            print(repr(e))

        response = {
            "success": True,
            "data": "201 Created"
        }
        # data = dynamo_client.scan(TableName=TABLE_NAME, FilterExpression=Attr("resource_key").eq("base") & Attr("data").contains("username"))

    if method == 'login':
        data = get_data(userInput['username'], "base")
        password = data['password']['data']

        if userInput['password'] == password:
            response = {
                "success": True,
                "data": "200 Authorized"
            }
        else:
            response = {
                "success": False,
                "data": "403 Forbidden"
            }

    if method == 'textract':
        pic_64 = json.loads(dump)['body']
        pic_bytes = base64.b64decode(pic_64)
        text = textract(pic_bytes)

        response = {
            "success": True,
            "data": text
        }

    # print("Succeeded: 2022")
    print(json.dumps(response, indent=2))

    return json.dumps(response, indent=2)
