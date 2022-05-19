import os
import requests
import base64

# endpoint api gateway for use lambdafuction
endpoint = "https://shwoiyr3gb.execute-api.ap-southeast-1.amazonaws.com/default/Cloud-Final-FinalProject490383E6-gusO3NuxUHHh"

# API header
headers = {"Content-type": "application/json; charset=utf-8"}

# initial user when not logged in
user_id_base = ""


def newuser(user_id, password):  # create new user
    param = {"method": "newuser"}
    data = {"user_id": user_id, "password": password}
    response = requests.post(endpoint, params=param, headers=headers, json=data)

    return response.json()


def login(user_id, password): # login
    param = {"method": "login"}
    data = {"user_id": user_id, "password": password}
    response = requests.post(endpoint, params=param, headers=headers, json=data)

    return response.json()


def put_card(resource, file, cvv): # Store data from card images.
    directory = os.getcwd()  # get current directory for write new file
    path = os.path.join(directory, file)
    pic_bytes = open(path, "rb").read() # read picture
    pic_64 = base64.b64encode(pic_bytes).decode("utf8") # encode bytes to base64
    param = {"method": "put_card"}
    data = {
        "user_id": user_id_base,
        "resource": resource,
        "picture": pic_64,
        "cvv": cvv,
    }
    response = requests.post(endpoint, params=param, headers=headers, json=data)

    return response.json()


def put_app(app, username, password): # Save other app account information.
    param = {"method": "put_app"}
    data = {
        "user_id": user_id_base,
        "app": app,
        "username": username,
        "password": password,
    }
    response = requests.post(endpoint, params=param, headers=headers, json=data)

    return response.json()


def view(resource): # get list of saved data by the source key
    param = {"method": "list_resource"}
    data = {"user_id": user_id_base, "resource": resource}
    response = requests.post(endpoint, params=param, headers=headers, json=data)

    response_data = response.json()["detail"] # list of saved data

    print("choose the number you want (default [0])")
    for i in range(len(response_data["data"])):        # Show all in the list.
        print(f"[{i}]", response_data["data"][i][1])
    
    select = int(input("choose >> "))  # Get input from user to call get function

    response = get(response_data["data"][select][0])

    return response.json()


def get(resource_key): #get saved data with password or cvv.
    param = {"method": "get_resource"}
    data = {"user_id": user_id_base, "resource_key": resource_key}
    response = requests.post(endpoint, params=param, headers=headers, json=data)

    return response


print(
    """                     Welcome to Samsun-G Application
==================================================================================
Please input command (newuser username password, login username password,
put_app appname app_username app_password, put_card resource filename,view appname
If you want to quit the program just type quit.
=================================================================================="""
)


while True:
    command_input = input(user_id_base + " >> ") # get commands from user
    commands = command_input.split(" ")

    if commands[0] == "newuser":
        response = newuser(commands[1], commands[2])

    if commands[0] == "login":
        response = login(commands[1], commands[2])
        if response["detail"]["success"]: # if login success set user_id_base = command[1]
            user_id_base = commands[1]

    if commands[0] == "logout": # if logout set user_id_base = '' (initial user)
        user_id_base = ""

    if commands[0] == "put_app":
        response = put_app(commands[1], commands[2], commands[3])

    if commands[0] == "put_card":
        response = put_card(commands[1], commands[2], commands[3])

    if commands[0] == "view":
        response = view(commands[1])

    if commands[0] == "quit":
        exit(0)

    print(response)
