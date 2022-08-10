import boto3
import botocore.exceptions
import logging
from core import settings


logger = logging.getLogger(__name__)

dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.AWS_DYNAMODB_REGION,
    aws_access_key_id=settings.AWS_DYNAMODB_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_DYNAMODB_ACCESS_KEY,
    endpoint_url=settings.AWS_DYNAMODB_ENDPOINT
)


tables = [
    {
        "TableName": "Innotter",
        "AttributeDefinitions": [
            {
                "AttributeName": "user_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "page_id",
                "AttributeType": "S"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": 'user_id',
                "KeyType": "HASH"
            },
            {
                "AttributeName": 'page_id',
                "KeyType": "RANGE"
            }

        ]
    }
]


def create_tables():
    try:
        for table in tables:
            dynamodb.create_table(
                TableName=table["TableName"],
                KeySchema=table["KeySchema"],
                AttributeDefinitions=table["AttributeDefinitions"],
                BillingMode="PAY_PER_REQUEST"
            )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            logger.info("db is ready to use!")
        else:
            logger.warning(e)
