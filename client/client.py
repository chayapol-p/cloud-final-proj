import os
import requests
import base64
import bcrypt

# endpoint api gateway for use lambdafuction
endpoint = 'https://shwoiyr3gb.execute-api.ap-southeast-1.amazonaws.com/default/Cloud-Final-FinalProject490383E6-gusO3NuxUHHh'

headers = {'Content-type': 'application/json; charset=utf-8'}

uuid = None


def newuser(username, password):  # create new user
    # password = bcrypt.kdf(password.encode('UTF-8'),
    #                       salt=b'bnb2022', desired_key_bytes=32, rounds=100)
    param = {'username': username, 'password': password, 'method': 'newuser'}
    response = requests.post(
        endpoint, params=param, headers=headers)

    return response.json()


def login(username, password):
    param = {'username': username, 'password': password, 'method': 'login'}
    response = requests.post(
        endpoint, params=param, headers=headers)

    return response.json()


def textract(file):
    directory = os.getcwd()  # get current directory for write new file
    path = os.path.join(directory, file)
    pic_bytes = open(path, 'rb').read()
    pic_64 = base64.b64encode(pic_bytes)
    param = {'method': 'textract'}
    response = requests.post(
        endpoint, params=param, headers=headers, data=pic_64)

    return response.json()


# def put(data):
#     param = {'user_id': uuid, 'method': 'put'}
#     response = requests.post(
#         endpoint, params=param, headers=headers, data=data)

#     return response


# def view(appname):
#     param = {'user_id': uuid, 'method': 'view', 'appname': appname}
#     response = requests.post(
#         endpoint, params=param, headers=headers)

#     return response


# def get():
#     param = {'method': 'put'}
#     response = requests.post(
#         endpoint, params=param, headers=headers)

#     return response


print('''Welcome to Samsun-G Application
======================================================
Please input command (newuser username password, textract filename
If you want to quit the program just type quit.
======================================================''')

# put filename, put username password, get uuid, view resource, or logout).

while True:
    command_input = input(">>")
    comands = command_input.split(' ')

    if comands[0] == 'newuser':
        response = newuser(comands[1], comands[2])
        print(response)

    if comands[0] == 'login':
        response = login(comands[1], comands[2])
        print(response)

    if comands[0] == 'textract':
        print(textract(comands[1]))

    if comands[0] == 'quit':
        exit(0)
