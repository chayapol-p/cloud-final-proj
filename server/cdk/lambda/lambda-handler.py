import json
import os
import uuid
import boto3
import base64


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

    def textract(picture_bytes):
        textract_response = textractclient.detect_document_text(
            Document={
                'Bytes': picture_bytes
            }
        )

        extractedText = ""
        for block in textract_response['Blocks']:
            if block["BlockType"] == "LINE":
                extractedText = extractedText+block["Text"]+" "
        return extractedText

    def put_dynamo(user_id, resource_key, field, data, is_secret=False):
        dynamo_client.put_item(
            TableName=TABLE_NAME,
            Item={
                "user_id": {"S": user_id},
                "resource_key": {"S": resource_key},
                'field': {"S": field},
                'data': {"S": data},
                'is_secret': {"BOOL": is_secret},
            }
        )

    # # data = dynamo_client.get_item(TableName=TABLE_NAME, Key={"username": {"S": username}})
    # data = dynamo_client.get_item(TableName=TABLE_NAME,)

    response = {
        "success": False,
        "data": 404
    }

    if method == 'newuser':
        put_dynamo(random_value, 'base', 'username', userInput['username'])
        put_dynamo(random_value, 'base', 'password', userInput['password'])

        response = {
            "success": True,
            "data": "201 Created"
        }

    if method == 'login':
        # db_password = dynamo_client.get_item(TableName=TABLE_NAME, Key={"user"})
        print("test")

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
