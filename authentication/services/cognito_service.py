import boto3
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64


class CognitoService:
    def __init__(self, region, user_pool_id, app_client_id, app_client_secret):
        self.client = boto3.client("cognito-idp", region_name=region)
        self.user_pool_id = user_pool_id
        self.app_client_id = app_client_id
        self.app_client_secret = app_client_secret

    def get_secret_hash(self, email):
        message = email + self.app_client_id
        dig = hmac.new(
            str(self.app_client_secret).encode("utf-8"), msg=str(message).encode("utf-8"), digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()

    def register_user(self, name, phone, email, password):
        try:
            response = self.client.sign_up(
                ClientId=self.app_client_id,
                SecretHash=self.get_secret_hash(email),
                Username=email,
                Password=password,
                UserAttributes=[
                    {"Name": "name", "Value": name},
                    {"Name": "phone_number", "Value": phone},
                    {"Name": "email", "Value": email},
                ],
            )
            return response
        except ClientError as e:
            raise e

    def login_user(self, email, password):
        try:
            response = self.client.initiate_auth(
                ClientId=self.app_client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password,
                    "SECRET_HASH": self.get_secret_hash(email),
                },
            )
            return response
        except ClientError as e:
            raise e
