import json
import os
import uuid
import boto3


def main(event, context):

    dump = json.dumps(event)
    userInput = json.loads(dump)["queryStringParameters"]

    random_value = str(uuid.uuid4().hex)
    TABLE_NAME = os.environ.get('TABLE_NAME')
    REGION = os.environ.get('REGION')
    print(f'Random value is {random_value}')

    textractclient = boto3.client("textract", region_name=REGION)
    dynamo_client = boto3.client("dynamodb", region_name=REGION)

    # textract
    textract_response = textractclient.detect_document_text(
        Document={
            'Bytes': userInput['card']
        }
    )

    extractedText = ""
    for block in textract_response['Blocks']:
        if block["BlockType"] == "LINE":
            extractedText = extractedText+block["Text"]+" "
    ####

    # data = dynamo_client.get_item(TableName=TABLE_NAME, Key={"username": {"S": username}})
    data = dynamo_client.get_item(TableName=TABLE_NAME,)
    response = {
        "success": True,
        "data": data
    }

    print("Succeeded:")
    print(json.dumps(response, indent=2))

    return json.dumps(response, indent=2)
