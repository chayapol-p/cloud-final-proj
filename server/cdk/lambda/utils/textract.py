import re
import os
import base64

import boto3


# Define neccessary constant and boto3
REGION = os.environ.get("REGION")
textractclient = boto3.client("textract", region_name=REGION)


# Function to Extract card entities from image
def image_to_entities(picture_bytes):

    # Get the text from image by calling Textract API
    textract_response = textractclient.detect_document_text(
        Document={"Bytes": picture_bytes}
    )

    extractedText = {}
    # Check each block whether it match to format of each field type or not
    for block in textract_response["Blocks"]:
        # Check only block that is Line
        if block["BlockType"] == "LINE":
            # Check if this block is card number or not by RegEx
            if re.match("(\d{4}[-\s]?){3}\d{3,4}", block["Text"]):
                extractedText["card_number"] = block["Text"]
            # Check if this block is expriry date or not by RegEx
            elif re.match("^(0[0-9]|1[0-2])\/?([0-9]{2})$", block["Text"]):
                extractedText["expriry_date"] = block["Text"]
    last_text = textract_response["Blocks"][-1]["Text"].lower()

    # Check if this block is provider or not by match string
    if last_text == "mastercard" or last_text == "visa":
        extractedText["provider"] = last_text

    # Return the extract entities
    return extractedText
