import jwt
from jwt import PyJWKClient, PyJWKSetError
from django.conf import settings
from rest_framework import authentication, exceptions


class CognitoAuthentication(authentication.BaseAuthentication):
    def __init__(self):
        self.cognito_jwks_url = (
            f"https://cognito-idp.{settings.AWS_REGION}.amazonaws.com/"
            f"{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        )
        self.jwks_client = PyJWKClient(self.cognito_jwks_url)

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            token = auth_header.split()[1]
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(token, signing_key.key, algorithms=["RS256"], aud=settings.COGNITO_APP_CLIENT_ID)
            return (payload, None)
        except PyJWKSetError as e:
            print(f"JWK Set Error: {e}")
            raise exceptions.AuthenticationFailed("JWK Set did not contain any usable keys")
        except jwt.ExpiredSignatureError as e:
            print(f"Expired Signature Error: {e}")
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.DecodeError as e:
            print(f"Decode Error: {e}")
            raise exceptions.AuthenticationFailed(f"Error decoding token: {e}")
        except jwt.InvalidTokenError as e:
            print(f"Invalid Token Error: {e}")
            raise exceptions.AuthenticationFailed(f"Invalid token: {e}")
        except Exception as e:
            print(f"Unhandled Exception: {e}")
            raise exceptions.AuthenticationFailed(f"Unhandled exception: {e}")
