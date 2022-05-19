from utils.dynamo import put_dynamo, get_user_base
from utils.secretsmanager import create_secret, get_secret
import json
import uuid


# Function to handle creating user feature
def create_user_handler(user_id, password, **kwargs):
    # Random secret key for user password to store in SSM
    random_value = str(uuid.uuid4().hex)
    # Format the password to store in SSM
    secret_value = json.dumps({random_value: password})
    try:
        # Create secret in SSM for this user
        create_secret(user_id, secret_value)
    except Exception as e:
        # If error, log and raise
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}

    # define data to be insert
    data_insert = {
        "user_id": {"data": user_id, "is_secret": False},
        "password": {"data": random_value, "is_secret": True},
    }

    try:
        # put base data to dynamo
        put_dynamo(user_id, "base", data_insert)
        # Create Empty application_count
        put_dynamo(user_id, "application_count", {})
    except Exception as e:
        # If error, log and raise
        print(repr(e))
        return {
            "success": False,
            "data": repr(e),
        }

    # Return Result
    return {
        "success": True,
        # "data": "201 Created"
        "data": "Create User successfully.",
    }


# Function to handle user login feature
def login_handler(user_id, password, **kwargs):
    # Query user with input user_id
    user = get_user_base(user_id)["resource"]
    print(user)

    # get pass from secret
    secret_user = get_secret(user_id)

    if secret_user[user["password"]["data"]] == password:
        # if password matched, return True
        return {
            "success": True,
            "data": "Login successfully.",
        }
    else:
        # if password minmatched, return False
        return {
            "success": False,
            "data": "Password incorrect.",
        }
