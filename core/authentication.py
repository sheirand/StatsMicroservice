from http.client import HTTPException
from core.settings import JWT_SECRET_KEY
import jwt
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from database.db import dynamodb


class JWTAuthentication(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=403, detail="Not authenticated"
                )
            else:
                return None
        return JWTAuthentication.has_access(credentials)

    @staticmethod
    def has_access(credentials):
        """Checks JWT-owner access"""

        token = credentials

        try:
            payload = jwt.decode(
                token, key=JWT_SECRET_KEY, algorithms=['HS256']
            )

            if not JWTAuthentication.check_user_id(str(payload["id"])):
                raise HTTPException(
                    status_code=403, detail="Not authenticated"
                )
            return str(payload["id"])

        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError) as error:
            raise HTTPException(status_code=403, detail=f"{error}")

    @staticmethod
    def check_user_id(user_id: str):
        table = dynamodb.Table("Innotter")
        response = table.query(
            KeyConditionExpression="user_id = :id",
            ExpressionAttributeValues={":id": user_id}
        )
        return response["Items"]
