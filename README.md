# cloud-final-proj

## Requirements
- python poetry
> run `pip install poetry`
- aws cdk cli
> run `npm insatll -g aws-cdk`
- aws cli
> run `brew install aws-cli`

## How to use
    First run `poetry shell` then `poetry install` to install all dependencies

### Client
    `cd client` then run `python3 client.py` to start the client cli.

### Server
    To deploy the server
- Edit the config variable in `server/app.py`
- Add AWS credentials by run `aws configure` in terminal
- Run `cd server`
- Run `cdk bootstrap` then `cdk deploy` to deploy the server to your aws account

> to destroy and clean up run `cdk destroy` then delete secrets in Secrets Manager manually.
