import base64
import uuid

from utils.secretsmanager import put_secret, get_secret_value
from utils.textract import image_to_entities
from utils.dynamo import (
    put_dynamo,
    get_user_app_count,
    get_user_resource_begins_with,
    get_user_resource,
)


# Function to handle when adding new data
def data_adder(user_id, resource, data_insert):
    try:
        # get current applicaton_count
        app_count = get_user_app_count(user_id)["resource"]
        if resource in app_count:
            # if already have this app, + 1
            app_count[resource] += 1
        else:
            # if this is the first, set to one
            app_count[resource] = 1

        # declare resource_key corresponding to amount of this app as prefix
        resource_key = f"{resource}_{app_count[resource] - 1}"
        # update new applicaton_count in dynamo
        put_dynamo(user_id, "application_count", app_count)
    except Exception as e:
        # If error, log and raise
        print(repr(e))
        return {
            "success": False,
            "data": "App Count Error",
        }

    try:
        # put data wanted to insert to dynamo
        put_dynamo(user_id, resource_key, data_insert)

    except Exception as e:
        # If error, log and raise
        print(repr(e))
        return {
            "success": False,
            "data": repr(e),
        }

    # return result
    return {
        "success": True,
        "data": "Create Data successfully.",
    }


# Function to handle adding new card feature
def put_card_handler(user_id, resource, picture, cvv, **kwargs):

    # transform card image to bytes and extract by textract
    pic_bytes = base64.b64decode(picture.encode("utf-8"))
    text_entities = image_to_entities(pic_bytes)
    print("Text entities:", text_entities)

    try:
        # Random secret key for cvv to store in SSM
        random_value = str(uuid.uuid4().hex)
        # Format the cvv to store and put to SSM
        secret_value = {random_value: cvv}
        put_secret(user_id, secret_value)

    except Exception as e:
        # If error, log and raise
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}

    # Declare data taht want to insert to dynamo
    data_insert = {
        "provider": {"data": text_entities["provider"], "is_secret": False},
        "card_number": {"data": text_entities["card_number"], "is_secret": False},
        "expriry_date": {"data": text_entities["expriry_date"], "is_secret": False},
        "cvv": {"data": random_value, "is_secret": True},
    }

    # Add the data by data_adder function the return the result
    return data_adder(user_id, resource, data_insert)


# Function to handle creating user feature
def put_app_handler(user_id, app, username, password, **kwargs):
    try:
        # Random secret key for password to store in SSM
        random_value = str(uuid.uuid4().hex)
        # Format the password to store and put to SSM
        secret_value = {random_value: password}
        put_secret(user_id, secret_value)

    except Exception as e:
        # If error, log and raise
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}

    # Declare data taht want to insert to dynamo
    data_insert = {
        "username": {"data": username, "is_secret": False},
        "password": {"data": random_value, "is_secret": True},
    }

    # Add the data by data_adder function the return the result
    return data_adder(user_id, app, data_insert)


# Function to handle list user's resource feature
def list_resource_handler(user_id, resource, **kwargs):
    # Get all this resource with this resource name
    resources = get_user_resource_begins_with(user_id, resource)["resources"]

    # Create The list of indentifier for each resource to show to user for selection
    resources_view = []
    for resource_i in resources:
        data = resource_i["data"]
        show_value = (
            data["card_number"]["data"]
            if "card_number" in data
            else data["username"]["data"]
        )
        resources_view.append((resource_i["resource_key"], show_value))

    # Return result
    return {"success": True, "data": resources_view}


# Function to handle geting user resource data feature
def get_resource_handler(user_id, resource_key, **kwargs):
    # Get the exact resource of this user
    data = get_user_resource(user_id, resource_key)["resource"]

    # Convert the data which are secret of this resource to be normal text
    resolved_data = {}
    for field_name in data:
        field = data[field_name]
        if field["is_secret"]:
            secret_key = field["data"]
            secret_data = get_secret_value(user_id, secret_key)
            resolved_data[field_name] = secret_data
        else:
            resolved_data[field_name] = field["data"]

    # Return the result
    return {"success": True, "data": resolved_data}
