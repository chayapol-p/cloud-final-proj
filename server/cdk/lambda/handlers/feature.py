import base64

from utils.secretsmanager import create_secret
from utils.textract import image_to_entities

def test_create_secret_handler(name, secret_value):
    try:
        create_secret(name, secret_value)
        return {"success": True, "data": "Created"}
    except Exception as e:
        print("Create Error:", repr(e))
        return {"success": True, "data": repr(e)}


def textract_card_handler(picture, **kwargs):
    pic_bytes = base64.b64decode(picture.encode('utf-8'))
    text_entities = image_to_entities(pic_bytes)
    print("Text entities:", text_entities)
    
    # TODO: put data to dynamo and SM
    return {"success": True,
            "data": text_entities}