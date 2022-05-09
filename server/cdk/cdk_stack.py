from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
)
import aws_cdk
from constructs import Construct

import os

dirname = os.path.dirname(__file__)

class FinalProjStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, region: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table_name = "FinalProjectData"

        lambda_fn = lambda_.Function(
            self,
            "FinalProject",
            code=lambda_.Code.from_asset(os.path.join(dirname, "lambda")),
            handler="lambda-handler.main",
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={"TABLE_NAME": table_name, "REGION": region},
        )

        # Build our DynamoDb Table
        dynamo = dynamodb.Table(
            self,
            table_name,
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name="user_id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="resource_key", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PROVISIONED,
            read_capacity=2,
            write_capacity=2,
        )
        
        dynamo.grant_full_access(lambda_fn)
        lambda_fn.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                'AmazonTextractFullAccess'
            )
        )
