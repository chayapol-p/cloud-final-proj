#!/usr/bin/env python3

import aws_cdk as cdk
from aws_cdk import aws_rds as rds

from cdk.cdk_stack import FinalProjStack


config = {
    "account_id": "402007393381",
    "region": "ap-southeast-1",
}

stack_config = cdk.Environment(account=config["account_id"], region=config["region"])

stack_params = {
    "env": stack_config,
    "region": config["region"],
}

app = cdk.App()

FinalProjStack(app, "Cloud-Final", **stack_params)

app.synth()
