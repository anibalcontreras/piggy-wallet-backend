import boto3
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64
from django.contrib.auth import get_user_model


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
            cognito_uuid = response["UserSub"]
            User = get_user_model()
            User.objects.create_user(
                username=email, email=email, password=password, first_name=name, phone=phone, user_id=cognito_uuid
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

    def list_users(self, attributes_to_get=None, limit=None, pagination_token=None):
        """
        Lists users from the Cognito user pool.
        """
        try:
            response = self.client.list_users(UserPoolId=self.user_pool_id)
            users = response["Users"]
            simplified_users = self.extract_user_info(users)
            return simplified_users
        except Exception as e:
            # Error handling remains the same
            if hasattr(e, 'response') and 'Error' in e.response:
                error_message = "Couldn't list users for {}. Here's why: {}: {}".format(
                    self.user_pool_id,
                    e.response["Error"]["Code"],
                    e.response["Error"]["Message"]
                )
            else:
                error_message = "Couldn't list users for {}. An error occurred: {}".format(
                    self.user_pool_id, str(e)
                )
            return error_message

    def extract_user_info(self, users):
        simplified_users = []
        for user in users:
            user_info = {"Username": user["Username"]}
            for attr in user["Attributes"]:
                if attr["Name"] == "email":
                    user_info["Email"] = attr["Value"]
                elif attr["Name"] == "name":
                    user_info["Name"] = attr["Value"]
            simplified_users.append(user_info)
        return simplified_users
