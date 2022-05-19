# cloud-final-proj

## Requirements
- python poetry
> run `pip install poetry`
- aws cdk cli
> run `npm insatll -g aws-cdk`
- aws cli
> see more detail in [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## How to use
First run `poetry shell` then `poetry install` to install all dependencies

### Client
`cd client` then run `python3 client.py` to start the client cli. If you have your own Lambda please edit `endpoint` variable in `client/client.py`

 - To create new user, run
 ```
 >> newuser <username> <password>
 ```
 - To Login, run
 ```
 >> login <username> <password>
 ```
 - To Add application details, run
 ```
 {username} >> put_app <appname> <app_username> <app_password>
 ```
 - To Add card details, run
 ```
 {username} >> put_card <name-to-save> <path-of-card-image> <cvv>
 ```
 > The card image should be same directory as client.py
 - To View your application or card detail, run
 ```
 {username} >> view <resource-name> <path-of-card-image> <cvv>
 ```


### Server
To deploy the server
- Edit the config variable in `server/app.py`
- Add AWS credentials by run `aws configure` in terminal
- Run `cd server`
- Run `cdk bootstrap` then `cdk deploy` to deploy the server to your aws account

> to destroy and clean up run `cdk destroy` then delete secrets in Secrets Manager manually.

## Noted
Code for lambda and explanation of it stored in `server/cdk/lambda/`
