import base64
from pydoc import resolve
import resource
import uuid
import json

from utils.secretsmanager import put_secret, create_secret, get_secret_value
from utils.textract import image_to_entities
from utils.dynamo import put_dynamo, get_user_app_count, get_user_resource_begins_with, get_user_resource


def test_create_secret_handler(name, secret_value, **kwargs):
    try:
        create_secret(name, secret_value)
        return {"success": True, "data": "Created"}
    except Exception as e:
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}


def put_card_handler(user_id, resource, picture, cvv, **kwargs):
    pic_bytes = base64.b64decode(picture.encode("utf-8"))
    text_entities = image_to_entities(pic_bytes)
    print("Text entities:", text_entities)

    try:
        random_value = str(uuid.uuid4().hex)
        secret_value = {random_value: cvv}
        put_secret(user_id, secret_value)
    except Exception as e:
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}

    data_insert = {
        "provider": {"data": text_entities["provider"], "is_secret": False},
        "card_number": {"data": text_entities["card_number"], "is_secret": False},
        "expriry_date": {"data": text_entities["expriry_date"], "is_secret": False},
        "cvv": {"data": random_value, "is_secret": True},
    }

    data_adder(user_id, resource, data_insert)
    return {"success": True, "data": text_entities}


def data_adder(user_id, resource, data_insert):
    try:
        app_count = get_user_app_count(user_id)["resource"]
        if resource in app_count:
            app_count[resource] += 1
        else:
            app_count[resource] = 1
        resource_key = f"{resource}_{app_count[resource] - 1}"
        put_dynamo(user_id, "application_count", app_count)
    except Exception as e:
        print(repr(e))
        return {
            "success": False,
            "data": "App Count Error",
        }

    try:
        put_dynamo(user_id, resource_key, data_insert)

    except Exception as e:
        print(repr(e))
        return {
            "success": False,
            "data": repr(e),
        }

    return {
        "success": True,
        "data": "Create Data successfully.",
    }


def put_app_handler(user_id, app, username, password, **kwargs):
    try:
        random_value = str(uuid.uuid4().hex)
        secret_value = {random_value: password}
        put_secret(user_id, secret_value)
    except Exception as e:
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}

    data_insert = {
        "username": {"data": username, "is_secret": False},
        "password": {"data": random_value, "is_secret": True},
    }

    return data_adder(user_id, app, data_insert)


def list_resource_handler(user_id, resource, **kwargs):
    resources = get_user_resource_begins_with(user_id, resource)["resources"]

    resources_view = []

    for resource_i in resources:
        data = resource_i["data"]
        show_value = data["card_number"]['data'] if "card_number" in data else data["username"]['data']
        resources_view.append((resource_i["resource_key"], show_value))

    return {"success": True, "data": resources_view}


def get_resource_handler(user_id, resource_key, **kwargs):
    data = get_user_resource(user_id, resource_key)["resource"]
    resolved_data = {}
    
    for field_name in data:
        field = data[field_name]
        if field['is_secret']:
            secret_key = field["data"]
            secret_data = get_secret_value(user_id, secret_key)
            resolved_data[field_name] = secret_data
        else:
            resolved_data[field_name] = field['data']

    return {
        'success': True,
        'data': resolved_data
    }