from utils.dynamo import put_dynamo, get_user_base
from utils.secretsmanager import create_secret, get_secret
import json
import uuid


def create_user_handler(user_id, password, **kwargs):
    random_value = str(uuid.uuid4().hex)
    secret_value = json.dumps({random_value:password})
    try:
        create_secret(user_id,secret_value)
    except Exception as e:
        print("Create Error:", repr(e))
        return {"success": False, "data": repr(e)}

    data_insert = {
        "user_id": {"data": user_id, "is_secret": False},
        # TODO: put password to secret
        "password": {"data": random_value, "is_secret": True},
    }
    # put_dynamo(random_value,'base','user_id',userInput['user_id'])
    # put_dynamo(random_value,'base','password',userInput['password'])
    try:
        put_dynamo(user_id, "base", data_insert)
        put_dynamo(user_id, "application_count", {})
    except Exception as e:
        print(repr(e))
        return {
            "success": False,
            # "data": "201 Created"
            "data": repr(e),
        }
    # data = dynamo_client.scan(TableName=TABLE_NAME, FilterExpression=Attr("resource_key").eq("base") & Attr("data").contains("user_id"))

    return {
        "success": True,
        # "data": "201 Created"
        "data": "Create User successfully.",
    }


def login_handler(user_id, password, **kwargs):
    # Query user with input user_id
    user = get_user_base(user_id)['resource']
    print(user)

    # get pass from secret
    secret_user = get_secret(user_id)

    if secret_user[user["password"]['data']] == password:
        return {
            "success": True,
            "data": "Login successfully.",
        }
    else:
        return {
            "success": False,
            "data": "Password incorrect.",
        }
