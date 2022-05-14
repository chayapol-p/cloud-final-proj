from utils.dynamo import put_dynamo

def create_user_handler(username, password, **kwargs):
    data_insert = {
        "username": {"data": username, "is_secret": False},
        "password": {"data": password, "is_secret": False},
    }
    # put_dynamo(random_value,'base','username',userInput['username'])
    # put_dynamo(random_value,'base','password',userInput['password'])
    try:
        put_dynamo(username, "base", data_insert)
    except Exception as e:
        print(repr(e))
        return {
            "success": False,
            # "data": "201 Created"
            "data": repr(e),
        }
    # data = dynamo_client.scan(TableName=TABLE_NAME, FilterExpression=Attr("resource_key").eq("base") & Attr("data").contains("username"))

    return {
        "success": True,
        # "data": "201 Created"
        "data": "",
    }


def login_handler():
    print("Test Pass")