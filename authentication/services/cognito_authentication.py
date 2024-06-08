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
            raise exceptions.AuthenticationFailed(f"JWK Set did not contain any usable keys: {e}")
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed(f"Token has expired: {e}")
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed(f"Error decoding token: {e}")
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {e}")
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Unhandled exception: {e}")
