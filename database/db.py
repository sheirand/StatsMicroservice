import boto3
from core import settings

dynamodb = boto3.resource(
    'dynamodb',
    region_name="us-west-2",
    aws_access_key_id=settings.AWS_DYNAMODB_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_DYNAMODB_ACCESS_KEY,
    endpoint_url='http://localhost:8001'
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
    except Exception as e:
        print(e)

