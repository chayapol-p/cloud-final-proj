import json

from handlers.feature import put_card_handler, test_create_secret_handler, put_app_handler, list_resource_handler, get_resource_handler
from handlers.user import create_user_handler, login_handler

# Main lambda function
def lambda_handler(event, context):
    # log the incomming event
    # print("event:", event)

    # Extract the body and command from event data
    body = json.loads(event["body"])
    print("event body:", body)

    command = event["queryStringParameters"]["method"]
    print("Method:", command)

    # Define function for each command in commands var.
    commands = ["newuser", "login", "put_card", "put_app", "list_resource", "get_resource"]
    command_fns = [
        create_user_handler,
        login_handler,
        put_card_handler,
        put_app_handler,
        list_resource_handler,
        get_resource_handler
    ]

    # Check if input command is available
    if command in commands:
        # Set up function for this command
        fn = command_fns[commands.index(command)]

        # Call the function with incomming body data
        result = fn(**body)

        # If Function not success, return with error
        if not result["success"]:
            response = {
                "statusCode": 418,
                "body": json.dumps({"detail": result}),
            }
        else:
            # Otherwise return success with result
            response =  {
                "statusCode": 200,
                "body": json.dumps({"detail": result}),
            }

    else:
        # If command not valid, return with error
        response = {
            "statusCode": 422,
            "body": json.dumps({"detail": "Command not found."}),
        }

    print(json.dumps(response, indent=2))
    return response