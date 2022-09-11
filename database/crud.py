from database.db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from boto3.dynamodb.conditions import Key


class CRUDManager:

    __table = dynamodb.Table("Innotter")

    @staticmethod
    def create_page(body: dict):
        print(body)
        payload = {"page_id": str(body["id"]),
                   "user_id": str(body["user_id"]),
                   "statistic": {
                       "followers": 0,
                       "likes": 0,
                       "posts": 0
                   }}
        try:
            page = CRUDManager.__table.put_item(Item=payload)
            return JSONResponse(content=page, status_code=201)
        except ClientError as e:
            return JSONResponse(content=e.response["Error"], status_code=500)

    @staticmethod
    def get_stats(user_id: str, page_id: str):
        try:
            response = CRUDManager.__table.query(
                KeyConditionExpression=Key("page_id").eq(page_id) & Key("user_id").eq(user_id)
            )
            print(response)
            return response["Items"]
        except ClientError as e:
            return JSONResponse(content=e.response["Error"], status_code=500)

    @staticmethod
    def update_param(method: str, body: dict):
        match method:
            case "add followers" | "remove followers":
                param = "followers"
                num = body["num"]
            case "new post":
                param = "posts"
                num = 1
            case "like":
                param = "likes"
                num = 1
            case "unlike":
                param = "likes"
                num = -1
            case _:
                raise HTTPException(status_code=500)
        try:
            CRUDManager.__table.update_item(
                Key={
                    "page_id": str(body["id"]),
                    "user_id": str(body['user_id'])
                },
                UpdateExpression=f"SET statistic.{param} = statistic.{param} + :value",
                ExpressionAttributeValues={":value": num}
            )
        except ClientError as e:
            return JSONResponse(content=e.response["Error"], status_code=500)

    @staticmethod
    def delete_page(body: dict):
        try:
            CRUDManager.__table.delete_item(
                Key={
                    "page_id": str(body["id"]),
                    "user_id": str(body["user_id"])
                }
            )
        except ClientError as e:
            return JSONResponse(content=e.response["Error"], status_code=500)
