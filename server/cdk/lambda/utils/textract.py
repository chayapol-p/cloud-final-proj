import re
import os
import base64

import boto3


REGION = os.environ.get('REGION')
textractclient = boto3.client("textract", region_name=REGION)


def image_to_entities(picture_bytes):
    
    textract_response = textractclient.detect_document_text(
        Document={
            'Bytes': picture_bytes
        }
    )
    

    extractedText = {}
    for block in textract_response['Blocks']:
        if block["BlockType"] == "LINE":
            if re.match("(\d{4}[-\s]?){3}\d{3,4}", block["Text"]):
                extractedText["card number"] = block["Text"]
            elif re.match("^(0[1-9]|1[0-2])\/?([0-9]{2})$", block["Text"]):
                extractedText["expriry date"] = block["Text"]
    last_text = textract_response['Blocks'][-1]["Text"].lower()
    if last_text == "mastercard" or last_text == "visa":
        extractedText["provider"] = last_text

    return extractedText
