from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Innotter")


def create_page(page: dict):
    try:
        table.put_item(Item=page)
        return page
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_page(user_id: str, page_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id) & Key('page_id').eq(page_id)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
